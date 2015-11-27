
class EntityList(HTMLObject):
	
	current_arg = 'page'
		
	entity_type = None
	entity_bundle = None
	
	# starting from 1
	current = 1
	total = 100
	
	# to pass custom query
	# if passed, entity based listing will not be used
	query = None
	
	# entities per page
	limit = 1
	
	view_mode = 'default'
	
	# default order
	order = {'created': 'DESC'}
	where = [['status', 1]]
	
	def __init__(self, data = None, items = None, **args):
	
		# the argument that contain page number
		
		self.pager = {
			'type' : 'PagerNumberList', #'PagerPrevNext', #'PagerLoadMore',
			'data' : {},
		}
		
		super().__init__(data, items, **args)
		
		# update current page
		try:
			request_args = IN.context.request.args['query']
			self.current = int(request_args.get(self.current_arg, 1))
		except ValueError:
			self.current = 1
			
		self.css.append('entiti-list')
		
@IN.register('EntityList', type = 'Themer')
class EntityListThemer(ObjectThemer):
	
	def theme_items(self, obj, format, view_mode, args):
		
		entity_type = obj.entity_type
		
		if not entity_type or obj.current > obj.total - 1:
			return super().theme_items(obj, format, view_mode, args)
		
		entitier = IN.entitier
		
		if obj.query is not None:
				
			total_entities = 0
			cursor = obj.query.execute_count()
			if cursor.rowcount > 0:
				total_entities = cursor.fetchone()[0]
			
		else:
			
			table = entitier.entity_model[entity_type]['table']['name']
			
			entity_bundle = obj.entity_bundle
			
			where = obj.where
			
			if entity_bundle:
				if type(entity_bundle) is str:
					where = [['type', entity_bundle]]
				else:
					where = [['type', 'IN', entity_bundle]]
				where.extend(obj.where)
				
			
			limit = obj.limit
			
			if obj.current > 1:
				limit = [obj.current * limit - 1, limit]
			
			cursor = IN.db.select({
				'table' : table,
				'columns' : ['count(*)'],
				'where' : where,
			}).execute()
			
			total_entities = 0
			if cursor.rowcount > 0:
				total_entities = cursor.fetchone()[0]
			
		if total_entities:
			
			if obj.query is not None:
				
				cursor = obj.query.execute()
				
			else:
				
				# TODO: move this logic to lister
				cursor = IN.db.select({
					'table' : table,
					'columns' : ['id'],
					'where' : where,
					'limit' : limit,
					'order' : obj.order
				}).execute()
			
			if cursor.rowcount > 0:
				
				result = cursor.fetchall()
				
				entity_ids = []
				for r in result:				
					if r[0] not in entity_ids:
						entity_ids.append(r[0])
				
				
				entities = entitier.load_multiple(entity_type, entity_ids)
				weight = 1
				for id in entity_ids: # keep order 
					if id in entities:
						entity = entities[id]
						entity.weight = weight
						obj.add(entity)
						weight += 1
		
			# add pager
			pager = obj.pager
			
			if len(obj) and pager and obj.current < obj.total:
				if 'data' not in pager:
					pager['data'] = {}
				
				pager['data'].update({
					'current_page' : obj.current,
					'total_pages' : int(total_entities / obj.limit),
					'url' : IN.context.request.path,
					'weight' : len(obj) + 1,
					'link_ajax_args' : {'lister' : 1},
				})
				
				pager = obj.add(**pager)
				
		if obj.view_mode:
			self.default_children_view_mode = obj.view_mode
		
		super().theme_items(obj, format, view_mode, args)

