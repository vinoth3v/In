from .page import *

@IN.hook
def actions():
	actns = {}
	
	admin_path = IN.APP.config.admin_path
	
	actns[admin_path + '/nabar'] = {
		'title' : 'Nabar',
		'handler' : action_admin_nabar,
	}
	actns[admin_path + '/nabar/role'] = {
		'title' : 'Nabar Role',
		'handler' : action_admin_nabar_role,
	}
	actns[admin_path + '/nabar/role/add'] = {
		'title' : 'Add Nabar Role',
		'handler' : action_admin_nabar_role_add,
	}
	actns[admin_path + '/nabar/role/access'] = {
		'title' : 'Nabar role access',
		'handler' : action_admin_nabar_role_access,
	}
	actns[admin_path + '/nabar/role/access/{group}'] = {
		'title' : 'Nabar role access',
		'handler' : action_admin_nabar_role_access,
	}
	return actns

