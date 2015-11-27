
def nabar_action_handler_page_edit_password(context, action, entity_id, **args):
	
	entitier = IN.entitier
	
	nabar = entitier.load_single('Nabar', entity_id)
	
	if not nabar:
		context.not_found()
	
	logged_in_nabar_id = context.nabar.id
	
	if logged_in_nabar_id == nabar.id:
		context.access('nabar_edit_password_own', nabar, True)
	else:
		context.access('nabar_edit_password_other', nabar, True)
	
	
	hashes = entitier.select('NabarHash', [['nabar_id', entity_id]])
	
	output = []
	if hashes: # TODO: SECURITY
		output.append(
	''.join(('''<br><div class="i-clearfix i-nbfc">
		<ul class="i-subnav">
			<li><a href="/nabar/''', str(entity_id), '/edit/password/new/form"><i class="i-icon-plus-circle"></i> ', s('Add new password'), '''</a></li>
		</ul>
		<div id="nabar-password-new-form"></div>
	</div>''')))
	
	output.append('''<div class="i-clearfix i-nbfc">
	<table class="i-table">''')
	
	output.append(s('Password').join(('<tr><th>', '</th><th></th></tr>')))
	
	for id, pwd in hashes.items():
		
		hashints = pwd.hint.split('|')
		
		if len(hashints) == 2:
			hashints = '******'.join((hashints[0], hashints[1]))
		else:
			hashints = '********'
		
		output.append(''.join(('<tr><td><div id="nabar-password-edit-', str(id),'">', hashints, '</div></td>')))
		output.append(''.join(('<td><a href="/nabar/', str(entity_id), '/edit/password/', str(id), '/form">', s('Change password'), '</a></td></tr>')))
	
	output.append('</table></div>')
	
	context.response.output.add('TextDiv', {
		'value' : ''.join(output)
	})
	
