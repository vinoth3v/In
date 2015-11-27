#-----------------------------------------------------------------------
#						FormatterConfigCopier
#-----------------------------------------------------------------------

class FormatterConfigCopierForm(Form):
	'''FormatterConfigCopier

	'''

	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, **args)
		set = self.add('FieldSet', {
			'id' : 'configset',
			'title' : '',
			'css' : ['i-form-row i-margin-large']
		})
		
		fielder = IN.fielder
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		view_mode = args['view_mode']
		
		entity_class = Entity.entity_class(entity_type, entity_bundle)
		view_modes =  entity_class.Entitier.view_modes()
		
		# remove current from modes
		if view_mode in view_modes:
			view_modes.remove(view_mode)
		
		set.add('HTMLSelect', {
			'id' : 'view_mode',
			'title' : s('Copy configuration from view mode'),
			'options' : view_modes,
			'required' :  True,
			'validation_rule' : [
				'Not', [['Empty', '']], 'The view mode is required!'
			],
			'value' : post.get('view_mode', None),
			'multiple' : False,
		})
		
		set.add('TextDiv', {
			'value' : s('Copy to view mode <b>{view_mode}</b>', {'view_mode' : view_mode}),
		})
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'title' : '',
			'css' : ['i-form-row i-margin-large']
		})

		set.add('Submit', {
			'value' : s('Copy configuration'),
			'css' : ['i-button i-button-primary']
		})

@IN.register('FormatterConfigCopierForm', type = 'Former')
class FormatterConfigCopierFormFormer(FormFormer):
	'''FormatterConfigCopierForm Former'''

	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
	
	def submit(self, form, post):
		'''Save the entity and return entity id'''

		if form.has_errors:
			return
		
		# custom commands
		form.result_commands = []
		
		args = form.args
				
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		view_mode = args['view_mode']
		from_view_mode = form['configset']['view_mode'].value
		
		fielder = IN.fielder
		
		if entity_bundle not in fielder.entity_field_config[entity_type]:
			
			form.result_commands.append({
				'method' : 'notify',
				'args' : [{
					'message' : s('No fields found on this bundle!'),
					'status'  : 'warning',
					'timeout' : 5000,
					'pos'     : 'bottom-left',
				}]
			})
			
			return
			
			
		for field_name in fielder.entity_field_config[entity_type][entity_bundle].keys():
			display_config = fielder.field_display_config(entity_type, entity_bundle, from_view_mode, field_name)
			
			config = {
				'field_formatter' : display_config.get('field_formatter', ''),
				'field_formatter_config' : display_config.get('field_formatter_config', {}),
			}
			
			try:
				fielder.set_field_formatter_config(entity_type, entity_bundle, view_mode, field_name, config)
			except Exception as e:
				IN.logger.debug()
				form.has_errors = True
				form.error_message = ' '.join((s('Error while copying configuration!'), str(e)))
				return
	
		form.result_commands.append({
			'method' : 'closeAjaxModal',
			'args' : [],
		})
		
		form.result_commands.append({
			'method' : 'notify',
			'args' : [{
				'message' : s('Configuration copied!'),
				'status'  : 'info',
				'timeout' : 5000,
				'pos'     : 'bottom-left',
			}]
		})

