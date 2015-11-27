def action_comment_load_more(context, action, entity_type, entity_id, last_id, parent_id, **args):

	try:

		entity = IN.entitier.load_single(entity_type, int(entity_id))

		if not entity:
			return
		
		output = Object()

		db = IN.db
		connection = db.connection

		container_id = IN.commenter.get_container_id(entity)
		
		# TODO: paging
		# get total
		total = 0
		limit = 10
		cursor = db.select({
			'table' : 'entity.comment',
			'columns' : ['count(id)'],
			'where' : [
				['container_id', container_id],
				['id', '<', int(last_id)],		# load previous
				['parent_id', parent_id],
				['status', 1],
			],
		}).execute()
		if cursor.rowcount >= 0:
			total = int(cursor.fetchone()[0])
		
		
		more_id = '_'.join(('more-commens', entity_type, str(entity_id), str(parent_id)))
		
		if total > 0:

			cursor = db.select({
				'table' : 'entity.comment',
				'columns' : ['id'],
				'where' : [
					['container_id', container_id],
					['id', '<', int(last_id)],
					['parent_id', parent_id],				# add main level comments only
					['status', 1],
				],
				'order' : {'created' : 'DESC'},
				'limit'	: limit,
			}).execute()

			ids = []
			last_id = 0
			if cursor.rowcount >= 0:
				for row in cursor:
					ids.append(row['id'])

				last_id = ids[-1]	# last id
				
				comments = IN.entitier.load_multiple('Comment', ids)

				for id, comment in comments.items():
					comment.weight = id	# keep asc order
					output.add(comment)

			remaining = total - limit
			
			if remaining > 0 and last_id > 0:
				output.add('TextDiv', {
					'id' : more_id,
					'value' : str(remaining) + ' more comments',
					'css' : ['ajax i-text-center i-text-danger pointer'],
					'attributes' : {
						'data-href' : ''.join(('/comment/more/!Content/', str(entity_id), '/', str(last_id), '/', str(parent_id)))
					},
					'weight' : -1,
				})
				
		#if not output:
			#output.add(type = 'TextDiv', data = {})
			
		output = {more_id : output}
		context.response = In.core.response.PartialResponse(output = output)
		
	except:
		IN.logger.debug()
