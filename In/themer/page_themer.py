from In.themer.object_themer import ObjectThemer

@IN.register('Page', type = 'Themer')
class PageThemer(ObjectThemer):

	__invoke_theme_hook__ = True
	merge_children = False

	def theme_attributes(self, obj, format, view_mode, args):
		super().theme_attributes(obj, format, view_mode, args)

		themer = args['__theme_engine__']

		page_attrbs = {
			'lang' : obj.page_lang,
			'dir' : obj.page_dir,
		}

		# hack
		theme_output = obj.theme_current_output['content']
		theme_output['page_attributes'] = themer.theme_attributes(page_attrbs)

	def theme_process_variables(self, obj, format, view_mode, args):
		
		super().theme_process_variables(obj, format, view_mode, args)
		
		
		args['page'] = obj # theme may need this instance

		args['title'] = IN.context.page_title

		#args['head'] = theme_output.header_links
		context = args['context']
		
		asset = context.asset
		
		IN.hook_invoke('asset_prepare', context)
		IN.hook_invoke('asset_prepare', context)
		
		args['header_css'] = asset.theme_css('header')
		args['footer_css'] = asset.theme_css('footer')
		args['header_js'] = asset.theme_js('header')
		args['footer_js'] = asset.theme_js('footer')

		args['doctype'] = '<!DOCTYPE html>'
		args['head_tags'] = ''
		args['html_attributes'] = ''

	#def theme_done(self, obj, format, view_mode, args):
		#super().theme_done(self, obj, format, view_mode, args)
	
	def ajax_replaceable_elements(self):
		return ['promotion', 'content', 'sidebar1', 'sidebar2']
		
	def theme_items(self, obj, format, view_mode, args):
		
		layout = obj.add(obj.__page_layout_type__, {
			'id' : 'ajax_page_replaceable',
		}, panel = None) # adding to page itself, not to panel
		
		
		for element in self.ajax_replaceable_elements():
			layout.add(obj[element])
			del obj[element]
		
		super().theme_items(obj, format, view_mode, args)
		
		
	def ajax_children(self, obj, panel = None):
		'''Change the children and return only ajax based elements.
		'''
		
		ajax_elements = {}

		if panel is None:
			ajax_elements['ajax_page_replaceable'] = obj.new(type=obj.__page_layout_type__, id='ajax_page_replaceable')
			
			for element in self.ajax_replaceable_elements():
				ajax_elements['ajax_page_replaceable'].add(obj[element])
				
		else:
			# replace only one panel
			panels = panel.split(',')
			for panel in panels:
				if panel in obj:
					ajax_elements[panel] = obj[panel]

		return ajax_elements


@IN.register('PageLayout', type = 'Themer')
class PageLayoutThemer(ObjectThemer):
	
	merge_children = False
	
	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)

		args['promotion'] = args['children']['promotion']['content']
		args['content'] = args['children']['content']['content']
		
		if 'sidebar1' in args['children']:
			args['sidebar1'] = args['children']['sidebar1']['content']
		if 'sidebar2' in args['children']:
			args['sidebar2'] = args['children']['sidebar2']['content']
		
		

