

@IN.hook
def page_menu_tab_admin_structure_entity_anything_after(context):
	
	tab = context.page_menu_tab
	
	li = tab.add('Li', {
		'css' : ['i-active' if context.request.path == 'admin/structure/entity' else ''],
		'weight' : 0
	}).add('Link', {
		'href' : '/admin/structure/entity',
		'value' : s('Entity'),
	})



@IN.hook
def page_menu_tab_admin_structure_entity___anything_after(context):
	
	tab = context.page_menu_tab
	path_parts = context.request.path_parts
	
	entity_type = path_parts[3].replace('!', '')
	path = ''.join(('admin/structure/entity/!', entity_type, '/bundle'))
	li = tab.add('Li', {
		'css' : ['i-active' if context.request.path == path else ''],
		'weight' : 1
	}).add('Link', {
		'href' : '/' + path,
		'value' : s(entity_type),
	})

@IN.hook
def page_menu_tab_admin_structure_entity___bundle___anything_after(context):
	
	tab = context.page_menu_sub_tab
	path_parts = context.request.path_parts
	
	entity_type = path_parts[3].replace('!', '')
	entity_bundle = path_parts[5].replace('!', '')
	
	path = ''.join(('admin/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/edit'))
	li = tab.add('Li', {
		'css' : ['i-active' if path_parts[6] == 'edit' else ''],
		'weight' : 0
	}).add('Link', {
		'href' : '/' + path,
		'value' : s(entity_bundle),
	})
	
	path = ''.join(('admin/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/field'))
	li = tab.add('Li', {
		'css' : ['i-active' if path_parts[6] == 'field' else ''],
		'weight' : 1
	}).add('Link', {
		'href' : '/' + path,
		'value' : s('Field'),
	})
	
	path = ''.join(('admin/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/display/!default'))
	li = tab.add('Li', {
		'css' : ['i-active' if path_parts[6] == 'display' else ''],
		'weight' : 2
	}).add('Link', {
		'href' : '/' + path,
		'value' : s('Display'),
	})

