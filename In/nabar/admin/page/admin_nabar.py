
def action_admin_nabar(context, action, **args):
	
	
	IN.context.access('admin_nabar', deny = True)
	
	limit = 10
	
	# TODO: ORDER BY
	query = IN.db.select({
		'tables' : [['account.nabar', 'n']],
		'columns' : ['n.id'],
		'order' : 'n.created DESC',
		'limit' : limit,
	})
	
	pager = {
		'type' : 'PagerNumberList',
	}

	lister = Object.new('ObjectLister', {
		'id' : 'nanbargal',
		'entity_type' : 'Nabar',
		'entity_load_query' : query,
		'pager' : pager,
		'limit' : limit,
		'css' : ['i-container i-panel-box'],
		'content_panel' : 'HTMLTable',
		'list_object_class' : 'i-panel i-panel-box ',
		'add_function' : add_function,
	})
	
	# handle the list
	lister.list()
	

	
def add_function(self, entity, content_panel, weight):
	
	if len(content_panel['header']) == 0:
		head = content_panel['header'].add('TR')
		w = 0
		for h in ['ID', 'Picture', 'Name', 'Primary E-mail', 'Created', 'Roles', 'Status']:
			head.add('TH', {
				'value' : s(h),
				'weight' : w,
			})
			w += 1
	
	row = content_panel['body'].add('TR')
	
	row.add('TD', {
		'value' : str(entity.id),
		'weight' : 0,
	})
	
	row.add('TD', {
		'value' : IN.nabar.nabar_profile_picture_themed(entity),
		'weight' : 1,
	})
	
	row.add('TD', {
		'value' : ''.join(('<a href="/nabar/', str(entity.id), '">', entity.name, '</a>')),
		'weight' : 2,
	})
	
	row.add('TD', {
		'value' : entity.data['primary_email'] if 'primary_email' in entity.data else '',
		'weight' : 3,
	})
	
	st = entity.created.strftime
	
	row.add('TD', {
		'value' : ' '.join((s(st('%B')), st("%d, %Y %I:%M"), s(st('%p')))),
		'weight' : 4,
	})
	
	roles = IN.nabar.roles
	
	row.add('TD', {
		'value' : ', '.join([roles[r]['name'] if r in roles else s('Unknown') for r in entity.roles]),
		'weight' : 5,
	})
	
	status = ''
	entity_status = entity.status
	
	if entity_status == IN.nabar.NABAR_STATUS_ACTIVE:
		status = s('Active')
	elif entity_status == IN.nabar.NABAR_STATUS_BLOCKED:
		status = s('Blocked').join(('<span class="i-text-danger">', '</span>'))
	elif entity_status == IN.nabar.NABAR_STATUS_REGISTERED:
		status = s('Registered')
	elif entity_status == 0:
		status = s('Inactive')
	else:
		status = ' : '.join((s('Unknown'), str(entity_status)))
	
	row.add('TD', {
		'value' : status,
		'weight' : 6,
	})