
def action_admin_nabar_role_access(context, action, group = 'general', **args):
	# TODO: ADMIN ACCESS

	IN.context.access('admin_nabar_role_access', deny = True)
	
	frm = IN.former.load('FormNabarRoleAccessAdmin', args = {'group' : group})

	page = context.response.output
	
	page.add(frm)

	# add role box
	role_box = IN.boxer.load_box('BoxAdminNabarRoleAccessGroup')
	page.add(role_box, panel = 'sidebar1')
