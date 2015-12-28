from .text_select_config import FieldTextSelectConfigForm, FieldTextSelectConfigFormFormer

#********************************************************************
#					FieldNumberSelectConfig FORM
#********************************************************************	

@IN.register('FieldNumberSelect', type = 'FieldConfigForm')
class FieldNumberSelectConfigForm(FieldTextSelectConfigForm):
	'''FieldConfig Form'''


		
@IN.register('FieldNumberSelectConfigForm', type = 'Former')
class FieldNumberSelectConfigFormFormer(FieldTextSelectConfigFormFormer):
	'''EntityForm Former'''

	def validate(self, form, post):
		
		super().validate(form, post)
		
		
		if form.has_errors: # fields may have errors
			return
		
		
		field_selection_type = form['configset']['field_selection_type'].value
		field_value_options = form['configset']['field_value_options'].value
		
		values = {}
		keys = []
		
		field_value_options = field_value_options.split('\n')
		
		for vals in field_value_options:
			if not vals:
				continue
			val = vals.split(':', 1)
			if len(val) == 1:
				val = val[0].strip()
			else:
				val1 = val[0].strip()
			
			if not val1.isnumeric():
				form.has_errors = True
				
				form['configset']['field_value_options'].has_errors = True
				form['configset']['field_value_options'].error_message = s('Number field only supports numeric keys!')
				
