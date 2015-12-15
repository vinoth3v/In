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
		
		#org_path_tokenized = context.request.path_tokenized
		#path_tokenized = org_path_tokenized.replace('*', '_')
		#path_tokenized = path_tokenized.replace('/', '_')
		
		## hook by path
		#IN.hook_invoke('page_menu_tab_' + path_tokenized, context)
		
		## hook by anything_after path
		
		## content/*/edit
		## content___edit_anything_after
		## content___anything_after
		## content_anything_after
		
		#token_paths = org_path_tokenized.split('/')
		#while(token_paths):
			
			#new_token_path = '/'.join(token_paths)
			#new_token_path = new_token_path.replace('*', '_')
			#new_token_path = new_token_path.replace('/', '_')
			
			#new_token_path += '_anything_after'
			
			##print(new_token_path)
			
			#IN.hook_invoke('page_menu_tab_' + new_token_path, context)
			
			##token_paths = token_paths[:-1]
			#del token_paths[-1]
		
		path_hook_tokens = context.request.path_hook_tokens()
		
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
