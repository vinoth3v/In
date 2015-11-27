from collections import OrderedDict
from In.field.admin.form.field_config import FieldConfigForm, FieldConfigFormFormer

@IN.register('FieldEntityReference', type = 'FieldConfigForm')
class FieldEntityReferenceFieldConfigForm(FieldConfigForm):
	'''FieldEntityReferenceFieldConfigForm'''

	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_name = args['field_name']
		
		config = self.config
		config_data = config['data']
		field_config = config_data.get('field_config', {})
		
		set = self['configset']
		
		options = IN.entitier.entity_bundle.keys()
		
		field_entity_type = post.get('entity_type', None) or field_config.get('entity_type', None)
		
		# always display value to make sure bundle displays the correct values
		if not field_entity_type:
			field_entity_type = list(options)[0]
			
		
		set.add('HTMLSelect', {
			'id' : 'entity_type',
			'value' : field_entity_type,
			'title' : s('Entity type'),
			'options' : options,
			'required' : True,
			'css' : ['ajax i-width-1-1 i-form-large'],
			'multiple' : False,
			'info' : s('The type of entity this field may reference to.'),
			'validation_rule' : [
				['Not', [['Empty', '']], s('Entity type is required!')]
			],
			'attributes' : {'data-ajax_partial' : 1},
			'weight' : 5,
		})
		
		options = OrderedDict()
		options['*'] = s('Any bundle')
		
		if field_entity_type is not None:
			# get bundles
			for bundle in IN.entitier.entity_bundle[field_entity_type].keys():
				options[bundle] = bundle
		
		bundle_element = set.add('CheckBoxes', {
			'id' : 'entity_bundle',
			'value' : post.get('entity_bundle', None) or field_config.get('entity_bundle', None),
			'title' : s('Entity bundle'),
			'options' : options,
			'required' : False,
			'css' : ['i-width-1-1 i-form-large'],
			'info' : s('Allow only these bundles.'),
			'validation_rule' : [
				['Not', [['Empty', '']], s('Entity bundle is required!')]
			],
			'weight' : 6,
		})
		
		self.ajax_elements.append('entity_bundle')
		
@IN.register('FieldEntityReferenceFieldConfigForm', type = 'Former')
class FieldEntityReferenceFieldConfigFormFormer(FieldConfigFormFormer):
	'''FieldEntityReferenceFieldConfigForm Former'''
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		fielder = IN.fielder
		
		args = form.args
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_name = args['field_name']
		
		# get config data from DB. local cache is old
		config_data = form.processed_data['config_data']
		
		field_config = config_data.get('field_config', {})
		
		field_config['entity_type'] = form['configset']['entity_type'].value
		field_config['entity_bundle'] = form['configset']['entity_bundle'].value
		
		
