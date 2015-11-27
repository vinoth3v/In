
def nabar_action_handler_page_edit_login(context, action, entity_id, **args):
	
	entitier = IN.entitier
	
	nabar = entitier.load_single('Nabar', entity_id)
	
	if not nabar:
		context.not_found()
	
	logged_in_nabar_id = context.nabar.id
	
	if logged_in_nabar_id == nabar.id:
		context.access('nabar_edit_login_own', nabar, True)
	else:
		context.access('nabar_edit_login_other', nabar, True)
	
	
	logins = IN.entitier.select('NabarLogin', [['nabar_id', entity_id]])
	
	text = s('''You can use any of these following logins to login in to the site!''')
	
	output = [text.join(('<div class="i-alert i-alert-success"><i class="i-icon-info-circle"></i> ', '</div>'))]
	
	output.append('<table class="i-table">')
	
	output.append(''.join(('<tr><th>', s('Login'), '</th><th>', s('Type'), '</th><th></th></tr>')))
	
	for id, login_entity in logins.items():
		
		confirmed = ''
		if login_entity.status <= 0:
			confirmed = s('not confirmed').join(('(<em>', '</em>)'))
			
		output.append(''.join(('<tr><td><div id="nabar-login-edit-', str(id),'">', login_entity.value, ' ', confirmed, '</div></td>')))
		output.append(''.join(('<td><div id="nabar-login-edit-', str(id),'">', login_entity.type, '</div></td>')))
		#output.append(''.join(('<td><a href="/nabar/', str(entity_id), '/edit/login/', str(id), '/form">', s('Change login'), '</a></td></tr>')))
	
	output.append('</table>')
	
	context.response.output.add('TextDiv', {
		'value' : ''.join(output)
	})
	
