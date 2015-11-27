
class VakaiListLazy(In.core.lazy.HTMLObjectLazy):
	'''list of vakais'''

	def __init__(self, data = None, items = None, **args):

		super().__init__(data, items, **args)
		
		parent_entity_type = self.parent_entity_type
		parent_entity_bundle = self.parent_entity_bundle
		parent_entity_id = self.parent_entity_id
		
		#parent_field_name = In.vakai.Entitier.parent_field_name
		
		# always set new id
		self.id = '_'.join(('VakaiListLazy', parent_entity_type, parent_entity_bundle, str(parent_entity_id)))
		
		if IN.context.request.ajax_lazy:
			
			db = IN.db
			connection = db.connection

			# TODO: paging
			# get total
			total = 0
			limit = 10
			# TODO: make it dynamic
			cursor = db.execute('''SELECT 
				  count(field_vakai_parent.value)
				FROM 
				  field.field_vakai_parent,
				  config.vakai
				WHERE
				  vakai.type = %(parent_entity_bundle)s AND
				  field_vakai_parent.entity_id = vakai.id AND
				  field_vakai_parent.value = %(parent_id)s AND
				  vakai.status > 0
				''', {
					'parent_entity_bundle' : parent_entity_bundle,
					'parent_id' : parent_entity_id
				})
			
			if cursor.rowcount >= 0:
				total = int(cursor.fetchone()[0])
			
			if total > 0:
				cursor = db.execute('''SELECT 
					  field_vakai_parent.entity_type, 
					  field_vakai_parent.entity_id, 
					  field_vakai_parent.value
					FROM 
					  field.field_vakai_parent,
					  config.vakai
					WHERE
					  vakai.type = %(parent_entity_bundle)s AND
					  field_vakai_parent.entity_id = vakai.id AND
					  field_vakai_parent.value = %(parent_id)s AND
					  vakai.status > 0
					ORDER BY 
					  vakai.weight
					''', {
					'parent_entity_bundle' : parent_entity_bundle,
					'parent_id' : parent_entity_id
				})
				
				ids = []
				last_id = 0
				if cursor.rowcount >= 0:
					for row in cursor:
						# reverse reference
						ids.append(row['entity_id'])

					last_id = ids[-1] # last id

					vakais = IN.entitier.load_multiple('Vakai', ids)
					
					for id, vakai in vakais.items():
						obj = ThemeArgs(vakai, {'view_mode' : 'adminlist'})
						self.add(obj)
	
				remaining = total - limit
				if remaining > 0 and  last_id > 0:
					self.add('TextDiv', {
						'id' : '_'.join(('more-vakais', parent_entity_type, str(parent_entity_id))),
						'value' : str(remaining) + ' more...',
						'css' : ['ajax i-text-center pointer i-panel-box i-panel-box-primary'],
						'attributes' : {
							'data-href' : ''.join(('/vakai/more/!', str(parent_entity_bundle), '/', str(last_id), '/', str(parent_entity_id)))
						},
						'weight' : -1
					})

		self.css.append('vakai-list')

@IN.register('VakaiListLazy', type = 'Themer')
class VakaiListLazyThemer(In.core.lazy.HTMLObjectLazyThemer):
	'''lazy themer'''

