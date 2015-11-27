

@IN.hook
def __In_app_init__(app):
	## set the boxer
	IN.nabar.build_access_roles()
	


@IN.hook
def page_menu_tab_nabar___edit_anything_after(context):
	
	nabar_id = context.nabar.id
	
	if not nabar_id:
		return
		
	tab = context.page_menu_tab
	
	path_parts = context.request.path_parts
	
	parts_len = len(path_parts)
	
	if parts_len == 4 or parts_len == 5:
		if path_parts[0] == 'nabar' and path_parts[1].isnumeric() and path_parts[2] == 'edit':

			last = path_parts[3]
			entity_id = path_parts[1]
			
			li = tab.add('Li', {
				'css' : ['i-active' if last == 'login' else '']
			}).add('Link', {
				'href' : ''.join(('/nabar/', entity_id, '/edit/login')),
				'value' : s('Logins'),
			})
			
			li = tab.add('Li', {
				'css' : ['i-active' if last == 'password' else '']
			}).add('Link', {
				'href' : ''.join(('/nabar/', entity_id, '/edit/password')),
				'value' : s('Passwords'),
			})
			
			#li = tab.add('Li', {
				#'css' : ['i-active' if last == 'profile' else '']
			#}).add('Link', {
				#'href' : ''.join(('/nabar/', entity_id, '/edit/profile/_general')),
				#'value' : s('Profile'),
			#})
			
			#li = tab.add('Li', {
				#'css' : ['i-active' if last == 'settings' else ''],
				#'weight' : 10, # last
			#}).add('Link', {
				#'href' : ''.join(('/nabar/', entity_id, '/edit/settings')),
				#'value' : s('Settings'),
				
			#})


@IN.hook
def page_menu_tab_nabar_anything_after(context):
	
	nabar_id = context.nabar.id
	
	if nabar_id:
		return
	
	tab = context.page_menu_tab
	
	path_parts = context.request.path_parts
	
	parts_len = len(path_parts)
	
	if parts_len == 1:
		second = 'login'
	else:
		second = path_parts[1]
		
		
	tab.add('Li', {
		'css' : ['i-active' if second == 'login' else ''],
		'weight' : 0
	}).add('Link', {
		'href' : '/nabar/login',
		'value' : s('Login'),
	})
	
	tab.add('Li', {
		'css' : ['i-active' if second == 'register' else ''],
		'weight' : 1
	}).add('Link', {
		'href' : '/nabar/register',
		'value' : s('Register'),
	})
	
	tab.add('Li', {
		'css' : ['i-active' if second == 'recover' else ''],
		'weight' : 2
	}).add('Link', {
		'href' : '/nabar/recover',
		'value' : s('Forgot password?'),
	})
	
		
