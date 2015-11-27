
def nabar_recover(context, action, **args):
	# if already logged in
	if context.nabar.id > 0 :
		context.redirect('/')

	frm = IN.former.load('FormRecover')
	context.response.output.add(frm)
