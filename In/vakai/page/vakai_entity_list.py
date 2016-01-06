def action_handler_vakai_entity_list(context, action, entity_type, field, vakai_id, **args):
	
	entitier = IN.entitier
	fielder = IN.fielder
	
	if field not in fielder.field_instance_config:
		context.not_found()
	
	cls = IN.register.get_class(entity_type, 'Entity')
	if cls is None:
		context.not_found()
	
	vakai_entity = IN.entitier.load_single('Vakai', vakai_id)
	
	if not vakai_entity:
		context.not_found()
		
	entity_title = entitier.entity_title(vakai_entity)
	
	if entity_title:
		context.page_title = entity_title
	
	#TODO: it overrides weight property of vakai
	vakai_entity.weight = -2
	
	context.response.output.add(vakai_entity)
	
	field_table = fielder.field_table(field)
	entity_table = entitier.entity_model[entity_type]['table']['name']
	
	limit = 10
	
	query = IN.db.select({
		'table' : [field_table, 'f'],
		'columns' : ['entity_id'],
		'join' : [
			['inner join', entity_table, 'e', [
				['f.entity_type', entity_type], 
				['f.entity_id = e.id']],
			]
		],
		'where' : [
			['e.status', '>', 0],
			['f.value', vakai_id]
		],
		'limit' : limit,
		'order' : {'e.created' : 'DESC'},
	})
	
	pager = {
		'type' : 'PagerLoadMore',
		'data' : {
			'css' : ['auto-scrollspy-click'],
			'attributes' : {'data-i-scrollspy' : '{topoffset: 200, delay:800, repeat: true}'},
		},
		'append_type' : 'append',
	}

	lister = Object.new('ObjectLister', {
		'id' : 'vakai_entity_lister',
		'entity_type' : entity_type,
		'entity_load_query' : query,
		'pager' : pager,
		'limit' : limit,
	})
	
	# handle the list
	lister.list()
	
