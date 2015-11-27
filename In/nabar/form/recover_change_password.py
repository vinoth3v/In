
import datetime


class RecoverChangePassword(Form):

	def __init__(self, data = None, items = None, post = None, **args):

		if data is None: data = {}
		if post is None: post = {}
		
		if 'id' not in data:
			data['id'] = 'RecoverChangePassword'
		
		super().__init__(data, items, **args)
		
		nabar_id = self.args['nabar_id']		
		email_token = self.args['email_token']
		email = self.args['email']
		
		if not nabar_id or not email_token or not email:
			return
		
		# token valid?
		token_data = In.core.token_verification.token_valid(email_token, 'recovery')
		
		if not token_data:
			IN.context.bad_request()
			return
		
		if token_data['nabar_id'] != nabar_id or token_data['email'] != email:
			IN.context.bad_request()
			return
		
		# validate nabar access here too
		
		entitier = IN.entitier
		context = IN.context
		
		nabar = entitier.load_single('Nabar', nabar_id)
		
		if not nabar:
			return
		
		# nabar is not active yet
		if nabar.status == IN.nabar.NABAR_STATUS_REGISTERED:
			return
		
		# nabar blocked
		if nabar.status == IN.nabar.NABAR_STATUS_BLOCKED:
			return
		
		if not context.access('nabar_edit_password_own', nabar, False):
			return
		
		try:
			
			# check email should be active
			cursor = IN.db.execute('''select l.nabar_id
				FROM account.login l
				JOIN account.nabar a ON l.nabar_id = a.id
				where l.value = %(email)s AND
					l.type = %(type)s AND
					l.status >= 1 AND 
					a.status >= 1 AND
					a.nabar_id = %(nabar_id)s''', {
				'email' : email,
				'type' : 'email',
				'nabar_id' : nabar_id,
			})
			if cursor.rowcount == 0:
				return
			
		except Exception as e:
			IN.logger.debug()
			self.has_errors = True
			self.error_message = s('Unknown error occurred!')
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
			'value' : s('Set password'),
			'css' : ['i-button i-button-danger']
		})
		
		
		self.css.append('i-panel i-panel-box i-margin-large')

@IN.register('RecoverChangePassword', type = 'Former')
class RecoverChangePasswordFormer(FormFormer):

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
		email_token = form.args['email_token']
		email = form.args['email']
		
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
			
			form.info = s('New password has been set! You can now login into the site!').join(('<div class="i-alert">', '</div>'))
			
			form['set'].visible = False
			form['actionset']['submit'].visible = False
			
			form['actionset'].add('Link', {
				'id' : 'login',
				'value' : s('Login'),
				'href' : '/nabar/login',
				'css' : ['i-button i-button-primary']
			})
			
			# invalidate the email token
			IN.db.execute('''Delete 
				FROM
				log.token l
				WHERE 
				l.token = %(token)s AND
				l.type = %(type)s
				''', {
				'token' : email_token,
				'type' : 'recovery',
			})
			
			IN.db.connection.commit()
			
		except Exception as e:
			IN.db.connection.rollback()
			
			IN.logger.debug()			
			
			form.has_errors = True
			form.error_message = s('Unknown error occurred!')
		
			
		
