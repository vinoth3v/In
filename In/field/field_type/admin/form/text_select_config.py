from collections import OrderedDict
from In.field.admin.form import FieldConfigForm, FieldConfigFormFormer

#********************************************************************
#					FieldTextSelectConfig FORM
#********************************************************************	

@IN.register('FieldTextSelect', type = 'FieldConfigForm')
class FieldTextSelectConfigForm(FieldConfigForm):
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
		
		field_value_options = post.get('field_value_options', None)
		if field_value_options is None:
			keys = field_config.get('field_value_option_keys', [])
			values = field_config.get('field_value_option_values', {})
			options = []
			for key in keys:
				if key in values:
					options.append(':'.join((str(key), values[key])))
			field_value_options = '\n'.join(options)
		
		set.add('TextArea', {
			'id' : 'field_value_options',
			'value' : field_value_options,
			'title' : s('Field allowed values'),
			'required' : True,
			'css' : ['i-form-large i-width-1-1'],
			'multiple' : False,
			'weight' : 2,
			'info' : s('''Colon separated key:value pair of allowed values, one per line. Key should be a number.
example:<br>
0:Female<br>
1:Male<br>
2:Shemale<br>
'''),
			'validation_rule' : ['Not', [['Empty']], 'Values field is required']
		})
		
@IN.register('FieldTextSelectConfigForm', type = 'Former')
class FieldTextSelectConfigFormFormer(FieldConfigFormFormer):
	'''EntityForm Former'''

	def validate(self, form, post):
		
		if form.has_errors: # fields may have errors
			return
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		
		if form.has_errors:
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
				values[val] = val
				keys.append(val)
			else:
				val1 = val[0].strip()
				val2 = val[1].strip()
				values[val1] = val2
				keys.append(val1)

		config_data = form.processed_data['config_data']
		field_config = config_data['field_config']
		
		field_config['field_selection_type'] = field_selection_type
		
		# to keep order
		field_config['field_value_option_keys'] = keys
		field_config['field_value_option_values'] = values
		
