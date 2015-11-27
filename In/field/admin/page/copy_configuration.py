
def field_admin_action_entity_display_copy_configuration(context, action, entity_type, entity_bundle, view_mode = 'default', **args):

	IN.entitier.access('admin', entity_type, entity_bundle, deny = True)
	
	context = IN.context
	
	form_args = {
		'entity_type' : entity_type,
		'entity_bundle' : entity_bundle,
		'view_mode' : view_mode
	}
	
	form = IN.former.load('FormatterConfigCopierForm', args = form_args)
	
	if context.request.ajax_modal:
		
		element_id = 'i-ajax-modal'
		element_id = element_id + ' .modal-content'
		
		modal = Object.new(type="HTMLModalPopup", data = {
			'title' : s('Copy field display configuration!'),
		})
		modal.add(form)
		
		output = {
			element_id : modal,			
		}
		context.response = In.core.response.PartialResponse(output = output)
	else:
		context.response.output.add(form)
