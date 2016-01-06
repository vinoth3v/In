import json

class FormEntityAdminEditBundle(Form):

	def __init__(self, data = None, items = None, post = None, **args):


		if data is None: data = {}
		if post is None: post = {}

		if 'id' not in data:
			data['id'] = 'FormEntityAdminEditBundle'

		super().__init__(data, items, **args)

		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		
		try:
			bundle_config = IN.entitier.entity_bundle[entity_type][entity_bundle]
		except Exception as e:
			IN.context.not_found()
		
		set = self.add('FieldSet', {
			'id' : 'configset',
			'title' : s('Config {entity_type} {entity_bundle}', {
				'entity_type' : entity_type,
				'entity_bundle': entity_bundle,
			}),
			'css' : ['i-form-row i-margin-large']
		})
		
		title = post.get('entity_bundle_title', '')
		if not title:
			try:
				title = bundle_config['data']['title']
			except KeyError as e:
				title = entity_bundle
				
		set.add('TextBox', {
			'id' : 'entity_bundle_title',
			'value' : title,
			'title' : s('Bundle title'),
			'placeholder' : s('Bundle title'),
			'validation_rule' : ['Length', 3, '>', 0, 'The Bundle title length should be greater than 3!'],
			'css' : ['i-width-1-1 i-form-large'],
			'required' : True,
			'info' : s('Human readble display title.'),
			'weight' : 0,
		})
		
		view_modes = post.get('entity_bundle_view_modes', None)
		if view_modes is None:
			try:
				view_modes = IN.entitier.view_modes(entity_type, entity_bundle)
				view_modes = '\n'.join(view_modes)
			except KeyError as e:
				view_modes = ''
				
		set.add('TextArea', {
			'id' : 'entity_bundle_view_modes',
			'value' : view_modes,
			'title' : s('Bundle view modes'),
			'placeholder' : s('Bundle view modes'),
			'css' : ['i-width-1-1 i-form-large'],
			'required' : True,
			'info' : s('Display view modes that is used in Themer settings. One per line.'),
			'weight' : 1,
		})
		
		set.add('CheckBox', {
			'label' : 'Default status?',
			'id' : 'default_status',
			'value' : 1,	# returned value if checked
			'checked' : post.get('default_status', '') == '1' or bundle_config['data'].get('default_status', True),
			'info' : s('Default entity published status. Published if checked, otherwise not.'),
		})
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-grid']
		})

		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Save'),
			'css' : ['i-button i-button-primary']
		})
		
		admin_path = IN.APP.config.admin_path
		
		set.add('Link', {
			'value' : s('Cancel'),
			'href' : ''.join(('/', admin_path, '/structure/entity/!', entity_type, '/bundle')),
			'css' : ['i-button']
		})
		
		self.css.append('ajax i-panel i-panel-box i-margin-large')

@IN.register('FormEntityAdminEditBundle', type = 'Former')
class FormEntityAdminEditBundle(FormFormer):

	
	def submit(self, form, post):

		if form.has_errors:
			return

		db = IN.db
		connection = db.connection
		
		entity_type = form.args['entity_type']
		entity_bundle = form.args['entity_bundle']
		
		
		try:
			
			title = form['configset']['entity_bundle_title'].value
			view_modes = []
			
			for mode in form['configset']['entity_bundle_view_modes'].value.split('\n'):
				view_modes.append(mode.strip())
			
			default_status = 1 if form['configset']['default_status'].checked else 0
			
			data = {
				'title' : title,
				'view_modes' : view_modes,
				'default_status' : default_status,
			}
			
			data = json.dumps(data, skipkeys = True, ensure_ascii = False)
			
			cursor = db.update({
				'table' : 'config.config_entity_bundle',
				'set' : [['data', data]],
				'where' : [['entity_type', entity_type], ['entity_bundle', entity_bundle]], # id not used
			}).execute()

			connection.commit()
			
			admin_path = IN.APP.config.admin_path
			
			form.redirect = ''.join((admin_path, '/structure/entity/!', entity_type, '/bundle'))
			
		except Exception as e:
			connection.rollback()
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again!')
			form.has_errors = True
			return

