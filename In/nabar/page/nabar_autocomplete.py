
def nabar_action_handler_nabar_autocomplete(context, action = None, query = '', **args):
	''''''
	results = []
	
	query = query.replace('%', '').replace("'", '')
	
	try:
		
		db = IN.db
		connection = db.connection

		limit = 10
		
		# TODO: make it dynamic
		cursor = db.execute('''SELECT 
				n.id, 
				n.name, 
				string_agg(l.value, ',') AS emails, 
				string_agg(l2.value, ',') AS names
			FROM 
				account.nabar n
			LEFT JOIN account.login l ON n.nabar_id = l.nabar_id and l.type = 'email'
			LEFT JOIN account.login l2 ON n.nabar_id = l2.nabar_id and l2.type = 'name'
			WHERE 
				n.status > 0 AND
				l.status > 0 AND
				(
					n.name like %(query)s OR
					l.value like %(query)s OR
					l2.value like %(query)s
				)
			GROUP BY n.id
			LIMIT %(limit)s
				''', {
			'limit' : limit,
			'query' : query.join(('%', '%'))
		})
		
		if cursor.rowcount >= 0:
			for row in cursor:
				names = set()
				for name in row['names'].split(','):
					names.add(name)
				for name in row['emails'].split(','):
					names.add(name)
				results.append({
					'id' : row['id'],
					'text' : '<h3>' + row['name'] + '</h3> ' + ', '.join(names),
					'item' : row['name']
				})
				
	except:
		IN.logger.debug()
	
	context.response = In.core.response.JSONResponse(output = results)
	