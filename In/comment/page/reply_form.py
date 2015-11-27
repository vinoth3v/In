def action_comment_reply_form(context, action, entity_type, entity_id, parent_id, container_id, **args):
	
	entity = IN.entitier.load_single(entity_type, int(entity_id))

	if not entity:
		return
		
	try:
		
		form = IN.commenter.get_comment_add_form(entity, parent_id)

		element_id = str(parent_id).join(('#Comment_', '-ajax-comment-form'))
		reply_id = '#repli-link-Comment-' + str(parent_id)
		#output = {
			#element_id : form,
			#reply_id : '',  # empty
			
		#}
		output = [
			{'method' : 'html', 'args' : [element_id, IN.themer.theme(form)]},
			{'method' : 'remove', 'args' : [reply_id]},
			{'method' : 'focus', 'args' : [element_id + ' form textarea']},
		]
		context.response = In.core.response.CustomResponse(output = output)
	except:
		IN.logger.debug()