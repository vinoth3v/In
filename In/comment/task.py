

class TaskCommentInsert(Task):
	''''''
	
	def run(self):
		args = self.args
		container_id = args['container_id']
		
		try:
			
			cursor = IN.db.select({
				'table' : ['entity.comment', 'c'],
				'columns' : ['id'],
				'where' : [
					['c.container_id', container_id],
					['status', '>', 0]
				]
			}).execute_count()
			
			if cursor.rowcount == 0:
				count = 0
			else:
				count = cursor.fetchone()[0]
			
			try:

				db = IN.db
				connection = db.connection
				
				cursor = db.update({
					'table' : 'entity.comment_container',
					'set' : [
						['total_comments', count]
					],
					'where' : [
						['id', container_id]
					]
				}).execute()
				
				connection.commit()
				
				
			except Exception as e1:
				connection.rollback()
				IN.logger.debug()
			
		except Exception as e:
			IN.logger.debug()


class TaskCommentDelete(TaskCommentInsert):
	''''''
	