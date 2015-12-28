
def action_image_browse_form(context, action, **args):
	
	try:
		
		post = context.request.args['post']
		
		ajax_args = post.get('ajax_args', {})
		
		form_args = {
			'ajax_args' : ajax_args,
		}
		
		form = IN.former.load('FormImageBrowser', args = form_args)
		
		if context.request.ajax_modal:
			
			element_id = ajax_args.get('modal_id', 'i-ajax-modal')
			element_id = element_id + ' .modal-content'
			
			modal = Object.new('HTMLModalPopup', {
				'title' : s('Select Image!'),
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