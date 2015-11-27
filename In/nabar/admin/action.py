from .page import *

@IN.hook
def actions():
	actns = {}

	actns['admin/nabar/role'] = {
		'title' : 'Nabar Role',
		'handler' : action_admin_nabar_role,
	}
	actns['admin/nabar/role/add'] = {
		'title' : 'Add Nabar Role',
		'handler' : action_admin_nabar_role_add,
	}
	actns['admin/nabar/role/access'] = {
		'title' : 'Nabar role access',
		'handler' : action_admin_nabar_role_access,
	}
	actns['admin/nabar/role/access/{group}'] = {
		'title' : 'Nabar role access',
		'handler' : action_admin_nabar_role_access,
	}
	return actns

