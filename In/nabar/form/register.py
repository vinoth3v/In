
import datetime
from collections import OrderedDict


class FormRegister(Form):

	def __init__(self, data = None, items = None, post = None, **args):

		if data is None: data = {}
		if post is None: post = {}

		if 'id' not in data:
			data['id'] = 'FormRegister'

		# set always to 0,
		# after validation it may have value
		self.nabar_id = 0

		super().__init__(data, items, **args)

		set = self.add('FieldSet',{
			'id' : 'registerset',
			'css' : ['i-form-row i-margin-large']
		})

		set.add('TextBox',{
			'id' : 'name',
			'value' : post.get('name', ''),
			'title' : s('Your name'),
			'placeholder' : s('Your name'),
			'required' :  True,
			'validation_rule' : ['Length', 3, '>', 0, 'The name length should be greater than 3.'],
			'css' : ['i-width-1-1 i-form-large']
		})
		set.add('TextBoxEmail',{
			'id' : 'email',
			'value' : post.get('email', ''),
			'title' : s('E-mail address'),
			'placeholder' : s('E-mail address'),
			'required' :  True,
			'validation_rule' : ['Email', 'Invalid E-mail address.'],
			'css' : ['i-width-1-1 i-form-large']
		})

		#set.add('TextBox',{
			#'id' : 'nabarname',
			#'value' : post.get('nabarname', ''),
			#'title' : s('Login name'),
			#'placeholder' : s('Login name'),
			#'validation_rule' : ['Length', 5, '>', 0, 'The loginname length should be greater than 5.'],
			#'css' : ['i-width-1-1 i-form-large']
		#})
		pwd = post.get('password', '')
		repwd = post.get('repassword', '')

		set.add('Password',{
			'id' : 'password',
			'value' : pwd,
			'title' : s('Password'),
			'placeholder' : s('Password'),
			'validation_rule' : ['Length', 5, '>', 0, 'The password length should be greater than 5!'],
			'css' : ['i-width-1-1 i-form-large'],
		})

		set.add('Password',{
			'id' : 'repassword',
			'value' : repwd,
			'title' : s('Retype password'),
			'placeholder' : s('Retype password'),
			'validation_rule' : ['Equal', pwd,  '=', 0, 'Two passwords must match!'],
			'css' : ['i-width-1-1 i-form-large'],
		})

		options = OrderedDict()
		options['male'] = s('Male')
		options['female'] = s('Female')
		options['shemale'] = s('Shemale')

		set.add('RadioBoxes',{
			'id' : 'gender',
			'name' : 'gender',
			'title' : s('Gender'),
			'options' : options,
			'value' : post.get('gender', 'female'),
			'css' : ['i-width-1-1 i-form-large'],
		})

		#options = OrderedDict()
		set.add('DateSelect',{
			'id' : 'dob',
			'name' : 'dob',
			'options' : options,
			'title' : s('Date of birth'),
			'value' : post.get('dob', None),
			'required' : True,
			'validation_rule' : ['Equal', datetime.date.today() - datetime.timedelta(days = 13*365), '<', 0, 'The Age should be greater than 13 years.'],
			'css' : ['i-width-1-1 i-form-large'],
		})

		set = self.add('FieldSet',{
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary']
		})
		tpath = IN.APP.config.paths['term_condition']
		tlink = ''.join(('<a target="_blank" href="/', tpath, '">', s('Terms & Conditions'), '</a>'))
		set.add('TextDiv',{
			'id' : 'terms',
			'value' : s('''By registering to our site you are accepting our {term_link}.''', {'term_link' : tlink}),
			'css' : ['i-text-primary']
		})

		set.add('Submit',{
			'id' : 'submit',
			'value' : s('Register new account'),
			'css' : ['i-button i-button-primary i-button-large']
		})

		#set.add('CheckBox',{
			#'id' : 'accept',
			#'label' : s('I Accept Terms & Conditions'),
			#'value' : 'on',
			#'checked' : 'on' == post.get('accept', ''),
			#'css' : ['']
		#})

		set = self.add('FieldSet',{
			'id' : 'linkset',
			'css' : ['i-form-row']
		})

		#set.add('Link',{
			#'id' : 'login_link',
			#'href' : 'nabar/login',
			#'value' : '<i class="i-icon-magic"></i> ' + s('Login'),
			#'css' : ['ajax i-button']
		#})

		self.css.append('i-panel i-panel-box i-margin-large')

@IN.register('FormRegister', type = 'Former')
class FormRegisterFormer(FormFormer):

	def validate(self, form, post):
		
		if form.has_errors: # fields may have errors
			return

		name = form['registerset']['name'].value.strip()
		#loginname = form['registerset']['loginname'].value
		email = form['registerset']['email'].value.strip()
		gender = form['registerset']['gender'].value
		password = form['registerset']['password'].value
		dob = form['registerset']['dob'].value

		if not name or not email or not gender or not password or not dob:
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		# TODO: make it as Valuator?

		# email already exists

		try:
			cursor = IN.db.execute('''select l.nabar_id
				FROM account.login l
				JOIN account.nabar a ON l.nabar_id = a.id
				where l.type = %(type)s and l.value = %(email)s AND
				l.status > 0 and a.status > 0 LIMIT 1''', {
				'type' : 'email',
				'email' : email,
			})
		except Exception as e:
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		if cursor.rowcount > 0:
			form['registerset']['email'].has_errors = True
			form['registerset']['email'].error_message = s('Someone already having account with this E-mail address!')
			form.has_errors = True
			return False

		# register
		# email verification mail, save token to db
		auth = None

		# form.has_errors = False dont set, field validations may have errors

	def submit(self, form, post):

		if form.has_errors:
			return

		name = form['registerset']['name'].value
		email = form['registerset']['email'].value
		gender = form['registerset']['gender'].value
		password = form['registerset']['password'].value
		dob = form['registerset']['dob'].value

		if not name or not email or not gender or not password or not dob:
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		nabar = None
		try:
			nabar = IN.nabar.register(email, password, name, gender, dob, None)
			form.info = form.info or ''
			form.info = form.info + s('''<div class="i-alert i-alert-success i-alert-large"><h2>Your account has been created!</h2> 
			<h3>Please check your e-mail for verification link!</h3></div>''')
			
		except Exception as e:
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		if not nabar:
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		# TODO: display error message
		form.redirect = None # non ajax redirect on register forms

