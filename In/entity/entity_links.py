
class EntityContextLinks(In.core.lazy.HTMLObjectLazy):

	context_type = 'links'

	theme_view_mode = 'default'

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)

		parent_entity_type = self.parent_entity_type
		parent_entity_id = self.parent_entity_id

		# always set new id
		self.id = '_'.join((self.__type__, parent_entity_type, str(parent_entity_id), self.theme_view_mode))

		# TODO:
		#self.css.append('')

class EntityContextMenu(EntityContextLinks):

	context_type = 'menu'

class EntityContextTab(EntityContextLinks):

	context_type = 'tab'


@IN.register('EntityContextLinks', type = 'Themer')
class EntityContextLinksThemer(In.core.lazy.HTMLObjectLazyThemer):


	def theme_items(self, obj, format, view_mode, args):

		if view_mode != 'lazy':

			entitier = IN.entitier

			# add entity links here
			entity_type = obj.parent_entity_type
			entity_id = obj.parent_entity_id

			entity = entitier.load_single(entity_type, entity_id)

			if entity is not None:

				links = entitier.entity_context_links(entity, obj.context_type, format, obj.theme_view_mode)

				if links is not None:
					for id, l in links.items():
						obj.add(l)

			super().theme_items(obj, format, view_mode, args)
