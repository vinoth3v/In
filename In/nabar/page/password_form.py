

def nabar_action_handler_page_edit_password_form(context, action, entity_id, hash_id, **args):
	
	entitier = IN.entitier
	
	nabar = entitier.load_single('Nabar', entity_id)
	if not nabar:
		context.not_found()
	
	hash = entitier.load_single('NabarHash', hash_id)
	
	if not hash:
		context.not_found()
	
	if hash.nabar_id != nabar.id:
		context.not_found()
	
	logged_in_nabar_id = context.nabar.id
	
	if logged_in_nabar_id == nabar.id:
		context.access('nabar_edit_password_own', nabar, True)
	else:
		context.access('nabar_edit_password_other', nabar, True)
	
	form = IN.former.load('NabarEditPassword', args = {
		'data' : {'id' : '-'.join(('NabarEditPassword', str(nabar.id), str(hash.id)))},
		'hash_id' : hash.id,
		'nabar_id' : nabar.id
	})
	element_id = '#nabar-password-edit-' + str(hash.id)
	
	output = [
		{'method' : 'html', 'args' : [element_id, IN.themer.theme(form)]},
	]
	
	context.response = In.core.response.CustomResponse(output = output)



def nabar_action_handler_page_new_password_form(context, action, entity_id, **args):
	
	entitier = IN.entitier
	
	nabar = entitier.load_single('Nabar', entity_id)
	if not nabar:
		context.not_found()
	
	logged_in_nabar_id = context.nabar.id
	
	if logged_in_nabar_id == nabar.id:
		context.access('nabar_edit_password_own', nabar, True)
	else:
		context.access('nabar_edit_password_other', nabar, True)
	
	form = IN.former.load('NabarNewPassword', args = {
		'data' : {'id' : '-'.join(('NabarNewPassword', str(nabar.id)))},
		'nabar_id' : nabar.id
	})
	element_id = '#nabar-password-new-form'
	
	output = [
		{'method' : 'html', 'args' : [element_id, IN.themer.theme(form)]},
	]
	
	context.response = In.core.response.CustomResponse(output = output)
