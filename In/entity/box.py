from In.boxer.box import Box, BoxThemer

class BoxEntityList(Box):

	pass


@IN.register('BoxEntityList', type = 'Themer')
class BoxEntityListThemer(BoxThemer):

	def theme(self, obj, format, view_mode, args):
		super().theme(obj, format, view_mode, args)

	def theme_value(self, obj, format, view_mode, args):

		values = []

		entitier = IN.entitier
		
		types = entitier.types
		bundles = entitier.entity_bundle
		
		for entity_type in types:
			subs = ''
			if entity_type in bundles:
				subs = []
				for bundle in bundles[entity_type]:
					subs.append(''.join(('<li><a data-ajax_panel="content" href="/admin/structure/entity/!', entity_type, '/bundle/!', bundle, '">', bundle, '</a></li>')))
				if subs:
					subs = ''.join(subs).join(('<ul class="i-nav-sub">', '</ul>'))
				
			values.append(''.join(('<li><a data-ajax_panel="content" href="/admin/structure/entity/!', entity_type, '">', entity_type, '</a>', subs, '</li>')))
			
		return ''.join(values).join(('<ul>', '</ul>'))
