import json
import datetime



class FormLogin(Form):

	def __init__(self, data = None, items = None, post = None, **args):


		if data is None: data = {}
		if post is None: post = {}

		if 'id' not in data:
			data['id'] = 'FormLogin'

		# set always to 0,
		# after validation it may have value
		self.nabar_id = 0

		super().__init__(data, items, **args)

		set = self.add('FieldSet', {
			'id' : 'loginset',
			'css' : ['i-form-row i-margin-large']
		})

		set.add('TextBox', {
			'id' : 'loginname',
			'value' : post.get('loginname', ''),
			'title' : s('Login name or E-mail address'),
			'placeholder' : s('Login name or e-mail'),
			#'validation_rule' : ['Length', 6, '>', 0, 'The loginname length should be greater than 6.'],
			'css' : ['i-width-1-1 i-form-large'],
			'required' : True,
		})
		set.add('Password', {
			'id' : 'password',
			'value' : post.get('password', ''),
			'title' : s('Password'),
			'placeholder' : s('Password'),
			#'validation_rule' : ['Length', 6, '>', 0, 'The password length should be greater than 6.'],
			'css' : ['i-width-1-1 i-form-large'],
			'required' : True,
		})



		if 'resend' in post:
		
			set = self.add('FieldSet', {
				'id' : 'resendset',
				'css' : ['i-form-row'],
				'weight' : -10,
			})
			resend = set.add('Button', {
				'id' : 'resend',
				'value' : s('Resend verification Link!'),
				'css' : ['ajax i-button i-button-success i-button-large'],
				'attributes' : {
					'data-ajax_partial' : 1
				}
			})
		
			self.ajax_elements.append('resend')
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-grid']
		})

		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Login'),
			'css' : ['i-button i-button-primary i-button-large']
		})

		set.add('CheckBox', {
			'id' : 'rememberme',
			'label' : s('Remember me'),
			'value' : 'on',
			'checked' : 'on' == post.get('rememberme', ''),
			'css' : ['']
		})

		set = self.add('FieldSet', {
			'id' : 'linkset',
			'css' : ['i-form-row']
		})

		set.add('Link', {
			'id' : 'register_link',
			'href' : '/nabar/register',
			'value' : '<i class="i-icon-magic"></i> ' + s('Register'),
			'css' : ['i-button']
		})

		set.add('Link', {
			'id' : 'forget_link',
			'href' : '/nabar/recover',
			'value' : '<i class="i-icon-key"></i> ' + s('Can\'t login? Forgot password?'),
			'css' : ['i-button']
		})

		self.css.append('i-panel i-panel-box i-margin-large')

@IN.register('FormLogin', type = 'Former')
class FormLoginFormer(FormFormer):

	def validate_partial(self, form, post):
		'''validate resend'''
		
		
	def validate(self, form, post):
		
		if form.has_errors: # fields may have errors
			return
		
		loginname = form['loginset']['loginname'].value
		password = form['loginset']['password'].value
		
		logins = IN.entitier.select('NabarLogin', [['value', loginname]])
		
		if not logins:
			form.error_message = s('Login name and/or password are incorrect! Please try again!')
			form.has_errors = True
			return
		
		for login_id, login in logins.items():
			pwd_hash = IN.nabar.match_password(login.nabar_id, password)
			if pwd_hash:
				# login, pass match
				
				# Check nabar status
				nabar = IN.entitier.load_single('Nabar', login.nabar_id)
		
				if nabar:
					
					# active
					if nabar.status >= 1 and login.status >= 1 and pwd_hash.status >= 1:
						# set the nabar id
						form.nabar_id = nabar.id
						return
					
					# BLOCKED
					if nabar.status == IN.nabar.NABAR_STATUS_BLOCKED:
						form.error_message = s('Sorry! This account has been blocked! Please contact the site administrator!')
						form.has_errors = True
						return
					
					# just registered
					if nabar.status == IN.nabar.NABAR_STATUS_REGISTERED:
						form.error_message = s('This account has registered but not verified yet!')
						form.has_errors = True
						
						set = form.add('FieldSet', {
							'id' : 'resendset',
							'css' : ['i-form-row'],
							'weight' : -10,
						})
						resend = set.add('Button', {
							'id' : 'resend',
							'value' : s('Resend verification Link!'),
							'css' : ['ajax i-button i-button-success i-button-large'],
							'attributes' : {
								'data-ajax_partial' : 1
							}
						})
						form.ajax_elements.append('resend')
						return
			
		form.error_message = s('Login name and/or password are incorrect! Please try again!')
		form.has_errors = True
		return
		
	
	def submit_partial(self, form, post):
		'''re send verification link'''
		
		
		if form.has_errors: # fields may have errors
			return
			
		if post['element_id'] == 'resend':
			
			try:
				
				loginname = form['loginset']['loginname'].value
				password = form['loginset']['password'].value
		
				logins = IN.entitier.select('NabarLogin', [['value', loginname]])
				
				if not logins:
					return
				
				for login_id, login in logins.items():
					pwd_hash = IN.nabar.match_password(login.nabar_id, password)
					if not pwd_hash:
						return
					
					# login, pass match
						
					# Check nabar status
					nabar = IN.entitier.load_single('Nabar', login.nabar_id)
					
					if not nabar:
						return
						
					# just registered
					if nabar.status != IN.nabar.NABAR_STATUS_REGISTERED:
						return
					
					
					connection = IN.db.connection
					
					token = In.core.token_verification.create_random_token()
					
					email = nabar.email_address
					
					# token data
					data = {
						'nabar_id' : nabar.id,
						'email' : email,
					}
					
					data = json.dumps(data, skipkeys = True, ensure_ascii = False)
					now = datetime.datetime.now()

					cursor = IN.db.execute('''INSERT INTO log.token
							(token, type, created, expire, data)
					VALUES  (%(token)s, %(type)s, %(created)s, %(expire)s, %(data)s)''', {
						'token' : token,
						'type' : 'register',
						'created' : now,
						'expire' : now + datetime.timedelta(days = 30), # nabar register token, 1 month
						'data' : data,
					})
					
					# commit the changes
					connection.commit()
					
					# send mail
					
					EMail.new('WelcomeEmailVerification', {
						'title' : s('Verify your email!'),
						'to_name' : nabar.name,
						'to_address' : email,
						'mail_verify_token' : token,
					}).send()
					
					form.has_errors = False
					form['resendset'].add('TextDiv', {
						'id' : 'resend',
						'value' : '<div class="i-alert">' + s('E-mail verification link has been sent to your registered email address!') + '</div>'
					})
					return
					
			except Exception as e:
				IN.logger.debug()
				connection.rollback()
				
	def submit(self, form, post):

		if form.has_errors:
			return

		nabar_id = form.nabar_id
		if not nabar_id:
			return

		rememberme = form['actionset']['rememberme'].value == post.get('rememberme', False)

		# logs in the nabar
		IN.nabar.login(nabar_id, rememberme)

		form.redirect = '/nabar/home'
		form.ajax_redirect = False # non ajax redirect on login forms

