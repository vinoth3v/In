
def action_comment_edit_form(context, action, comment_id, **args):
	
	entitier = IN.entitier
	
	entity = entitier.load_single('Comment', int(comment_id))

	if not entity:
		context.not_found()
		
	try:
		
		entitier.access('edit', entity, deny = True)
		
		form = IN.commenter.get_comment_edit_form(entity)
		
		if context.request.ajax:
			element_id = '-'.join(('#comment', str(entity.id), 'children'))
			
			output = [{
				'method' : 'html',
				'args' : [element_id, IN.themer.theme(form)]
			}]
			context.response = In.core.response.CustomResponse(output = output)
			
		else:
			context.response.output.add(form)
			
	except:
		IN.logger.debug()