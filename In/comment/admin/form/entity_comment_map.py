import json

class FormEntityCommentMapAdmin(Form):

	def __init__(self, data = None, items = None, post = None, **args):

		if data is None: data = {}
		if post is None: post = {}
		
		if 'id' not in data:
			data['id'] = self.__type__

		super().__init__(data, items, **args)
		
		#roleset = self.add(type = 'FieldSet', data = {
			#'id' : 'mapset',
			#'title' : s('Comment to Entity mapp'),
			#'css' : ['i-form-row i-margin-large']
		#})

		config_entity_bundle = IN.entitier.entity_bundle
		if post and 'ajax_args' in post:
			ajax_args = post['ajax_args']
			
			self.partial = True
			
			entity_type = ajax_args['entity_type']

			if entity_type not in config_entity_bundle:
				return
				
			if 'entity_bundle' not in ajax_args: # entity only
				
				self.ajax_elements = [entity_type] # render only this elements
				
				entityset = self.add('TextDiv', {
					'id' : entity_type,
					'value' : entity_type.join(('<h3>','</h3>')),
					'css' : ['i-panel i-panel-divider']
				})
				
				bundles = config_entity_bundle[entity_type]
				for entity_bundle, bundle_config in bundles.items():
					attr = {'entity_type' : entity_type, 'entity_bundle' : entity_bundle}
					attr = json.dumps(attr, skipkeys = True, ensure_ascii = False)
					bundleset = entityset.add('TextDiv', {
						'id' : entity_type + entity_bundle,
						'value' : ''.join(('<h3 class="ajax" data-ajax_args=\'', attr, '\'>', entity_bundle, '</h3>')),
						'css' : ['i-panel i-panel-divider']
					})
			else:

				# bundle clicked
				entity_bundle = ajax_args['entity_bundle']
				
				self.ajax_elements = [entity_type + entity_bundle]
				entity_type_bundle = entity_type + entity_bundle
				bundleset = self.add('TextDiv', {
					'id' : entity_type_bundle,
					'value' : entity_bundle.join(('<h3>', '</h3>')),
					'css' : ['i-panel i-panel-divider']
				})

				config = IN.commenter.config_comments_enabled
				config = config.get(entity_type, {}).get(entity_bundle, {})

				enabled = config.get('comment_bundle', False)
				data = config.get('data', {})
				
				bundleset.add('CheckBox', {
					'id' : entity_type_bundle + '_enable_comments',
					'name' : ''.join(('enable_comments[', entity_type, '][', entity_bundle, ']')),
					'label' : s('Enable comments'),
					'value' : 'on',
					'checked' : enabled,
					'css' : ['']
				})
				
				options = {}

				bundles = IN.entitier.entity_bundle['Comment']
				
				for bundle, con in bundles.items():
					options[bundle] = bundle
					
				bundleset.add('HTMLSelect', {
					'id' : entity_type_bundle + '_comment_bundle',
					'name' : ''.join(('comment_bundle[', entity_type, '][', entity_bundle, ']')),
					'value' : enabled if enabled else '',
					'title' : s('Comment type'),
					'options' : options,
					'required' : True,
					'multiple' : False,
					'css' : ['i-form-large']
				})
		
				bundleset.add('HTMLSelect', {
					'id' : entity_type_bundle + '_comment_level',
					'name' : ''.join(('comment_level[', entity_type, '][', entity_bundle, ']')),
					'value' : data.get('comment_level', 0),
					'title' : s('Comment level'),
					'options' : range(10),
					'required' : True,
					'multiple' : False,
					'css' : ['i-form-large']
				})
				
				actionset = bundleset.add('FieldSet', {
					'id' : entity_type_bundle + '_actions',
					'css' : ['i-form-row i-margin-large']
				})
				
				attr = {'entity_type' : entity_type, 'entity_bundle' : entity_bundle}
				attr = json.dumps(attr, skipkeys = True, ensure_ascii = False)
				
				actionset.add('Submit', {
					'id' : entity_type_bundle + '_submit',
					'value' : s('Save'),
					'name' : ''.join(('submit[', entity_type, '][', entity_bundle, ']')),
					'attributes' : {'data-ajax_args' : attr},
					'css' : ['i-button i-button-primary i-button-large']
				})
				# all comment type


		else:
			for entity_type, bundles in config_entity_bundle.items():
				attr = {'entity_type' : entity_type}
				attr = json.dumps(attr, skipkeys = True, ensure_ascii = False)
				entityset = self.add('TextDiv', {
					'id' : entity_type,
					'value' : ''.join(('<h3 class="ajax" data-ajax_args=\'', attr, '\'>', entity_type, '</h3>')),
					'css' : ['i-panel i-panel-divider']
				})
				
				#for entity_bundle, bundle_config in bundles.items():
					#bundleset = entityset.add(type = 'FieldSet', data = {
						#'id' : entity_type + entity_bundle,
						#'title' : entity_bundle,
						#'css' : ['i-form-row i-margin-large']
					#})

		
		#if group not in access_keys:
			#roleset.add(type = 'TextDiv', data = {
				#'id' : 'terms',
				#'value' : s('''Access keys for the group {group} not found!''', {'group' : group}),
				#'css' : ['i-text-primary']
			#})
			#return

		#access_keys = access_keys[group]

		##set.add(type = 'TextDiv', data = {
			##'value' : s('Access keys'),
			##'css' : ['i-width-3-10']
		##})

		#role_options = OrderedDict()
		
		#for rid, role in roles.items():

			## admin always has access
			#if rid == IN.nabar.admin_role_id:
				#continue
			
			#name = role['name']
			#role_options[str(rid)] = name
			##set.add(type = 'TextDiv', data = {
				##'id' : 'role_' + str(rid),
				##'value' : name,
				##'css' : ['']
			##})

		##set.add(type = 'TextDiv', data = {
			##'value' : '<hr class="i-grid-divider">',
		##})

		#post_access = post.get('access', {})

		#flags = {
			#'danger' : s('danger').join((' <span class="i-badge i-badge-danger">', '</span>')),
			#'warning' : s('warning').join((' <span class="i-badge i-badge-warning">', '</span>'))
		#}

		#for key, data in access_keys.items():
			#keyset = roleset.add(type = 'FieldSet', data = {
				#'id' : 'set_' + key,
				#'css' : ['i-form-row i-margin-large i-grid i-grid-divider']
			#})

			#title = data.get('title', '')
			#info = data.get('info', '')
			#flag = data.get('flag', '')
			#flag = flags.get(flag, '')
			
			#text = '''<h3><b>{title}</b>{flag}</h3> <i>Access key: {key}</i><br>
			#{info}'''.format(title = title, key = key, info = info, flag = flag)
			
			#keyset.add(type = 'TextDiv', data = {
				#'id' : 'access_text_' + key,
				#'value' : text,
				#'css' : ['i-width-1-1 i-margin-bottom']
			#})

			##keyset.add(type = 'TextDiv', data = {
				##'value' : '<hr class="i-grid-divider">',
			##})

			
			#value = access_roles.get(key, set())

			#keyset.add(type = 'CheckBoxes', data = {
				#'id' : '-'.join(('access', str(rid), key)),
				#'name' : ''.join(('access[', key, ']')),
				#'value' : value,
				#'options' : role_options,
				#'css' : ['i-grid']
			#})
			
			##for rid, role in roles.items():
				##set.add(type = 'CheckBox', data = {
					##'id' : '-'.join(('access', str(rid), key)),
					##'name' : ''.join(('access[', str(rid), '][', key, ']')),
					##'value' : post.get('name'),
					##'css' : ['']
				##})

			#roleset.add(type = 'TextDiv', data = {
				#'value' : '<div class="i-grid-divider"></div>',
			#})
		
		##set.add(type = 'TextDiv', data = {
			##'id' : 'terms',
			##'value' : s('''By registering to our site you are accepting our {term_link}.''', term_link = tlink),
			##'css' : ['i-text-primary']
		##})

		#roleset.add(type = 'Submit', data = {
			#'id' : 'submit',
			#'value' : s('Save Access'),
			#'css' : ['i-button i-button-primary i-button-large']
		#})

		self.css.append('ajax i-panel i-panel-box i-margin-large')

