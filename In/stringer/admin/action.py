from .page import *

@IN.hook
def actions():
	actns = {}
	
	admin_path = IN.APP.config.admin_path
	
	actns[admin_path + '/dev/string'] = {
		'handler' : action_handler_stringer_admin_dev_i18n,
	}
	actns[admin_path + '/dev/string/update-to-db'] = {
		'handler' : action_handler_stringer_update_to_db,
	}
	return actns
