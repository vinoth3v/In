
def nabar_action_handler_page_profile(context, action, entity_id, **args):
	
	entitier = IN.entitier
	
	nabar = entitier.load_single('Nabar', entity_id)
	
	if not nabar:
		context.not_found()
	
	logged_in_nabar_id = context.nabar.id
	
	if logged_in_nabar_id == nabar.id:
		context.access('nabar_edit_profile_own', nabar, True)
	else:
		context.access('nabar_edit_profile_other', nabar, True)
	
	content = Object.new('TextDiv', {
		'css' : ['i-grid i-grid-small'],
	})
	
	
	if context.request.path_parts[4] == '_general':
		general_tab = True
	else:
		general_tab = False
	
	tab = content.add('Ul', {
		'css' : ['i-tab i-tab-left i-width-medium-1-4']
	})
	
	tab.add('Li', {
		'weight' : -1,
		'css' : ['i-active' if general_tab else ''],
	}).add('Link', {
		'value' : s('General'),
		'href' : ''.join(('/nabar/', str(entity_id), '/edit/profile/_general'))
	})
	
	if 'Profile' in entitier.entity_bundle:
		for bundle, bundle_conf in entitier.entity_bundle['Profile'].items():
			tab.add('Li').add('Link', {
				'value' : bundle,
				'href' : ''.join(('/nabar/', str(entity_id), '/edit/profile/!' + bundle))
			})
	
	
	profile_tab = content.add('TextDiv', {
		'css' : ['i-width-medium-3-4'],
	})
	
	if general_tab:
		# add custom profile edit for nabar entity
		form = IN.former.load('NabarGeneralProfileForm', args = {
			'data' : {'id' : '-'.join(('NabarGeneralProfileForm', str(nabar.id)))},
			'nabar_id' : nabar.id
		})
		profile_tab.add(form)
	else:
		# add profile entity edit form
		# check if profile exists
		#profiles = IN.nabar.nabar_profile(nabar, )
		pass
		
	context.response.output.add(content)
	
