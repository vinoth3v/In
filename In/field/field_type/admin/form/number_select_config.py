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

	
