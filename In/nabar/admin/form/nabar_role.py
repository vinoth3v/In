
class FormNabarRoleAdmin(Form):

	def __init__(self, data = None, items = None, post = None, **args):

		if data is None: data = {}
		if post is None: post = {}

		if 'id' not in data:
			data['id'] = 'FormNabarRoleAdmin'

		
		super().__init__(data, items, **args)

		set = self.add('FieldSet', {
			'id' : 'set',
			'css' : ['i-form-row i-margin-large']
		})
		
		table = set.add('HTMLTable')
		
		roles = IN.nabar.roles
		for rid, role in roles.items():

			row = table['body'].add('HTMLTableRow')
			row.add('HTMLTableColumn', {
				'value' : role['name'],
				'weight' : 1,
			})
			
			row.add('HTMLTableColumn', {
				'value' : role['info'],
				'weight' : 2,
			})
			
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary']
		})
		
		#set.add('Submit', {
			#'id' : 'submit',
			#'value' : s('Register new account'),
			#'css' : ['i-button i-button-primary i-button-large']
		#})

		
		self.css.append('i-panel i-panel-box i-margin-large')

@IN.register('FormNabarRoleAdmin', type = 'Former')
class FormNabarRoleAdminFormer(FormFormer):

	def validate(self, form, post):
		
		if form.has_errors: # fields may have errors
			return

		
		
	def submit(self, form, post):

		if form.has_errors:
			return

		
