

@IN.hook
def actions():
	actns = {}

	actns['admin/structure/entity'] = {
		'title' : 'Entity',
		'handler' : entity_admin_action_entity_list,
	}
	
	actns['admin/structure/entity/{entity_type}'] = {
		'title' : 'Entity',
		'handler' : entity_admin_action_config_ui_form,
	}
	actns['admin/structure/entity/{entity_type}/bundle'] = {
		'title' : 'Entity',
		'handler' : entity_admin_action_config_bundle_ui_form,
	}

	actns['admin/structure/entity/{entity_type}/add/{entity_bundle}'] = {
		'title' : 'Entity',
		'handler' : entity_admin_action_add_entity,
	}
	
	actns['admin/structure/entity/{entity_type}/bundle/{entity_bundle}/edit'] = {
		'title' : 'Edit Entity bundle',
		'handler' : entity_admin_action_entity_bundle_edit,
	}
	
	
	actns['admin/structure/entity/{entity_type}/{entity_id}'] = {
		'title' : 'Entity view',
		'handler' : entity_admin_action_view_entity,
	}

	actns['admin/structure/entity/{entity_type}/{entity_id}/edit'] = {
		'title' : 'Entity edit',
		'handler' : entity_admin_action_edit_entity,
	}
	
	actns['admin/structure/entity/{entity_type}/list'] = {
		'title' : 'Entity list',
		'handler' : entity_admin_action_entity_list_entity_instance,
	}
	actns['admin/structure/entity/{entity_type}/bundle/{entity_bundle}/list'] = {
		'title' : 'Entity list by bundle',
		'handler' : entity_admin_action_entity_bundle_list,
	}

	return actns

def entity_admin_action_config_ui_form(context, action, entity_type, **args):

	IN.entitier.access('admin', entity_type, deny = True)
	
	#frm = IN.former.load('FormUserRoleAccessAdmin', args = {'group' : group})

	page = context.response.output
	
	#page.add(frm)

	# add entity list box
	box = IN.boxer.load_box('BoxEntityList')
	page.add(box, panel = 'sidebar1')

def entity_admin_action_entity_list(context, action, **args):
	
	# TODO
	IN.context.access('admin_all_entity', deny = True)

	# add asset
	# in code
	#context.asset.add_js('/files/libraries/uikit-2.18.0/dist/js/core/dropdown.js', key = 'i-dropdown')
	
	#frm = IN.former.load('FormUserRoleAccessAdmin', args = {'group' : group})

	values = ['<table class="i-table">', ''.join(('<thead><tr><td>', s('Entity name'), '</td><td>', s('Actions'), '</td></tr></thead>')), '<tbody>']

	entitier = IN.entitier
	
	types = entitier.types
	bundles = entitier.entity_bundle
	
	si = sorted(types.keys(), key = lambda o: o)
	
	for entity_type in si:
		
		values.append(''.join((
			'<tr><td><a data-ajax_panel="content" href="/admin/structure/entity/!', entity_type, '/bundle">', entity_type, '</a>', '</td>',
			'''<td><div class="i-button-group">
    <a href="/admin/structure/entity/!''', entity_type, '" class="i-button">', s('Edit'), '''</a>
    <a href="/admin/structure/entity/!''', entity_type, '/bundle" class="i-button">', s('Bundles'), '''</a>
    <div data-i-dropdown="{mode:'click'}">
        <a href="#" class="i-button"><i class="i-icon-caret-down"></i></a>
        <div class="i-dropdown i-dropdown-small">
            <ul class="i-nav i-nav-dropdown">
                <li></li>
                <li><a href="">...</a></li>
            </ul>
        </div>
    </div>
</div>
</td>
</tr>'''
		)))
	values.append('</tbody></table>')
	table = ''.join(values)


	page = context.response.output
	page.add('Text', {'value' : table,})

def entity_admin_action_config_ui_form(context, action, entity_type, **args):

	IN.entitier.access('admin', entity_type, deny = True)
	
	#frm = IN.former.load('FormUserRoleAccessAdmin', args = {'group' : group})

	page = context.response.output
	
	#page.add(frm)

	# add entity list box
	box = IN.boxer.load_box('BoxEntityList')
	page.add(box, panel = 'sidebar1')

