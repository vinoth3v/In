
def nabar_logout(context, action = None, **args):

	IN.nabar.logout(context, action, **args)
	
	context.redirect(IN.APP.config.logout_path)
