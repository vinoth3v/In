

def profile_action_handler_page_profile_edit(context, action, entity_id, profile_bundle, **args):
	
	entitier = IN.entitier
	
	nabar = entitier.load_single('Nabar', entity_id)
	
	if not nabar:
		context.not_found()
	
	logged_in_nabar_id = context.nabar.id
	
	if logged_in_nabar_id == nabar.id:
		context.access('nabar_edit_profile_own', nabar, True)
	else:
		context.access('nabar_edit_profile_other', nabar, True)
	
	if profile_bundle not in entitier.entity_bundle['Profile']:
		context.not_found()
	
	content = Object.new('TextDiv', {
		'css' : ['i-grid i-grid-small'],
	})
	
	tab = content.add('Ul', {
		'css' : ['i-tab i-tab-left i-width-medium-1-4']
	})
	
	if 'Profile' in entitier.entity_bundle:
		profile_config = entitier.entity_bundle['Profile']
		for bundle in sorted(profile_config.keys(), key = lambda o:o):
			bundle_conf = profile_config[bundle]
			tab.add('Li', {
				'css' : ['i-active' if profile_bundle == bundle else '']
			}).add('Link', {
				'value' : bundle_conf['data']['title'],
				'href' : ''.join(('/nabar/', str(entity_id), '/edit/profile/!' + bundle))
			})
	
	
	profile_tab = content.add('TextDiv', {
		'css' : ['i-width-medium-3-4'],
	})
	
	
	# add profile entity edit form
	
	# check if profile exists	
	profiles = In.profile.nabar_profile(nabar.id, profile_bundle)
	
	if profiles:
		form = IN.former.load('ProfileEditForm', args = {
			'data' : {
				'id' : '-'.join(('ProfileEditForm', str(nabar.id))),
				'entity_type' : 'Profile',
				'entity_bundle' : profile_bundle,
				'entity_id' : next(iter(profiles.keys())),
			},
			'nabar_id' : nabar.id,
		})
		profile_tab.add(form)
	else:
		form = IN.former.load('ProfileAddForm', args = {
			'data' : {
				'id' : '-'.join(('ProfileAddForm', str(nabar.id))),
				'entity_type' : 'Profile',
				'entity_bundle' : profile_bundle,
			},
			'nabar_id' : nabar.id,
			'entity_type' : 'Profile',
			'entity_bundle' : profile_bundle,			
		})
		profile_tab.add(form)
		
	context.response.output.add(content)
	
