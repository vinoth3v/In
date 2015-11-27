from .text import FieldText, FieldTextFielder


class FieldTextArea(FieldText):
	'''Text Area field'''
	__input_field_type__ = 'TextArea'
	
	
@IN.register('FieldTextArea', type = 'Fielder')
class FieldTextAreaFielder(FieldTextFielder):
	'''Base Field Fielder'''

	
	#field_type = 'Field'

	def get_input_field(self, type, id, name, value, weight, placeholder_text, field_config):
		'''helper method'''
		
		ckeditor = field_config.get('data', {}).get('field_config', {}).get('ckeditor_config', '')
		
		if ckeditor:
			ck_config = IN.APP.config.ckeditor[ckeditor]
			ckeditor = '''
	<script type="text/javascript">
	require(['jQuery', 'ckeditor-jquery', 'once'], function() {
		try {
			$('#''' + str(id) + '''').once('ckeditor').ckeditor(''' + ck_config+ ''');
		} catch(e) {};
	});
	</script>
			'''
			# TODO: ajax script include
			#IN.context.asset.add_js(ckeditor, 'ckeditor', 'inline')
		
		textfield = Object.new(type, {
			'id' : id,
			'name' : name,
			'value' : value,
			'placeholder' : placeholder_text,
			'css' : ['i-width-1-1 i-form-large'],
			'weight' : weight,
			'info' : ckeditor
		})
		
		if field_config['data'].get('field_config', {}).get('required', False):
			textfield.validation_rule = ['Not', [['Empty']], s('{name} is required!', {'name' : field_config['data']['title']})]
			
		return textfield
