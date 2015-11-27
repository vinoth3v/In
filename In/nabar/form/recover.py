

class FormRecover(Form):

	def __init__(self, data = None, items = None, post = None, **args):


		if data is None: data = {}
		if post is None: post = {}

		if 'id' not in data:
			data['id'] = 'FormRecover'

		# set always to 0,
		# after validation it may have value
		self.nabar_id = 0

		super().__init__(data, items, **args)

		set = self.add('FieldSet', {
			'id' : 'recoverset',
			'title' : s('Enter your account e-mail address!'),
			'css' : ['i-form-row']
		})

		#set.add('TextBox', {
			#'id' : 'loginname',
			#'value' : post.get('loginname', ''),
			#'title' : s('Login name'),
			#'placeholder' : s('Login name'),
			##'validation_rule' : ['Length', 6, '>', 0, 'The recovername length should be greater than 6.'],
			#'css' : ['i-width-1-1 i-form-large']
		#})


		#set.add('TextDiv', {
			#'id' : 'or1',
			#'value' : In.html.divider(s('Or')),
			#'css' : ['i-width-1-1 i-form-large']
		#})


		set.add('TextBoxEmail', {
			'id' : 'email',
			'value' : post.get('email', ''),
			'title' : s('E-mail address'),
			'placeholder' : s('E-mail address'),
			'validation_rule' : ['Email', 'Invalid E-mail address.'], # login name or email
			'css' : ['i-width-1-1 i-form-large']
		})

		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-grid']
		})

		set.add('Submit', {
			'id' : 'submit',
			'value' : s('send recovery e-mail!'),
			'css' : ['i-button i-button-primary i-button-large']
		})

		#set.add('CheckBox', {
			#'id' : 'rememberme',
			#'label' : s('Remember me'),
			#'value' : 'on',
			#'checked' : 'on' == post.get('rememberme', ''),
			#'css' : ['']
		#})

		#set = self.add('FieldSet', {
			#'id' : 'linkset',
			#'css' : ['i-form-row']
		#})

		#set.add('Link', {
			#'id' : 'register_link',
			#'href' : 'nabar/register',
			#'value' : '<i class="i-icon-magic"></i> ' + s('Register'),
			#'css' : ['ajax i-button']
		#})

		self.css.append('i-panel i-panel-box i-margin-large')

@IN.register('FormRecover', type = 'Former')
class FormRecoverFormer(FormFormer):

	def validate(self, form, post):

		if form.has_errors: # fields may have errors
			return

		email = form['recoverset']['email'].value.strip()
		
		logins = IN.entitier.select('NabarLogin', [
			['value', email], 
			['type', 'email'],
			['status', '>', 0],
		])
		
		if not logins:
			form.error_message = s('Sorry! Unknown error occurred! Please try again!')
			form.has_errors = True
			return
			
		for login_id, login in logins.items():
			
			# Check nabar status
			nabar = IN.entitier.load_single('Nabar', login.nabar_id)
			if not nabar:
				continue
			
			if nabar.status == IN.nabar.NABAR_STATUS_BLOCKED:
				form.error_message = s('Sorry! This account is Blocked! Please contact the site administrator!')
				form.has_errors = True
				return
			
			form.nabar_id = nabar.id
			form.email = email
			
			return
		
		
		form.error_message = s('Sorry! Unable to send the e-mail right now! Try again!')
		form.has_errors = True
		return


	def submit(self, form, post):

		if form.has_errors:
			return

		nabar_id = form.nabar_id
		if not nabar_id:
			return
		
		email = form.email
		
		# logs in the nabar
		try:
			IN.nabar.send_recovery_email(nabar_id, email)
			form.info += s('Recovery e-mail has been sent to this e-mail address!').join(('<div class="i-alert">', '</div>'))
		except Exception as e:
			form.info += s('Sorry! Unable to send the e-mail right now! Please Try again!').join(('<div class="i-alert i-danger">', '</div>'))

