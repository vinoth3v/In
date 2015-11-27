
def content_entity_edit_form(context, action, entity_id, **args):
	# TODO: nabar access

	entity_type = 'Content'

	entitier = IN.entitier
	
	# load the entity
	entity_id = int(entity_id)
	
	IN.entitier.entity_page_edit(entity_type, entity_id, 'full')
	
	#entity = entitier.load(entity_type, entity_id)
	
	#if entity is None:
		 #invalid entity
		#context.not_found()
	#else:

		 #access denied
		#entitier.access('edit', entity, deny = True)
		
		#context.ensure_page_response()

		#try:
			 #it may raise errors
			#form = entitier.get_entity_edit_form(entity_type, entity_id)
			#if form is not None:
				#context.response.output.add(form)
		#except Exception as e:
			#IN.logger.debug()
			#context.not_found()
