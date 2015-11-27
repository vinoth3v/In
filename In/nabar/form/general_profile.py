
import datetime
from collections import OrderedDict


class NabarGeneralProfileForm(Form):

	def __init__(self, data = None, items = None, post = None, **args):

		if data is None: data = {}
		if post is None: post = {}
		
		if 'id' not in data:
			data['id'] = 'NabarGeneralProfileForm'
		
		super().__init__(data, items, **args)
		
		nabar_id = self.args['nabar_id']
		
		# validate nabar access here too
		
		entitier = IN.entitier
		context = IN.context
		
		nabar = entitier.load_single('Nabar', nabar_id)
		
		if not nabar:
			return
		
		logged_in_nabar_id = context.nabar.id
		
		if logged_in_nabar_id == nabar.id:
			if not context.access('nabar_edit_own', nabar, False):
				return
		else:
			if not context.access('nabar_edit_other', nabar, False):
				return
		

		set = self.add('FieldSet', {
			'id' : 'set',
			'title' : s('General profile'),
			'css' : ['i-form-row i-margin-large']
		})

		set.add('TextBox', {
			'id' : 'nabar_name',
			'value' : post.get('nabar_name', nabar.name),
			'title' : s('Full name'),
			'placeholder' : s('First & Last name'),
			'css' : ['i-width-1-1 i-form-large'],
			'required' : True,
		})
		
		options = OrderedDict()
		options['male'] = s('Male')
		options['female'] = s('Female')
		options['shemale'] = s('Shemale')
		
		gender = {0 : 'female', 1 : 'male', 2 :'shemale'}[nabar.gender] 
		
		set.add('RadioBoxes',{
			'id' : 'gender',
			'name' : 'gender',
			'title' : s('Gender'),
			'options' : options,
			'value' : post.get('gender', gender),
			'css' : ['i-width-1-1 i-form-large'],
		})

		set.add('DateSelect',{
			'id' : 'dob',
			'name' : 'dob',
			'options' : options,
			'title' : s('Date of birth'),
			'value' : post.get('dob', nabar.dob),
			'required' : True,
			'validation_rule' : ['Equal', datetime.date.today() - datetime.timedelta(days = 13*365), '<', 0, 'The Age should be greater than 13 years.'],
			'css' : ['i-width-1-1 i-form-large'],
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
		
		
		self.css.append('i-panel i-panel-box i-margin-large')

@IN.register('NabarGeneralProfileForm', type = 'Former')
class NabarGeneralProfileFormFormer(FormFormer):

	#def validate(self, form, post):

		#if form.has_errors: # fields may have errors
			#return
		
		#nabar_id = form.args['nabar_id']
		#hash_id = form.args['hash_id']
		
		#set = form['set']
		
		#current_password = set['current_password'].value
		#new_password = set['new_password'].value
		#confirm_password = set['confirm_password'].value
		
		#if new_password != confirm_password:
			#form.has_errors = True
			#set['confirm_password'].has_errors = True
			#set['confirm_password'].error_message = s('Confirm password does not match!')
			#return
			
		#try:
			
			## password auth
			#hashes = IN.entitier.select('NabarHash', [
				#['nabar_id', nabar_id], 
				#['id', hash_id], 
			#])

			#if not hashes: # None or empty
				#form.has_errors = True
				#set['current_password'].has_errors = True
				#set['current_password'].error_message = s('Unknown error occurred!')
				#return
				
			#for hid, hash in hashes.items():
				
				#form.processed_data['hash'] = hash
				
				#old_hash = hash.hash
				#new_hash = IN.nabar.hasher.password_crypt('sha512', current_password, old_hash)
				#if old_hash != new_hash: # success
					#form.has_errors = True
					#set['current_password'].has_errors = True
					#set['current_password'].error_message = s('Current password does not match!')
		#except Exception as e:
			#IN.logger.debug()
			#form.has_errors = True
			#set['current_password'].has_errors = True
			#set['current_password'].error_message = s('Unknown error occurred!')


	def submit(self, form, post):

		if form.has_errors:
			return

		nabar_id = form.args['nabar_id']
		if not nabar_id:
			return

		
		#nabar_id = form.args['nabar_id']
		#hash_id = form.args['hash_id']
		
		#set = form['set']
		
		#current_password = set['current_password'].value
		#new_password = set['new_password'].value
		#confirm_password = set['confirm_password'].value
		
		#try:
			#hash = form.processed_data['hash']
			
			#old_hash = hash.hash
			#new_hash = IN.nabar.hasher.hash(new_password)
			
			## set new hash
			#hash.hash = new_hash
			
			## set new hint
			#hash.hint = ''.join((new_password[0], '|', new_password[-1:]))
			
			#hash.save()
			
			#form.result_commands = []
		
			#form.result_commands.append({
				#'method' : 'notify',
				#'args' : [{
					#'message' : s('Password updated successfully!'),
					#'status'  : 'info',
					#'timeout' : 5000,
					#'pos'     : 'bottom-left'			
				#}]
			#})
			
			#hashints = hash.hint.split('|')
		
			#if len(hashints) == 2:
				#hashints = '******'.join((hashints[0], hashints[1]))
			#else:
				#hashints = '********'
			
			
			#form.result_commands.append({
				#'method' : 'html',
				#'args' : ['#nabar-password-edit-' + str(hash.id), hashints]
			#})
			
		#except Exception as e:
			#IN.logger.debug()
			#form.has_errors = True
			#form.error_message = s('Unknown error occurred!')
