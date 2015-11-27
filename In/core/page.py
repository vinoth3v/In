class PageLayout(Object):
	'''page layout usefull for ajax returns'''
	
	

class Page(Object):

	page_lang = ''
	page_dir = 'ltr'
	def_content_panel = 'content'
	__page_layout_type__ = 'PageLayout'
	__panel_type__ = 'Section'

	def __init__(self, data = None, items = None, **args):
		if data is None:
			data = {}

		data['panels'] = data.get('panels', {})
		data['messages'] = data.get('messages', In.logger.Logs())
		data['breadcrumb'] = data.get('breadcrumb', BreadCrumb(child_separator = ' - '))

		super().__init__(data, items, **args)


		# super() : adding panel to page instead of add object to panel
		# add pass panel to None
		
		super().add('SiteHeader', {
			'id' : 'header',
			'css' : ['site-header']
		})
		super().add('Object', {
			'id' : 'promotion',
			'css' : ['promoted']
		})
		
		# add default panel = content
		super().add(self.__panel_type__, {
			'id' : self.def_content_panel,
			'css' : ['main-content']
		})

		super().add('Aside', {
			'id' : 'sidebar1',
			'css' : ['sidebar1']
		})
		super().add('Aside', {
			'id' : 'sidebar2',
			'css' : ['sidebar2']
		})
		super().add('Aside', {
			'id' : 'sidebar3',
			'css' : ['sidebar3']
		})
		super().add('Aside', {
			'id' : 'sidebar4',
			'css' : ['sidebar4']
		})
		super().add('SiteFooter', {
			'id' : 'footer',
			'css' : ['site-footer'],
		})


	def add(self, obj = None, type = 'Object', panel = def_content_panel, **args):
		'''Add Object to page.

		by default object will be added to default panel = content
		pass panel to None to add Object to page itself.
		'''
		
		bType = builtins.type
		obj_type = type
		
		if bType(obj) is str:
			# use first string as string
			obj_type = obj
		
		if bType(type) is dict:
			# second arg may be dict
			data = type
			args['data'] = data
		
		if not isinstance(obj, Object):

			#if 'weight' not in args:
				#args['weight'] = len(self)

			obj = self.new(obj_type, **args)

		if obj is None:
			raise In.core.object.ObjectMismatchException(''.join(('Unable to add item to ', self.__type__, '. Item is None.')))
		
		if panel is not None:
			if panel not in self.panels:
				self.panels[panel] = panel

			# add item to panel/childern
			try:
				panel_obj = self[panel]
			except KeyError:
				panel_obj = super().add(self.__panel_type__, data = {
					'id' : panel,
				})

			panel_obj.add(obj)
			
		else:
			super().add(obj)
		return obj


