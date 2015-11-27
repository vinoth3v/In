def nabar_register(context, action, **args):
	# if already logged in
	if context.nabar.id > 0 :
		context.redirect('/')

	frm = IN.former.load('FormRegister')
	context.response.output.add(frm)
