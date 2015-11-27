
def action_handler_stringer_admin_dev_i18n(context, action, **args):
	
	context.response.output.add('TextDiv', {
		'value' : str(IN.stringer.strings),
	})
