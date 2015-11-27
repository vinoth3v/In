from .page import *

@IN.hook
def actions():
	actns = {}

	actns['status/add/{entity_bundle}'] = {
		'title' : 'Add status',
		'handler' : status_add_form,
	}

	actns['status/{entity_id}'] = {
		'handler' : status_view,
	}

	actns['status/{status_id}/edit'] = {
		'handler' : action_status_edit_form,
	}

	actns['status/{status_id}/delete/confirm'] = {
		'title' : 'status delete confirm',
		'handler' : action_status_delete_form,
	}

	return actns

