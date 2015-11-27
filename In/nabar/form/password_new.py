
import datetime


class NabarNewPassword(Form):

	def __init__(self, data = None, items = None, post = None, **args):

		if data is None: data = {}
		if post is None: post = {}
		
		if 'id' not in data:
			data['id'] = 'NabarNewPassword'
		
		super().__init__(data, items, **args)
		
		nabar_id = self.args['nabar_id']
		if not nabar_id:
			return
		
		# validate nabar access here too
		
		entitier = IN.entitier
		context = IN.context
		
		nabar = entitier.load_single('Nabar', nabar_id)
		
		if not nabar:
			return
		
		logged_in_nabar_id = context.nabar.id
		
		if logged_in_nabar_id == nabar.id:
			if not context.access('nabar_edit_password_own', nabar, False):
				return
		else:
			if not context.access('nabar_edit_password_other', nabar, False):
				return
		
		
		set = self.add('FieldSet', {
			'id' : 'set',
			'title' : s('Nabar passwords'),
			'css' : ['i-form-row i-margin-large']
		})

		set.add('Password', {
			'id' : 'new_password',
			'value' : post.get('new_password', ''),
			'title' : s('New password'),
			'placeholder' : s('New password'),
			'validation_rule' : ['Length', 5, '>', 0, 'The password length should be greater than 5.'],
			'css' : ['i-width-1-1 i-form-large'],
			'required' : True,
		})

		set.add('Password', {
			'id' : 'confirm_password',
			'value' : post.get('confirm_password', ''),
			'title' : s('Confirm password'),
			'placeholder' : s('Confirm password'),
			'validation_rule' : ['Length', 5, '>', 0, 'The password length should be greater than 5.'],
			'css' : ['i-width-1-1 i-form-large'],
			'required' : True,
		})


		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-grid']
		})

		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Add password'),
			'css' : ['i-button i-button-danger']
		})
		
		set.add('TextDiv', {
			'value' : s('Cancel'),
			'css' : ['i-button'],
			'attributes' : {
				'onclick' : 'jQuery("#nabar-password-new-form").html("");'
			}
		})
		
		self.css.append('i-panel i-panel-box i-margin-large')

@IN.register('NabarNewPassword', type = 'Former')
class NabarNewPasswordFormer(FormFormer):

	def validate(self, form, post):

		if form.has_errors: # fields may have errors
			return
		
		nabar_id = form.args['nabar_id']
		
		set = form['set']
		
		new_password = set['new_password'].value
		confirm_password = set['confirm_password'].value
		
		if new_password != confirm_password:
			form.has_errors = True
			set['confirm_password'].has_errors = True
			set['confirm_password'].error_message = s('Confirm password does not match!')
			
			
		
	def submit(self, form, post):

		if form.has_errors:
			return

		nabar_id = form.args['nabar_id']
		if not nabar_id:
			return

		nabar_id = form.args['nabar_id']
		
		set = form['set']
		
		password = set['new_password'].value
		
		hash_id = None
		try:
			''''''
			hash_id = In.nabar.NabarHash({
				'id' : None,				# new password
				'nabar_id' : nabar_id,
				'hash' : IN.nabar.hasher.hash(password),
				'hint' : ''.join((password[0], '|', password[-1:])),
				'type' : '$S$',
				'created' : datetime.datetime.now(),
				'status' : 1, 				
			}).insert()			
			
		except Exception as e:
			IN.logger.debug()
			form.has_errors = True
			form.error_message = s('Unknown error occurred!')
		
		if hash_id:
			form.redirect = str(nabar_id).join(('/nabar/', '/edit/password'))
			
		
