
def field_admin_action_entity_display_ui(context, action, entity_type, entity_bundle, view_mode = 'default', **args):
	# TODO: admin access

	IN.entitier.access('admin', entity_type, entity_bundle, deny = True)

	context.asset.add_css('/files/libraries/uikit-2.21.0/dist/css/components/nestable.almost-flat.css', 'uikir-nestable')
	
	values = [s('{entity_type}: {entity_bundle}  view mode: {view_mode}', {'entity_type' : entity_type, 'entity_bundle' : entity_bundle, 'view_mode' : view_mode}).join(('<h2>', '</h2>'))]

	entitier = IN.entitier
	fielder = IN.fielder
	
	types = entitier.types
	bundles = entitier.entity_bundle
	
	entity_field_config = fielder.entity_field_config
	
	admin_path = IN.APP.config.admin_path
	
	subs = ''
	if entity_type in entity_field_config and entity_bundle in entity_field_config[entity_type]:
		
		field_config = entity_field_config[entity_type][entity_bundle]
		
		subs = []

		subs.append('<ul id="nestable" class="i-nestable">')
		
		for field_name, field_config in field_config.items():
			subs.append(''.join(('''<li class="i-nestable-item" data-i-nestable={handleClass:'i-nestable-handle'}>
				<div class="i-nestable-item">
				<div class="i-nestable-panel">
					<i class="i-icon-bars i-nestable-handle"></i> <span data-nestable-action="toggle"></span>''', 
					'<a data-ajax_type="POST" data-ajax_panel="content" href="/', admin_path, '/structure/entity/!''', entity_type, '/bundle/!', entity_bundle, '/display/!', view_mode, '/field/!', field_name, '/field_formatter_form">', field_name, '</a>', 
				'<div id="', entity_type, '_', entity_bundle, '_', field_name, '_field_formatter_config"></div>',
				'</div></div></li>'
			)))
		subs.append('</ul>')
		
		subs = ''.join(subs)
	
	values.append(subs)
	values.append('''
	<script type="text/javascript">
		require(['jQuery', 'uikit!nestable'], function(){
			//var nestable = UIkit.nestable('#nestable', { });
		});
	</script>
	''')
	
	output = ''.join(values)
	
	page = context.response.output
	page.add('Text', {'value' : output, 'weight' : 10})
	
	
	set = page.add('FieldSet', {
		'title' : s('Copy field display configuration'),
		'css' : ['i-margin-large'],
		'weight' : 11,
	})

	set.add('Link', {
		'id' : 'copi-field-displai-configuration',
		'css' : ['no-ajax ajax-modal i-button i-button-small'],
		'value' : s('Copy configuration'),
		'href' : ''.join(('/', admin_path, '/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/display/!', view_mode, '/copi-configuration')),
	})
	
