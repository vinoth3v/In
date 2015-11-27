
def action_comment_delete_form(context, action, comment_id, **args):
	
	entity = IN.entitier.load_single('Comment', int(comment_id))

	if not entity:
		context.not_found()
		
	try:
		
		form = IN.commenter.get_comment_delete_form(entity)
		
		if context.request.ajax_modal:
			
			element_id = 'i-ajax-modal'
			element_id = element_id + ' .modal-content'
			
			modal = Object.new(type="HTMLModalPopup", data = {
				'title' : s('Delete!'),
			})
			modal.add(form)
			
			output = {
				element_id : modal,			
			}
			context.response = In.core.response.PartialResponse(output = output)
		else:
			context.response.output.add(form)
			
	except:
		IN.logger.debug()