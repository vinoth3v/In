import json

class FormImageBrowser(Form):

	def __init__(self, data = None, items = None, post = None, **args):


		if data is None: data = {}
		if post is None: post = {}
		
		if 'id' not in data:
			data['id'] = 'FormImageBrowser'

		super().__init__(data, items, **args)
		
		
		
		tab = self.add('Ul', {
			'id' : 'browse_tab',
			'attributes' : {
				'data-i-switcher' : json.dumps({'connect' : '#browse_tab_content'}, skipkeys = True, ensure_ascii = False)
			},
			'css' : ['i-tab'],
			'weight' : 1
		})
		
		tab.add('Li').add('Link', {
			'value' : s('Browse Images')
		})
		
		tab.add('Li').add('Link', {
			'value' : '<i class="i-icon-upload"></i> ' + s('Upload')
		})
		
		tab_content = self.add('Ul', {
			'id' : 'browse_tab_content',
			'css' : ['i-switcher'],
			'weight' : 5
		})
		
		#self.ajax_elements.append('browse_tab_content')
		
		browse_content = tab_content.add('Li', {
			'id' : 'image_browse_content_li',
		}).add('TextDiv', {
			'id' : 'image_browse_content',
			'css' : ['i-overflow-container']
		})
		
		if 'new_upload' not in post: # add it later
			self.__list_images__()
		
		# upload
		upload_content = tab_content.add('Li').add('TextDiv', {})
		
		upload_content.add('FileUpload', {
			'id' : 'new_upload',
			'title' : s('Select image from disk'),
			'css' : ['ajax i-width-1-1 i-form-large'],
			'attributes' : {
				'data-ajax_partial' : 1
			},
		})
		
		set = self.add('TextDiv', {
			'id' : 'actionset',
			'css' : ['i-modal-footer i-text-right'],
			'weight' : 50, # last
		})
		
		set.add('Link', {
			'name' : 'cancel',
			'value' : s('Cancel'),
			'css' : ['i-button i-modal-close']
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'name' : 'submit',
			'value' : s('Select'),
			'css' : ['i-button i-button-primary']
		})


		self.css.append('i-margin-large')
	
	def __list_images__(self):
		
		browse_content = self['browse_tab_content']['image_browse_content_li']['image_browse_content']
		nabar_id = IN.context.nabar.id
		limit = 10
		
		query = IN.db.select({
			'tables' : [['entity.file', 'f']],
			'columns' : ['f.id'],
			'where' : [
				['f.nabar_id', nabar_id],
				['f.type', 'image'],
				['f.status', '>', 0],		
			],
			'order' : {'f.created' : 'DESC'},
			'limit' : limit,
		})
		
		pager = {
			'type' : 'PagerNumberList',
			'data' : {
				'link_attributes' : {
					'data-ajax_type' : 'POST',
				}
			},
		}

		lister = Object.new('ObjectLister', {
			'id' : 'files',
			'entity_type' : 'File',
			'view_mode' : 'small',
			'entity_load_query' : query,
			'handler_prepare_objects' : handler_prepare_objects,
			'pager' : pager,
			'limit' : limit,
			'css' : ['i-container'],
			'content_panel' : {
				'css' : ['i-grid i-grid-medium i-margin i-margin-top'], # i-grid-width-small-1-2 i-grid-width-medium-1-5
			},
			'container' : browse_content,
		})
		
		# handle the list
		lister.list()
			
def handler_prepare_objects(self):
	
	limit = self.limit
	
	if self.current > 1:
		if self.current == 2:
			limit = [limit, limit]
		else:
			limit = [(self.current -1) * limit, limit]
		self.entity_load_query.limit = limit
	
	cursor = self.entity_load_query.execute()
	entitier =  IN.entitier
	content_panel = self.content_panel
	
	if cursor.rowcount > 0:
		
		result = cursor.fetchall()
		
		entity_ids = []
		for r in result:
			if r[0] not in entity_ids:
				entity_ids.append(r[0])
		
		entities = entitier.load_multiple(self.entity_type, entity_ids)
		weight = 1
		for id in entity_ids: # keep order
			if id in entities:
				entity = entities[id]
				entity.weight = weight
				
				cid = 'image-browser-img-' + str(id)
				wrapper = content_panel.add('TextDiv', {
					'css' : ['i-width-1-2 i-width-medium-1-4 i-width-large-1-5']
				})
				thumb = wrapper.add('TextDiv', {
					'id' : cid,
					'css' : ['i-thumbnail'],
					'attributes' : {
						'onclick' : 'var t = jQuery(this); t.toggleClass("border-blue-3"); var c = t.find(":checkbox"); c.prop("checked", !c.prop("checked"));'
					},
				})
				
				thumb.add('CheckBox', {
					'id' : cid + '-check',
					'name' : 'selected_files',
					'css' : ['i-hidden'],
					'value' : id,
				})
				
				thumb.add(entity)
				
				weight += 1

@IN.register('FormImageBrowser', type = 'Former')
class FormImageBrowserFormer(FormFormer):

	def validate(self, form, post):

		if form.has_errors: # fields may have errors
			return
		
		try:
			pass
		except Exception as e:
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again!')
			form.has_errors = True
			return
	
	def submit_partial(self, form, post):
		
		# new_upload
		if 'new_upload' in post:
			value = post['new_upload']
			
			if '__upload__' in value and value['__upload__'] and value['path']:
				
				path = value['path']
			
				file_entity_id = In.file.create_file_entity(path, 'image')
				
				if file_entity_id:
					# list
					form.__list_images__()
		
	def submit(self, form, post):

		if form.has_errors:
			return

		try:
			
			ajax_args = form.args['ajax_args']
			field_id = ajax_args['field_id']
			field_name = ajax_args['field_name']
			form_id = ajax_args['form_id']
			
			selected_files =  post.get('selected_files', [])
			
			if selected_files:
				if type(selected_files) is list: # multiple
					options = ''.join(([str(id).join(('<option selected value="', '"></option>')) for id in selected_files]))
				else:
					options = str(selected_files).join(('<option selected value="', '"></option>'))
				
				form.result_commands = [{
					'method' : 'closeAjaxModal',
					'args' : [],
				}]
				
				script = '''
				var c = jQuery('#''' + field_id + '''');
				c.html(' ''' + options + ''' ');
				c.trigger('change');
				'''
				
				form.result_commands.append({
					'method' : 'script',
					'args' : [script]
				})
			
		except Exception as e:
			
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again!')
			form.has_errors = True
			return

