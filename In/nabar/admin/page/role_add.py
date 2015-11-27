
def action_admin_nabar_role_add(context, action, **args):
	# TODO: ADMIN ACCESS
	
	IN.context.access('admin_nabar_role_access', deny = True)
	
	frm = IN.former.load('FormNabarRoleAddAdmin')
	context.response.output.add(frm)
