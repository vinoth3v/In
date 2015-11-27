
class ObjectLister(HTMLObject):
	'''List objects'''
	
	# value from this argument will be used to identify the current page index
	current_arg = 'page'
	
	# default object view mode
	view_mode = 'default'
	
	# if set this query will be used to load entities
	entity_load_query = None
	
	entity_type = None
	
	limit = 1
	current = None
	__total__ = None
	
	handler_get_total = None
	handler_prepare_objects = None
	
	list_object_class = None
	list_object_wrapper = None
	
	empty_text = None
	
	# objects will be added to this if set
	container = None
	url = None
	
	pager = None
	
	def __init__(self, data = None, items = None, **args):
		
		super().__init__(data, items, **args)
		
		content_panel = data.get('content_panel', {})
		content_panel.update({
			'id' : 'content_panel',
			'weight' : 0,
			'default_children_view_mode' : self.view_mode
		})
		
		self.content_panel = self.add('TextDiv', content_panel)
		
		self.content_panel.css.append('content-panel')
		
		self.pager_panel = self.add('TextDiv', {
			'id' : 'pager_panel',
			'css' : ['pager-panel'],
			'weight' : 10,
		})
		
		try:
			request_args = IN.context.request.args['query']
			self.current = int(request_args.get(self.current_arg, 1))
		except ValueError:
			self.current = 1
		
		
	def list(self):
		'''list objects'''
		
		# prepare and add the objects to self.content_panel
		try:
			self.__prepare_objects__()
		except Exception as e:
			IN.logger.debug()
		
		context = IN.context
		
		pager = self.pager
		
		listed = self.current * self.limit
		
		if len(self.content_panel) and pager: # and listed < self.total:
			if 'data' not in pager:
				pager['data'] = {}
			
			if not self.url:
				self.url = IN.context.request.path
			
			pager['data'].update({
				'current_page' : self.current,
				'total_pages' : int(self.total / self.limit),
				'url' : self.url,
				'link_ajax_args' : {'lister' : 1},
			})
			
			pager = self.pager_panel.add(**pager)
		
		# add empty_text
		if len(self.content_panel) == 0 and self.current == 1 and self.empty_text:
			self.content_panel.add('TextDiv', {
				'value' : self.empty_text,
				'css' : ['empty-text']
			})
		
		
		if not 'lister' in context.request.ajax_args:
			# new list, # add self, theme self
			if self.container:
				self.container.add(self)
			else:
				context.response.output.add(self)
			
		else:
			# already in lister, # append or replace based on pager
			if self.pager and 'append_type' in self.pager:
				append_type = self.pager['append_type']
			else:
				append_type = 'replace'
			
			context.response = In.core.response.CustomResponse()
			output = IN.themer.theme(self)
			
			if append_type == 'replace':
				# replace self
				IN.context.response.output = [{
					'method' : append_type,
					'args' : ['#' + self.id, output]
				}]
			else:
				# append to content list and 
				output = self.content_panel.theme_output['html']['default']['output']['children']
				context.response.output = [{
					'method' : append_type,
					'args' : ['#' + self.id + ' .content-panel', output]
				}]
				
				# replace pager
				pager_output = self.pager_panel.theme_current_output['output']['final']
				context.response.output.append({
					'method' : 'replace',
					'args' : [''.join(('#', self.id, ' .pager-panel')), pager_output]
				})
			
			
	@property
	def total(self):
		if self.__total__ is not None:
			return self.__total__
			
		if self.entity_load_query:
			cursor = self.entity_load_query.execute_count()
			if cursor.rowcount > 0:
				self.__total__ = cursor.fetchone()[0]
		elif self.handler_get_total:
			self.__total__ = self.handler_get_total()
		else:
			self.__total__ = 0
			
		return self.__total__
		
	def __prepare_objects__(self):
		
		if self.handler_prepare_objects:
			# call the handler to load objects
			self.handler_prepare_objects(self)
			
			
		elif self.entity_load_query is not None:
			# load entities and add
			
			limit = self.limit
			
			if self.current > 1:
				if self.current == 2:
					limit = [limit, limit]
				else:
					limit = [(self.current -1) * limit, limit]
				self.entity_load_query.limit = limit
				
			
			cursor = self.entity_load_query.execute()
			entitier =  IN.entitier
			content_panel = self.content_panel
			
			if cursor.rowcount > 0:
				
				result = cursor.fetchall()
				
				entity_ids = []
				for r in result:
					if r[0] not in entity_ids:
						entity_ids.append(r[0])
				
				entities = entitier.load_multiple(self.entity_type, entity_ids)
				weight = 1
				for id in entity_ids: # keep order
					if id in entities:
						entity = entities[id]
						entity.weight = weight
						
						if self.list_object_class:
							entity.css.append(self.list_object_class)
						
						if self.list_object_wrapper is None:
							content_panel.add(entity)
						else:
							content_panel.add(self.list_object_wrapper).add(entity)
						weight += 1
		else:
			pass
			
builtins.ObjectLister = ObjectLister