def entity_admin_action_config_bundle_ui_form(context, action, entity_type, **args):
	
	# TODO
	IN.context.access('admin_all_entity', deny = True)
	
	#frm = IN.former.load('FormUserRoleAccessAdmin', args = {'group' : group})

	values = [entity_type.join(('<h2>', '</h2>'))]

	entitier = IN.entitier
	
	types = entitier.types
	bundles = entitier.entity_bundle
	
	subs = ''
	if entity_type in bundles:
		subs = [''.join(('<thead><tr><td>', s('Bundle name'), '</td><td>', s('Actions'), '</td></tr></thead>'))]

		subs.append('<tbody>')
		
		for bundle in bundles[entity_type]:
			subs.append(''.join((
			'<tr><td><a data-ajax_panel="content" href="/admin/structure/entity/!', entity_type, '/bundle/!', bundle, '/edit">', bundle, '</a>', '</td>',
			'''<td><div class="i-button-group">
	<a href="/admin/structure/entity/!''', entity_type, '/bundle/!', bundle, '/edit" class="i-button">', s('Edit'), '''</a>
	<a href="/admin/structure/entity/!''', entity_type, '/bundle/!', bundle, '/field" class="i-button">', s('Fields'), '''</a>
	<a href="/admin/structure/entity/!''', entity_type, '/bundle/!', bundle, '/display/!default" class="i-button">', s('Display'), '''</a>
	<div data-i-dropdown="{mode:'click'}">
		<a href="#" class="i-button"><i class="i-icon-caret-down"></i></a>
		<div class="i-dropdown i-dropdown-small">
			<ul class="i-nav i-nav-dropdown">
				<li></li>
				<li><a href="/admin/structure/entity/!''', entity_type, '/add/!', bundle, '">', s('Add new {entity_bundle}', {'entity_bundle' : bundle}),'''</a></li>
			</ul>
		</div>
	</div>
</div>
</td>
</tr>'''
		)))
		subs.append('</tbody>')
		
		subs = ''.join(subs).join(('<table class="i-table">', '</table>'))
			
	values.append(subs)

	output = ''.join(values)
	
	page = context.response.output
	page.add('Text', {'value' : output,})

	form = IN.former.load('FormEntityAdminAddBundle', args = {'entity_type' : entity_type})
	page.add(form)

def entity_admin_action_add_entity(context, action, entity_type, entity_bundle, **args):

	entitier = IN.entitier

	# access denied
	entitier.access('add', entity_type, entity_bundle, deny = True)
	
	form = entitier.get_entity_add_form(entity_type, entity_bundle)
	
	if form is not None:
		context.response.output.add(form)
	

def entity_admin_action_view_entity(context, action, entity_type, entity_id, **args):

	view_mode = 'full'

	IN.entitier.entity_page_view(entity_type, entity_id, view_mode)
	
def entity_admin_action_edit_entity(context, action, entity_type, entity_id, **args):

	IN.entitier.entity_page_edit(entity_type, entity_id)
	
def entity_admin_action_entity_list_entity_instance(context, action, entity_type, **args):
	
	# TODO: admin access
	
	data = {
		'entity_type' : entity_type,
	}
	
	list = Object.new('EntityList', data = data)
	
	context.response.output.add(list)


def entity_admin_action_entity_bundle_list(context, action, entity_type, entity_bundle, **args):
	
	# TODO: admin access
	
	data = {
		'entity_type' : entity_type,
		'entity_bundle': entity_bundle,
	}
	
	list = Object.new('EntityList', data = data)
	
	context.response.output.add(list)

def entity_admin_action_entity_bundle_edit(context, action, entity_type, entity_bundle, **args):
	
	args = {
		'entity_type' : entity_type,
		'entity_bundle': entity_bundle,
	}
	
	form = IN.former.load('FormEntityAdminEditBundle', args = args)
	context.response.output.add(form)
	
