
class FormNabarRoleAddAdmin(Form):

	def __init__(self, data = None, items = None, post = None, **args):

		if data is None: data = {}
		if post is None: post = {}

		if 'id' not in data:
			data['id'] = 'FormNabarRoleAddAdmin'

		super().__init__(data, items, **args)

		set = self.add('FieldSet', {
			'id' : 'roleset',
			'title' : s('Add new role'),
			'css' : ['i-form-row i-margin-large']
		})

		set.add('TextBox', {
			'id' : 'name',
			'value' : post.get('name', ''),
			'title' : s('Role name'),
			'placeholder' : s('Role name'),
			'required' :  True,
			'validation_rule' : ['Length', 3, '>', 0, 'The name length should be greater than 3.'],
			'css' : ['i-width-1-1 i-form-large']
		})

		set.add('TextArea', {
			'id' : 'info',
			'value' : post.get('info', ''),
			'placeholder' : s('Small info about this role.'),
			'title' : s('Description'),
			'css' : ['i-width-1-1 i-form-large'],
			'rows' : 2
		})
		
		# weight
		set.add('HTMLSelect', {
			'id' : 'weight',
			'value' : post.get('weight', 0),
			'title' : s('Weight'),
			'options' : range(51),
			'required' : True,
			'css' : ['i-form-large'],
			'multiple' : False,
			'info' : s('The order that how role access will affect. Heavy weight will override low weight roles.'),
			'weight' : 3,
		})
		
		#set.add('TextDiv', {
			#'id' : 'terms',
			#'value' : s('''By registering to our site you are accepting our {term_link}.''', term_link = tlink),
			#'css' : ['i-text-primary']
		#})
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary']
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Create new nabar role'),
			'css' : ['i-button i-button-primary']
		})

		self.css.append('ajax i-panel i-panel-box i-margin-large')

@IN.register('FormNabarRoleAddAdmin', type = 'Former')
class FormNabarRoleAddAdminFormer(FormFormer):

	def validate(self, form, post):
		
		if form.has_errors: # fields may have errors
			return

		name = form['roleset']['name'].value
		
		if not name :
			form.error_message = s('Role name cannot be empty!')
			form.has_errors = True
			return False

		# email already exists

		try:
			cursor = IN.db.execute('''select r.id
				FROM account.role r
				where r.name = %(name)s''', {
				'name' : 'name',
			})
		except Exception as e:
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		if cursor.rowcount > 0:
			form['roleset']['email'].has_errors = True
			form['roleset']['email'].error_message = s('The role name already exists!')
			form.has_errors = True
			return False

		# register
		# email verification mail, save token to db
		auth = None

		# form.has_errors = False dont set, field validations may have errors

	def submit(self, form, post):

		if form.has_errors:
			return

		name = form['roleset']['name'].value.strip()
		info = form['roleset']['info'].value
		weight = int(form['roleset']['weight'].value)
		
		if not name:
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		try:
			cursor = IN.db.insert({
				'table' : 'account.role',
				'columns' : ['name', 'info', 'weight'],
				'returning' : 'id',
			}).execute([[name, info, weight]])

			if cursor.rowcount == 1:
				# update nabar role
				role_id = cursor.fetchone()[0]
				IN.nabar.roles[role_id] = {
					'id' : role_id,
					'name' : name,
					'weight' : weight,
					'info': info,
				}
			# commit
			IN.db.connection.commit()
			
		except Exception as e:
			connection.rollback()
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		form.redirect = '/admin/nabar/role'

