

def nabar_login(context, action, **args):
	
	# if already logged in
	if context.nabar.id > 0 :
		context.redirect('/nabar/' + str(context.nabar.id))
		
	context.ensure_page_response()

	frm = IN.former.load('FormLogin')
	context.response.output.add(frm)
