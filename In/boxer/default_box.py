from In.boxer.box import Box, BoxThemer

@IN.hook
def decide_page_boxes_alter(boxes, context, page, format):
	'''add default boxes'''
	
	if format != 'html':
		return
	
	# add menu tab only if page has tabs
	boxes.append(['BoxPageMenuTab', 'content', {
		'type' : 'BoxPageMenuTab',
		'data' : {
			'weight' : -2,
		}
	}])
	
	if context.display_title:
		boxes.append(['BoxPageTitle', 'content', {
			'type' : 'BoxPageTitle',
			'data' : {
				'weight' : -3,
			}
		}])
	

class BoxSitelogo(Box):
	pass


@IN.register('BoxSitelogo', type = 'Themer')
class BoxSitelogoThemer(BoxThemer):
	''''''

class BoxPageMenuTab(Box):
	pass


@IN.register('BoxPageMenuTab', type = 'Themer')
class BoxPageMenuTabThemer(BoxThemer):


	def theme_items(self, obj, format, view_mode, args):
		
		context = args['context']
		
		path_hook_tokens = context.request.path_hook_tokens()
		pprint(path_hook_tokens)
		for hook in path_hook_tokens:
			IN.hook_invoke('page_menu_tab_' + hook, context)
		
		# hook by all path
		IN.hook_invoke('page_menu_tab', context)
		
		if len(IN.context.page_menu_tab):
			IN.context.page_menu_tab.weight = 1
			obj.add(IN.context.page_menu_tab)
			
		if len(IN.context.page_menu_sub_tab):
			IN.context.page_menu_sub_tab.weight = 2
			obj.add(IN.context.page_menu_sub_tab)

		if len(IN.context.page_menu_sub_tab_2):
			IN.context.page_menu_sub_tab_2.weight = 3
			obj.add(IN.context.page_menu_sub_tab_2)
		
		super().theme_items(obj, format, view_mode, args)

		
class BoxPageTitle(Box):
	''''''
	
@IN.register('BoxPageTitle', type = 'Themer')
class BoxPageTitleThemer(BoxThemer):
	'''BoxPageTitle'''
	
	def theme_value(self, obj, format, view_mode, args):
		return IN.context.page_title or ''
