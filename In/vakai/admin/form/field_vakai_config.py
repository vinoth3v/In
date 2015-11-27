from collections import OrderedDict

from In.field.admin.form import FieldConfigForm, FieldConfigFormFormer

#********************************************************************
#					FieldVakaiConfig FORM
#********************************************************************	

@IN.register('FieldVakai', type = 'FieldConfigForm')
class FieldVakaiConfigForm(FieldConfigForm):
	'''FieldConfig Form'''

	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)

		config = self.config
		config_data = config['data']
		field_config = config_data.get('field_config', {})
		
		set = self['configset']
		
		
		options = OrderedDict()
		
		options['autocomplete'] = s('Auto complete')
		options['select'] = s('Select list')
		options['checkboxes'] = s('Check boxes')
		options['radioboxes'] = s('Radio boxes')
		
		# max limit
		set.add('HTMLSelect', {
			'id' : 'field_selection_type',
			'value' : post.get('field_selection_type', None) or field_config.get('field_selection_type', None),
			'title' : s('Field selection type'),
			'options' : options,
			'required' : True,
			'css' : ['i-form-large'],
			'multiple' : False,
			'weight' : 1,
		})
		
		entitier = IN.entitier
		
		options = entitier.entity_bundle['Vakai'].keys()
		
		
		# max limit
		set.add('HTMLSelect', {
			'id' : 'vakai_bundle',
			'value' : post.get('vakai_bundle', None) or field_config.get('vakai_bundle', None),
			'title' : s('Allowed Vakai Bundle'),
			'options' : options,
			'required' : True,
			'css' : ['i-form-large'],
			'multiple' : False,
			'info' : s('Allowed vakai bundle in this field.'),
			'weight' : 2,
		})
		
@IN.register('FieldVakaiConfigForm', type = 'Former')
class FieldVakaiConfigFormFormer(FieldConfigFormFormer):
	'''EntityForm Former'''

	def validate(self, form, post):
		
		if form.has_errors: # fields may have errors
			return
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		
		if form.has_errors:
			return
		
		vakai_bundle = form['configset']['vakai_bundle'].value
		field_selection_type = form['configset']['field_selection_type'].value
		
		config_data = form.processed_data['config_data']
		field_config = config_data['field_config']
		
		field_config['vakai_bundle'] = vakai_bundle
		field_config['field_selection_type'] = field_selection_type
