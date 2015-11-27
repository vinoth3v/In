
def action_vakai_autocomplete(context, action, vakai_bundle, query, **args):
	
	vakais = []
	
	query = query.replace('%', '').replace("'", '')
	
	try:
		
		db = IN.db
		connection = db.connection

		limit = 10
		
		# TODO: make it dynamic
		cursor = db.execute('''SELECT 
			field_vakai_title.value, 
			field_vakai_title.entity_id,
			vakai.weight
		FROM
			field.field_vakai_title
		JOIN 
			config.vakai ON field_vakai_title.entity_id = vakai.id 
		WHERE
			vakai.type = %(vakai_bundle)s AND
			vakai.status > 0 AND
			field_vakai_title.value LIKE %(query)s
		ORDER BY
			field_vakai_title.value
		LIMIT %(limit)s
				''', {
			'vakai_bundle' : vakai_bundle,
			'limit' : limit,
			'query' : query.join(('%', '%'))
		})
		
		if cursor.rowcount >= 0:
			for row in cursor:		
				vakais.append({
					'id' : row['entity_id'],
					'text' : row['value']
				})
				
	except:
		IN.logger.debug()
	
	context.response = In.core.response.JSONResponse(output = vakais)
	