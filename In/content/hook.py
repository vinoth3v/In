
@IN.hook
def access():
	return {
		'content' : {								# group
			'view_content' : {},					# access key
			'view_own_unpublished_content' : {},
			'edit_own_content' : {},
			'edit_own_unpublished_content' : {},
		}
	}
	
@IN.hook
def entity_insert_Content(entity):
	
	# hack
	if hasattr(entity, 'create_comment_container') and not entity.create_comment_container:
		return
	
	IN.commenter.create_comment_container(entity)

@IN.hook
def page_menu_tab_node___anything_after(context):
	
	tab = context.page_menu_tab
	
	path_parts = context.request.path_parts
	
	parts_len = len(path_parts)
	
	if path_parts[1].isnumeric():
		
		entity_id = path_parts[1]
		entitier = IN.entitier
		
		entity = entitier.load_single('Content', int(entity_id))
		
		if entity is None or entity.status == entitier.STATUS_DELETED:
			return
			
		if not IN.entitier.access('edit', entity):
			
			# we don't need just a view tab alone
			return
		
		li = tab.add('Li', {
			'css' : ['i-active' if parts_len == 2 else ''],
			'weight' : 0
		}).add('Link', {
			'href' : ''.join(('/node/', entity_id)),
			'value' : s('View'),
		})
		
		li = tab.add('Li', {
			'css' : ['i-active' if parts_len == 3 and path_parts[2] == 'edit' else ''],
			'weight' : 1,
		}).add('Link', {
			'href' : ''.join(('/node/', entity_id, '/edit')),
			'value' : s('Edit'),
			'attributes' : {
				'data-ajax_type' : 'POST',
			}
		})
		
		
