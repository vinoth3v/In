
class Vakaigal:
	'''Vakai engine'''
	
	
	def find_by_title(self, title, bundle):
		'''return vakai that havs title title'''
		
		try:
		
			db = IN.db
			connection = db.connection

			limit = 10
			
			# TODO: make it dynamic
			cursor = db.execute('''SELECT 
				field_vakai_title.entity_id
			FROM
				field.field_vakai_title
			JOIN 
				config.vakai ON field_vakai_title.entity_id = vakai.id 
			WHERE
				vakai.type = %(vakai_bundle)s AND
				vakai.status > 0 AND
				field_vakai_title.value = %(title)s
			LIMIT 1
			''', {
				'vakai_bundle' : bundle,
				'title' : title
			})
			
			if cursor.rowcount > 0:
				id = cursor.fetchone()['entity_id']
				
				vakai = IN.entitier.load_single('Vakai', id)
				return vakai
		except Exception as e:
			IN.logger.debug()
			
