@IN.register('Status', type = 'EntityAddForm')
class StatusAddForm(In.entity.EntityAddForm):
	'''Status Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		to_entity_type = args['to_entity_type']
		to_entity_id = args['to_entity_id']
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary'],
			'weight' : 101, # last
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Save'),
			'css' : ['i-button i-button-primary']
		})
		
		self.css.append('ajax i-panel i-panel-box i-margin-large')

@IN.register('StatusAddForm', type = 'Former')
class StatusAddFormFormer(In.entity.EntityAddFormFormer):
	'''Status Form Former'''

	def submit_prepare(self, form, post):
		
		args = form.args
		
		post['to_entity_type'] = args['to_entity_type']
		post['to_entity_id'] = args['to_entity_id']
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
			
		# create entity object from form post
		entity_type = form.entity_type
		entity_bundle = form.entity_bundle

		entity = form.processed_data['entity']
		
	def submit(self, form, post):
		
		super().submit(form, post)
		
		if form.has_errors:
			return
		
		form.redirect = None #'/'.join((form.args['parent_entity_type'].lower(), str(form.args['parent_entity_id'])))

		# set result commands
		if form.entity_id is not None:
			status = IN.entitier.load('Status', form.entity_id)
			if status is not None:
				
				# we need to included comments boxes when theming
				status.__include_comment_boxes__ = True
				output = IN.themer.theme(status, view_mode = 'full')
				element_id = 'status_added_list'
				form.result_commands = [{
					'method' : 'prepend',
					'args' : ['#' + element_id, output]
				}]

				# clear the body field
				for field in form['field_status_body'].values():
					# TODO: reset to default
					field.value = ''



@IN.register('StatusAddForm', type = 'Themer')
class StatusAddFormThemer(FormThemer):
	'''StatusAddForm themer'''

	def theme(self, obj, format, view_mode, args):
		
		
		if 'field_status_body' in obj:
			for k, field in obj['field_status_body'].items():
				if isinstance(field, In.html.tags.TextArea):
					field.rows = 2
		super().theme(obj, format, view_mode, args)

	def theme_process_variables(self, obj, format = 'html', view_mode = 'default', args = None):
		super().theme_process_variables(obj, format, view_mode, args)

		nabar = args['context'].nabar
		
		args['nabar_name'] = nabar.name
		args['nabar_id'] = nabar.id
		args['nabar_picture'] = IN.nabar.nabar_profile_picture_themed(nabar)
