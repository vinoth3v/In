def action_status_edit_form(context, action, status_id, **args):
	
	entitier = IN.entitier
	
	entity = entitier.load_single('Status', int(status_id))

	if not entity:
		context.not_found()
		
	try:
		
		entitier.access('edit', entity, deny = True)
		
		form = IN.entitier.get_entity_edit_form('Status', entity.id)
		
		if context.request.ajax:
			element_id = '-'.join(('#status', str(entity.id), 'children'))
			
			output = [{
				'method' : 'html',
				'args' : [element_id, IN.themer.theme(form)]
			}]
			context.response = In.core.response.CustomResponse(output = output)
			
		else:
			context.response.output.add(form)
			
	except:
		IN.logger.debug()