@IN.register('FormEntityCommentMapAdmin', type = 'Former')
class FormEntityCommentMapAdminFormer(FormFormer):

	#def validate(self, form, post):
		#pprint(post)
		#if form.has_errors: # fields may have errors
			#return

	def submit(self, form, post):

		if form.has_errors:
			return


		connection = IN.db.connection
		
		try:

			if 'element_id' not in post or post['element_id'] != 'submit':
				return
			
			if 'ajax_args' in post:

				ajax_args = post['ajax_args']
				
				entity_type = ajax_args['entity_type']
				entity_bundle = ajax_args['entity_bundle']

				# delete old keys
				cursor = IN.db.delete({
					'table' : 'config.config_entity_bundle_comment',
					'where' : [['entity_type', entity_type], ['entity_bundle', entity_bundle]],
				}).execute()

				try:
					
					if post['enable_comments'][entity_type][entity_bundle] == 'on':
						
						try:
							
							comment_bundle = post['comment_bundle'][entity_type][entity_bundle]
							
							if comment_bundle:
								data = {
									'comment_level' : int(post['comment_level'][entity_type][entity_bundle])
								}
								data = json.dumps(data, skipkeys = True, ensure_ascii = False)
								values = [entity_type, entity_bundle, comment_bundle, data]
								cursor = IN.db.insert({
									'table' : 'config.config_entity_bundle_comment',
									'columns' : ['entity_type', 'entity_bundle', 'comment_bundle', 'data'],
									'values' : [values],
								}).execute()

						except KeyError:
							pass
				except KeyError:
					pass
			
				# commit
				connection.commit()

				# rebuild access
				# TODO: NOT USEFULL. server runs on multiple instances
				IN.commenter.build_config_comments_enabled()
				
		except Exception as e:
			connection.rollback()
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		#form.redirect = '/admin/nabar/role'

