from .page import *

@IN.hook
def actions():
	actns = {}

	actns['nabar/{entity_id}/edit/profile/{profile_bundle}'] = {
		'handler' : profile_action_handler_page_profile_edit,
	}

	return actns

