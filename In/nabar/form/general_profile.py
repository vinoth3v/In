#
# NOT USED
#

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
		
		set.add('RadioBoxes', {
			'id' : 'gender',
			'name' : 'gender',
			'title' : s('Gender'),
			'options' : options,
			'value' : post.get('gender', gender),
			'css' : ['i-width-1-1 i-form-large'],
		})

		set.add('DateSelect', {
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


	def submit(self, form, post):

		if form.has_errors:
			return

		nabar_id = form.args['nabar_id']
		if not nabar_id:
			return

		
