from collections import OrderedDict

@IN.hook
def access_keys():

	group = 'nabar'
	
	keys = {
		group : OrderedDict()
	}

	keys[group]['admin_nabar_role_access'] = {
		'title' : s('(Administer) Allow nabar to manage nabar roles and access'),
		'flag' : 'danger',
	}
	
	keys[group]['nabar_edit_password_own'] = {
		'title' : s('(warning) Allow nabar to manage own password'),
		'flag' : 'warning',
	}
	keys[group]['nabar_edit_password_other'] = {
		'title' : s('(danger) Allow nabar to manage others password'),
		'flag' : 'danger',
	}
	
	keys[group]['nabar_edit_login_own'] = {
		'title' : s('(warning) Allow nabar to manage own login'),
		'flag' : 'warning',
	}
	keys[group]['nabar_edit_login_other'] = {
		'title' : s('(danger) Allow nabar to manage others login'),
		'flag' : 'danger',
	}
	
	keys[group]['nabar_edit_profile_own'] = {
		'title' : s('(warning) Allow nabar to manage own profile'),
		'flag' : 'warning',
	}
	keys[group]['nabar_edit_profile_other'] = {
		'title' : s('(danger) Allow nabar to manage others profile'),
		'flag' : 'danger',
	}
	
	return keys
