

@IN.hook
def page_menu_tab_admin_structure_entity___bundle___display__(context):
	
	
	request = context.request
	
	path_parts = context.request.path_parts
	
	entity_type = request.path_tokenized_values[0]
	entity_bundle = request.path_tokenized_values[1]
	if len(path_parts) == 8:
		view_mode = request.path_tokenized_values[2]
	else:
		view_mode = 'default'
	
	view_modes =  IN.entitier.view_modes(entity_type, entity_bundle)
	
	if not view_modes:
		return
	
	admin_path = IN.APP.config.admin_path
	
	tab = context.page_menu_sub_tab_2
	for mode in sorted(view_modes, key = lambda v: v):
		li = tab.add('Li', {
			'css' : ['i-active' if view_mode == mode else '']
		}).add('Link', {
			'href' : ''.join(('/', admin_path, '/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/display/!', mode)),
			'value' : s(mode),
		})
