from .page import *

@IN.hook
def actions():
	actns = {}
	
	admin_path = IN.APP.config.admin_path
	
	actns[admin_path + '/structure/entity/{entity_type}/bundle/{entity_bundle}/field'] = {
		'title' : 'Entity fields',
		'handler' : field_admin_action_field_ui_form,
	}
	
	actns[admin_path + '/structure/entity/{entity_type}/bundle/{entity_bundle}/field/add'] = {
		'title' : 'Add new fields',
		'handler' : field_admin_action_field_ui_add_field_form,
	}

	actns[admin_path + '/structure/entity/{entity_type}/bundle/{entity_bundle}/field/{field_name}/edit'] = {
		'title' : 'Entity field_config_form',
		'handler' : field_admin_action_entity_bundle_field_config_form,
	}

	actns[admin_path + '/structure/entity/{entity_type}/bundle/{entity_bundle}/display'] = {
		'title' : 'Entity view mode',
		'handler' : field_admin_action_entity_display_ui,
	}
	actns[admin_path + '/structure/entity/{entity_type}/bundle/{entity_bundle}/display/{view_mode}'] = {
		'title' : 'Entity view mode: default',
		'handler' : field_admin_action_entity_display_ui,
	}

	actns[admin_path + '/structure/entity/{entity_type}/bundle/{entity_bundle}/display/{view_mode}/copy-configuration'] = {
		'title' : 'copy field display confguration',
		'handler' : field_admin_action_entity_display_copy_configuration,
	}

	actns[admin_path + '/structure/entity/{entity_type}/bundle/{entity_bundle}/display/{view_mode}/field/{field_name}/field_formatter_form'] = {
		'title' : 'Entity field_formatter_form',
		'handler' : field_admin_action_entity_bundle_field_field_formatter_form,
	}

	return actns
