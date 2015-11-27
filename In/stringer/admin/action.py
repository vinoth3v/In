from .page import *

@IN.hook
def actions():
	actns = {}

	actns['admin/dev/string'] = {
		'handler' : action_handler_stringer_admin_dev_i18n,
	}
	actns['admin/dev/string/update-to-db'] = {
		'handler' : action_handler_stringer_update_to_db,
	}
	return actns
