

@IN.hook
def actions():
	actns = {}

	actns['flag/flag/{entity_type}/{entity_id}/{flag_type}/{new_status}'] = {
		'title' : 'flag',
		'handler' : action_handler_flag_flag,
	}

	return actns


def action_handler_flag_flag(context, action, entity_type, entity_id, flag_type, new_status, **args):
	
	entitier = IN.entitier
	flagger = IN.flagger
	nabar = IN.context.nabar
	entity_id = int(entity_id)
	
	try:
		# load entity
		entity = entitier.load_single(entity_type, entity_id)
		
		if not entity:
			return
			
	except Exception as e:
		context.response = In.core.response.EmptyResponse()
		return
	
	entity_bundle = entity.type
	
	try:
		# get flag types
		flag_types = flagger.enabled_flag_type[entity_type][entity_bundle]
	except KeyError as e:
		# no flag enabled for this entity
		context.response = In.core.response.EmptyResponse()
		return
	
	for flag_type_entity in flag_types:
		
		# not this flag type
		if flag_type != flag_type_entity.type:
			continue
		
		flag_entity = flagger.flag(flag_type_entity.type, entity, nabar)
		
		flag_status = flag_type_entity.data.get('flag_status', [])
		if not flag_status:
			break
		
		current_status = None
		if flag_entity:
			current_status = flag_entity.flag_status
		
		key, text = flagger.get_next_flag_key_title(flag_status, current_status)
		
		# invalid
		if not key:
			break
			
		# invalid
		if key != new_status:
			break
		
		if not flagger.access(entity, nabar, flag_type_entity, key):
			break
		
		try:
			
			# create update change flag
			flag_entity = flagger.flag(flag_type_entity.type, entity, nabar, new_status)
			
			# get new status and output
			# id flag_link-Comment-comment_page-like
			
			key, text = flagger.get_next_flag_key_title(flag_status, flag_entity.flag_status)
			
			element_id = '-'.join(('flag_link', entity_type, entity_bundle, flag_type_entity.type))
			flag_link = Object.new(type = 'Link', data = {
				'id' : element_id,
				'css' : [
					'ajax i-button i-button-small',
					'flag-button flag-' + flag_type_entity.type,
					'-'.join(('flag', flag_type_entity.type, key))
				],
				'value' : text,
				'href' : ''.join(('/flag/flag/!', entity_type, '/', str(entity_id), '/!', flag_type_entity.type, '/!', key)),
				'weight' : -1,
			})
			
			output = {element_id : flag_link}
			context.response = In.core.response.PartialResponse(output = output)
			
			return
			
		except:
			IN.logger.debug()

		context.response = In.core.response.EmptyResponse()
