

class FieldFormatterSelectionForm(Form):
	'''FieldFormatterSelectionForm

	'''

	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, **args)
		set = self.add('FieldSet', {
			'id' : 'configset',
			'title' : '',
			'css' : ['i-form-row i-margin-large']
		})
		
		fielder = IN.fielder
		
		display_config = fielder.field_display_config(args['entity_type'], args['entity_bundle'], args['view_mode'], args['field_name'])
		
		options = fielder.supported_field_formatters(self.args['field_type'])
		
		set.add('HTMLSelect', {
			'id' : 'field_formatter',
			'name' : 'field_formatter',
			'title' : s('Field formatter'),
			'options' : options,
			'required' :  True,
			'validation_rule' : [
				'Not', [['Empty', '']], 'The Field formatter class is required!'
			], 
			'value' : post.get('field_formatter', display_config.get('field_formatter', None)),
			'multiple' : False,
		})
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'title' : '',
			'css' : ['i-form-row i-margin-large']
		})

		set.add('Submit', {
			'value' : s('Continue'),
			'css' : ['i-button']
		})
		

@IN.register('FieldFormatterSelectionForm', type = 'Former')
class FieldFormatterSelectionFormFormer(FormFormer):
	'''FieldFormatterConfigForm Former'''

	def validate(self, form, post):
		
		if form.has_errors: # fields may have errors
			return
			
		field_formatter = form['configset']['field_formatter'].value
		
		f = IN.register.get_class(field_formatter, 'FieldFormatter')
		if f is None:
			form.has_errors = True
			form.error_message = s('Invalid field formatter class: {field_formatter}', {'field_formatter' : field_formatter})
			IN.logger.debug()
		

	def submit(self, form, post):
		'''Save the entity and return entity id'''

		if form.has_errors:
			return
			
		context = IN.context
		
		form.context_response_changed = True
		
		output = Object()
		context.response = In.core.response.PartialResponse(output = output)
		
		field_formatter = form['configset']['field_formatter'].value
		
		args = form.args
		
		field_type = args['field_type']
		field_name = args['field_name']
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_config = args['field_config']
		
		data = {
			'value' : {},
			'id' : field_name,
			'name' : field_name,
			'entity_type' : entity_type,
			'entity_id' : 0,
		}

		#field = Field.new(field_type, data = data)
		
		objclass = IN.fielder.formatter_class(field_formatter)
		

		config_form = objclass.FieldFormatterConfigForm
		
		args['field_formatter'] = field_formatter
		next_form = IN.former.load(config_form.__type__, args = args)
		
		element_id = '_'.join((entity_type, entity_bundle, field_name, 'field_formatter_config'))
		
		o = HTMLObject({
			'id' : element_id,
		})
		
		o.add(next_form)
		
		context.response.output[element_id] = o

