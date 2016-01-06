
@IN.hook
def actions():
	actns = {}
	
	admin_path = IN.APP.config.admin_path
	actns[admin_path + '/structure/entity/{entity_type}/bundle/{entity_bundle}/manage/vakai'] = {
		'title' : 'Manage Vakai',
		'handler' : vakai_admin_action_manage,
	}

	return actns



def vakai_admin_action_manage(context, action, entity_type, entity_bundle, **args):
	
	# TODO: admin access
	# TODO: drag n drop to weight order, parent/child
	
	context.page_title = s('Manage {entity_bundle} vakai', {'entity_bundle' : entity_bundle})
	
	# add list
	data = {
		'lazy_args' : {
			'load_args' : {
				'data' : {
					'parent_entity_type' : entity_type, # always should be Vakai
					'parent_entity_bundle' : entity_bundle,
					'parent_entity_id' : 0, # parent
				},
			},
		},
		'parent_entity_type' : entity_type, # always should be Vakai
		'parent_entity_bundle' : entity_bundle,
		'parent_entity_id' : 0, # parent
	}
	
	list = Object.new('VakaiListLazy', data = data)
	
	output = context.response.output
	output.add(list)
	
	# add form
	args = {
		'data' : {
			# ajax replace
			'id' : '_'.join(('VakaiAdminAddForm', entity_type, entity_bundle)),
			'title' : s('Add new vakai'),
		},
		'parent_entity_bundle' : entity_bundle,
		'parent_entity_type' : entity_type,
	}
	
	form = IN.entitier.get_entity_add_form(entity_type, entity_bundle, args)
	
	if form:
		output.add(form)
	
