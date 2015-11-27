from .page import *


@IN.hook
def actions():
	actns = {}

	actns['node/add/{entity_bundle}'] = {
		'title' : 'Add content',
		'handler' : content_entity_add_form,
	}

	actns['node/{entity_id}'] = {
		'handler' : content_view,
	}

	actns['node/{entity_id}/edit'] = {
		'handler' : content_entity_edit_form,
	}

	actns['node/{entity_id}/delete'] = {
		'handler' : content_entity_delete_form,
	}

	return actns


