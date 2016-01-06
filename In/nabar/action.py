from .page import *

@IN.hook
def actions():
	actns = {}
	
	actns['nabar/register'] = {
		'title' : 'Nabar Register',
		'handler' : nabar_register,
	}
	actns['nabar/recover'] = {
		'title' : 'Forgot Password',
		'handler' : nabar_recover,
	}
	actns['nabar/login'] = {
		'title' : 'Nabar Login',
		'handler' : nabar_login,
	}
	# TODO: referrer only from same domain
	actns['nabar/logout'] = {
		'title' : 'Nabar logout',
		'handler' : nabar_logout,
	}
		
	actns['nabar/{entity_id}'] = {
		'handler' : nabar_view,
	}
	#actns['nabar/{entity_id}/edit'] = {
		#'handler' : nabar_view,
	#}
	actns['nabar/{entity_id}/edit/login'] = {
		'handler' : nabar_action_handler_page_edit_login,
	}
	actns['nabar/{entity_id}/edit/password'] = {
		'handler' : nabar_action_handler_page_edit_password,
	}
	actns['nabar/{entity_id}/edit/password/{hash_id}/form'] = {
		'handler' : nabar_action_handler_page_edit_password_form,
	}
	actns['nabar/{entity_id}/edit/password/new/form'] = {
		'handler' : nabar_action_handler_page_new_password_form,
	}

	#actns['nabar/{entity_id}/edit/settings'] = {
	#	'handler' : nabar_action_handler_page_edit_login,
	#}
	
	actns['nabar/autocomplete/{query}'] = {
		'handler' : nabar_action_handler_nabar_autocomplete,
	}
	
	return actns

