
def field_admin_action_field_ui_form(context, action, entity_type, entity_bundle, **args):
	# TODO: admin access

	IN.entitier.access('admin', entity_type, entity_bundle, deny = True)

	values = [s('{entity_type} fields', {'entity_type' : entity_type}).join(('<h2>', '</h2>'))]

	entitier = IN.entitier
	fielder = IN.fielder
	
	types = entitier.types
	bundles = entitier.entity_bundle
	
	entity_field_config = fielder.entity_field_config
	
	admin_path = IN.APP.config.admin_path
	
	subs = ''
	if entity_type in entity_field_config and entity_bundle in entity_field_config[entity_type]:
		
		field_config = entity_field_config[entity_type][entity_bundle]
		
		subs = [''.join(('<thead><tr><td>', s('Field'), '</td><td>', s('Field type'), '</td><td>', s('Actions'), '</td></tr></thead>'))]

		subs.append('<tbody>')
		
		for field_name, field_config in field_config.items():
			subs.append(''.join((
			'<tr><td><a data-ajax_panel="content" href="/', admin_path, '/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/field/!', field_name, '/edit">', field_name, '</a>', '</td>',
			'<td>', field_config['field_type'], '</td>',
			'<td><div class="i-button-group">',
			'<a href="/', admin_path, '/structure/entity/!''', entity_type, '/bundle/!', entity_bundle, '/field/!', field_name, '/edit" class="i-button">', s('Edit'), '''</a>
	<div data-i-dropdown="{mode:'click'}">
		<a href="#" class="i-button"><i class="i-icon-caret-down"></i></a>
		<div class="i-dropdown i-dropdown-small">
			<ul class="i-nav i-nav-dropdown">
				<li></li>''',
				'<li><a href="/', admin_path, '/structure/entity/!''', entity_type, '/add/!', entity_bundle, '">', s('Add new {entity_bundle}', {'entity_bundle' : entity_bundle}),'''</a></li>
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

	set = page.add('FieldSet', {
		'title' : s('Add field'),
		'css' : ['i-margin-large'],
		'weight' : 11,
	})

	set.add('Link', {
		'css' : ['i-button i-button'],
		'value' : s('Add new field'),
		'href' : ''.join(('/', admin_path, '/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/field/add')),
	})
