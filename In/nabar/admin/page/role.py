
def action_admin_nabar_role(context, action, **args):
	# TODO: ADMIN ACCESS
	
	IN.context.access('admin_nabar_role_access', deny = True)
	
	frm = IN.former.load('FormNabarRoleAdmin')
	context.response.output.add(frm)
	
	# add form
	frm = IN.former.load('FormNabarRoleAddAdmin')
	context.response.output.add(frm)
