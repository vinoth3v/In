from collections import OrderedDict

@IN.hook
def access_keys():
	
	keys = {}

	entity_type = 'Comment'
	
	group = 'Entity_' + entity_type
	
	keys[group] = OrderedDict() 			# keep order
	
	keys_entity_type = keys[group]

	# reply
	prefix = '_'.join(('reply', entity_type))
	keys_entity_type[prefix + '_own'] = {
		'title' : s('Allow nabar to reply own ') + entity_type
	}
	keys_entity_type[prefix + '_others'] = {
		'title' : s('Allow nabar to reply other\'s ') + entity_type,
	}

	return keys

@IN.hook
def entity_insert_Comment(entity):
	
	task = Task.new('TaskCommentInsert', {
		'status' : 1,
		'weight' : 10,
		'args' : {
			'container_id' : entity.container_id,
		},
	})
	
	try:
		IN.tasker.add(task)
	except Exception as e:
		IN.logger.debug()
			
@IN.hook
def entity_delete_Comment(entity):
	#recursive comment delete
	
	try:
		cursor = IN.db.select({
			'table' : ['entity.comment', 'c'],
			'columns' : ['id'],
			'where' : [
				['c.parent_id', entity.id]
			]
		}).execute()
		
		if cursor.rowcount == 0:
			# no subs
			return
		
		result = cursor.fetchall()
				
		entity_ids = []
		for r in result:
			entity_ids.append(r[0])
		
		entities = IN.entitier.load_multiple('Comment', entity_ids)
		
		for id, comment in entities.items():
			try:
				comment.__recursive_delete__ = True
				comment.Entitier.delete(comment)
				#addons may invoke hook on each delete
				
			except Exception as e1:
				IN.logger.debug()
	except Exception as e:
		IN.logger.debug()
	
	# don't add for sub delete
	if not hasattr(entity, '__recursive_delete__'):
		# add task comment_insert_delete
		
		task = Task.new('TaskCommentDelete', {
			'status' : 1,
			'weight' : 10,
			'args' : {
				'container_id' : entity.container_id,
			},
		})
		
		try:
			IN.tasker.add(task)
		except Exception as e:
			IN.logger.debug()
			
	


#@IN.hook
#def tasker_task_type():
	#''''''
	#return {
		#'comment_insert_delete' : {
			#'handler' : tasker_handler_comment_insert_delete
		#}
	#}

