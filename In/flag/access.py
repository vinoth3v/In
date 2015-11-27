from collections import OrderedDict

@IN.hook
def access_keys():
	
	entitier = IN.entitier
	
	# flagger not available here
	#flagger = IN.flagger
	
	keys = {}

	group = 'Flag'
	keys[group] = OrderedDict()	# we may need order
	keys_entity_type = keys[group]

	# flag any entities
	keys_entity_type['flag'] = {
		'title' : s('(Administer) Allow ANY flag on ANY site Entities'),
		'flag' : 'danger',
	}
	
	types = IN.entitier.load_all('FlagType')
	
	if types is None:
			return
		
		
	for id, flag_type in types.items():
		
		data = flag_type.data
		entity_bundle = data.get('entity_bundle', {})
		
		for entity_type, entity_bundles in entity_bundle.items():
			
			group = 'Flag_' + entity_type
			keys[group] = OrderedDict() 			# keep order
			
			keys_entity_type = keys[group]
			
			prefix = '_'.join(('flag', entity_type))
			
			keys_entity_type[prefix] = {
				'title' : s('(Administer) Allow ANY flag on {entity_type} Entities', {'entity_type' : entity_type}),
				'flag' : 'warning',
			}
			
			if '*' in entity_bundles:
				# add all
				if entity_type not in entitier.entity_bundle:
					# entity not found
					break
			
				bundles = sorted(entitier.entity_bundle[entity_type].keys(), key = lambda o:o)
				
			else:
				
				bundles = entity_bundles
				
			for entity_bundle in bundles:
				
				bundle_of_entity = s('{entity_bundle} of type {entity_type}', {
					'entity_type' : entity_type,
					'entity_bundle' : entity_bundle
				})
				
				prefix = '_'.join(('flag', entity_type, entity_bundle, flag_type.type))
				keys_entity_type[prefix] = {
					'title' : s('Allow flag on ') + bundle_of_entity
				}
				
				statuses = data.get('flag_status', [])
				
				for status in statuses:
					key = status[0]
					prefix = '_'.join(('flag', entity_type, entity_bundle, flag_type.type, key))
					keys_entity_type[prefix] = {
						'title' : s('Allow flag {flag_status} on ', {'flag_status' : key}) + bundle_of_entity
					}

	return keys
