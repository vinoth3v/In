from collections import OrderedDict

@IN.hook
def access_keys():
	
	entity_bundle = IN.entitier.entity_bundle
	keys = {}

	group = 'Entity Admin'
	keys[group] = OrderedDict()	# we may need order
	keys_entity_type = keys[group]

	# administer all entities
	keys_entity_type['admin_all_entity'] = {
		'title' : s('(Administer) Allow nabar to do ANY ACTION on all site Entities'),
		'flag' : 'danger',
	}
	
	for entity_type, bundles in entity_bundle.items():
		
		#entity_type = entity_type.lower()			# lower case
		group = 'Entity_' + entity_type
		keys[group] = OrderedDict() 			# keep order
		
		keys_entity_type = keys[group]

		for entity_bundle in bundles:

			bundle_of_entity = s('{entity_bundle} of type {entity_type}', {
				'entity_type' : entity_type,
				'entity_bundle' : entity_bundle
			})
		
			#entity_bundle =  entity_bundle.lower()

			# add / create
			prefix = '_'.join(('add', entity_type, entity_bundle))
			keys_entity_type[prefix] = {
				'title' : s('Allow nabar to add/create ') + bundle_of_entity
			}
			
			# view
			prefix = '_'.join(('view', entity_type, entity_bundle))
			keys_entity_type[prefix + '_own'] = {
				'title' : s('Allow nabar to view own ') + bundle_of_entity
			}
			keys_entity_type[prefix + '_others'] = {
				'title' : s('Allow nabar to view other\'s ') + bundle_of_entity
			}
			keys_entity_type[prefix + '_own_unpublished'] = {
				'title' : s('Allow nabar to view own unpublished ') + bundle_of_entity
			}
			keys_entity_type[prefix + '_others_unpublished'] = {
				'title' : s('Allow nabar to view other\'s unpublished ') + bundle_of_entity
			}
			
			# edit / update
			prefix = '_'.join(('edit', entity_type, entity_bundle))
			keys_entity_type[prefix + '_own'] = {
				'title' : s('Allow nabar to edit own ') + bundle_of_entity
			}
			keys_entity_type[prefix + '_others'] = {
				'title' : s('Allow nabar to edit other\'s ') + bundle_of_entity,
				'flag' : 'warning',
			}
			keys_entity_type[prefix + '_own_unpublished'] = {
				'title' : s('Allow nabar to edit own unpublished ') + bundle_of_entity
			}
			keys_entity_type[prefix + '_others_unpublished'] = {
				'title' : s('Allow nabar to edit other\'s unpublished ') + bundle_of_entity,
				'flag' : 'warning',
			}
			
			# delete
			prefix = '_'.join(('delete', entity_type, entity_bundle))
			keys_entity_type[prefix + '_own'] = {
				'title' : s('Allow nabar to delete own ') + bundle_of_entity
			}
			keys_entity_type[prefix + '_others'] = {
				'title' : s('Allow nabar to delete other\'s ') + bundle_of_entity,
				'flag' : 'danger',
			}
			keys_entity_type[prefix + '_own_unpublished'] = {
				'title' : s('Allow nabar to delete own unpublished ') + bundle_of_entity
			}
			keys_entity_type[prefix + '_others_unpublished'] = {
				'title' : s('Allow nabar to delete other\'s unpublished ') + bundle_of_entity,
				'flag' : 'danger',
			}

			# admin
			prefix = '_'.join(('admin', entity_type, entity_bundle))
			keys_entity_type[prefix] = {
				'title' : s('(Administer) Allow nabar to do ANY ACTION on all ') + bundle_of_entity,
				'flag' : 'danger',
			}

		# administer entity_type
		keys_entity_type['admin_' + entity_type] = {
			'title' : s('(Administer) Allow nabar to do ANY ACTION on all type of ') + entity_type,
			'flag' : 'danger',
		}
		
	return keys
