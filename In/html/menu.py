from In.html.tags import Ul

builtins.menu_admin = '~admin'

class Menu(Object):
	'''<ul>, <li> tags
	'''
	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		args['direction'] = args.get('direction', '|')

	def add(self, itm=None, **args):
		if not 'item_wrapper' in args:
			args['item_wrapper'] = 'Li'
		return super().add(self, itm, **args)

class SimpleMenu(Object):
	'''inline <a> tags
	'''

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		args['child_separator'] = args.get('child_separator', ' | ')
		Object.__init__(self, **args)


class BreadCrumb(Object):
	'''inline <a> tags
	'''

	def __init__(self, data = None, items = None, **args):
		args['child_separator'] = args.get('child_separator', ' | ')
		super().__init__(data, items, **args)


class PageMenuTab(Ul):
	'''page primary menu'''

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		self.css.append('i-tab')


#def build_menu(refresh=False):
	#'''TODO:Prepares all the menus
	#'''
	#if not refresh and hasattr(app, 'menus'):
		#ret_menus = app.menus
		#if ret_menus:
			#return ret_menus

	#ret_menus = OrderedDict()
	#ret = package.invokeall('blocks', __inc_module__ = True)
	#if ret:
		#for itm in ret:
			#if itm:
				#for mod, blks in itm.items():
					#for key, blk in blks.items():
						#blk['module'] = mod
						#ret_menus[mod + '.' + key] = blk
	#app.menus = ret_menus
	#return ret_menus

#@IN.hook
#def actions():
	#actns = {}
	#actns[menu_admin + '/settings/menu'] = {
		#'title' : 'Menu', #it will call s() automatically on display
		#'handler' : page_menu_list,
	#}
	#return actns

#def page_menu_list(**args):

	#rows = {}
	#blks = action.build_blocks()

	#tbl = page.add(
		#type = 'Table',
		#rows = rows,
	#)

	#tr = tbl.add(type = 'Row', rowtype = 'header', columns = ['module', 'title', 'handler'])

	#for key, blk in blks.items():
		#tr = tbl.add(type = 'Row', columns = [blk['module'], blk['title'], blk['handler']])

builtins.Menu = Menu
builtins.SimpleMenu = SimpleMenu
builtins.BreadCrumb = BreadCrumb

