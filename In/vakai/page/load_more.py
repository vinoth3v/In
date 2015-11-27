
def action_vakai_load_more(context, action, parent_entity_bundle, last_id, parent_entity_id, **args):

	try:
		
		parent_entity_type = 'Vakai'
		
		parent_entity_id = int(parent_entity_id)
		
		last_id = int(last_id)
		
		output = Object()
		
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
			  field.field_vakai_parent
			JOIN
			  config.vakai ON field_vakai_parent.entity_id = vakai.id 
			WHERE
			  vakai.type = %(parent_entity_bundle)s AND
			  field_vakai_parent.value = %(parent_id)s AND
			  vakai.id < %(last_id)s AND
			  vakai.status != 0
			''', {
				'parent_entity_bundle' : parent_entity_bundle,
				'parent_id' : parent_entity_id,
				'last_id' : last_id,
			})
		
		if cursor.rowcount >= 0:
			total = int(cursor.fetchone()[0])
		
		more_id = '_'.join(('more-vakais', parent_entity_type, str(parent_entity_id)))
		
		if total > 0:
			cursor = db.execute('''SELECT 
				  field_vakai_parent.entity_type, 
				  field_vakai_parent.entity_id, 
				  field_vakai_parent.value,
				  vakai.weight
				FROM 
				  field.field_vakai_parent
			    JOIN 
				  config.vakai ON field_vakai_parent.entity_id = vakai.id 
				WHERE
				  vakai.type = %(parent_entity_bundle)s AND
				  field_vakai_parent.value = %(parent_id)s AND
				  vakai.id < %(last_id)s AND
				  vakai.status != 0
				ORDER BY 
				  vakai.weight
				LIMIT %(limit)s
				''', {
				'parent_entity_bundle' : parent_entity_bundle,
				'parent_id' : parent_entity_id,
				'last_id' : last_id,
				'limit' : limit,
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
					output.add(obj)

			remaining = total - limit
			if remaining > 0 and  last_id > 0:
				output.add('TextDiv', {
					'id' : more_id,
					'value' : str(remaining) + ' more...',
					'css' : ['ajax i-text-center pointer i-panel-box i-panel-box-primary'],
					'attributes' : {
						'data-href' : ''.join(('/vakai/more/!', str(parent_entity_bundle), '/', str(last_id), '/', str(parent_entity_id)))
					},
					'weight' : -1
				})
		
		output = {more_id : output}
		context.response = In.core.response.PartialResponse(output = output)
		
	except:
		IN.logger.debug()