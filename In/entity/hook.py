

@IN.register
def register():
	'''
	instance :
		class - class type assigned directly
		instance - instance will be created and assigned, all object will use the same member instance
	'''
	return {
		# all entity type class should have Entitier member of type which is
		'class_members' : {								# register for
			'Entity' : {								# type of object - arg to class members
				'Entitier' : {						# key
					'name' : 'Entitier',				# member name
					'instance' : 'instance',			# type of instance
				},
				'Model' : {							# key
					'name' : 'Model',					# member name
					'instance' : 'instance',			# type of instance
				},
				'EntityAddForm' : {					# key
					'name' : 'EntityAddForm',			# member name
					'instance' : 'class',				# type of instance
				},
				'EntityEditForm' : {				# key
					'name' : 'EntityEditForm',			# member name
					'instance' : 'class',				# type of instance
				},
				'EntityDeleteForm' : {				# key
					'name' : 'EntityDeleteForm',		# member name
					'instance' : 'class',				# type of instance
				},
			},
		},
	}
