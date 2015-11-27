import json

class FormEntityAdminAddBundle(Form):

	def __init__(self, data = None, items = None, post = None, **args):


		if data is None: data = {}
		if post is None: post = {}

		if 'id' not in data:
			data['id'] = 'FormEntityAdminAddBundle'

		super().__init__(data, items, **args)

		self.entity_type = args['entity_type']
		
		set = self.add('FieldSet', {
			'id' : 'newbundleset',
			'title' : s('Create new {entity_type} bundle', {'entity_type' : self.entity_type}),
			'css' : ['i-form-row i-margin-large']
		})

		set.add('TextBox', {
			'id' : 'entity_bundle_title',
			'value' : post.get('entity_bundle_title', ''),
			'title' : s('Bundle title'),
			'placeholder' : s('Bundle title'),
			'validation_rule' : ['Length', 2, '>', 0, 'The Bundle title length should be greater than 2!'],
			'css' : ['i-width-1-1 i-form-large'],
			'required' : True,
			'info' : s('Human readble display title.'),
			'weight' : 1,
		})
		
		set.add('TextBox', {
			'id' : 'entity_bundle',
			'value' : post.get('entity_bundle', ''),
			'title' : s('Bundle name'),
			'placeholder' : s('Bundle name'),
			'validation_rule' : ['Length', 2, '>', 0, 'The Bundle name length should be greater than 2!'],
			'css' : ['i-width-1-1 i-form-large'],
			'info' : s('Machine readable name.'),
			'required' : True,
			'weight' : 2,
		})
		set.add('CheckBox', {
			'label' : 'Default status published?',
			'id' : 'default_status',
			'value' : 1,	# returned value if checked
			'checked' : post.get('default_status', '') == '1',
			'info' : s('Default entity published status. Published if checked, otherwise not.'),
		})
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-grid']
		})

		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Create new bundle'),
			'css' : ['i-button i-button-primary']
		})
		
		self.css.append('ajax i-panel i-panel-box i-margin-large')

@IN.register('FormEntityAdminAddBundle', type = 'Former')
class FormEntityAdminAddBundle(FormFormer):

	def validate(self, form, post):

		if form.has_errors: # fields may have errors
			return

		entity_bundle = form['newbundleset']['entity_bundle'].value

		db = IN.db
		
		try:
			# if bundle already exists?
			cursor = db.select({
				'tables' : 'config.config_entity_bundle',
				'columns' : ['id'],
				'where' : [
					['entity_type', form.entity_type],
					['entity_bundle', entity_bundle],
				],
			}).execute()
				
			if cursor.rowcount > 0:
				form.error_message = s('Entity bundle name already exists! Please try another name!')
				form.has_errors = True
				return

		except Exception as e:
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again!')
			form.has_errors = True
			return

	def submit(self, form, post):

		if form.has_errors:
			return

		db = IN.db
		connection = db.connection
		entity_bundle = form['newbundleset']['entity_bundle'].value
		entity_bundle_title = form['newbundleset']['entity_bundle_title'].value
		
		try:
			
			default_status = 1 if form['newbundleset']['default_status'].checked else 0
			
			data = {
				'title' : entity_bundle_title,
				'default_status' : default_status,
			}
			
			data = json.dumps(data, skipkeys = True, ensure_ascii = False)
			
			values = [form.entity_type, entity_bundle, data]
			cursor = db.insert({
				'table' : 'config.config_entity_bundle',
				'columns' : ['entity_type', 'entity_bundle', 'data'],
			}).execute([values])

			connection.commit()
			
			form.redirect = form.entity_type.join(('admin/structure/entity/!', '/bundle'))
			
		except Exception as e:
			connection.rollback()
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again!')
			form.has_errors = True
			return

