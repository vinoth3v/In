
import datetime

@IN.hook
def ws_action_me(context, message):
	
	try:
		context.send({
			'ws_command' : 'me',
			'nabar' : {
				'id' : context.nabar.id,
				'name' : context.nabar.name
			}
		})
	except Exception as e:
		IN.logger.debug()
	
	
	
	try:
		
		now = datetime.datetime.now()
		nabar_id = context.nabar.id
		
		# update
		cursor = IN.db.update({
			'table' : 'log.nabar_active',
			'set' : [
				['active', now]
			],
			'where' : [
				['nabar_id', nabar_id]
			]
		}).execute()
		
		if cursor.rowcount == 0:
			# insert
			cursor = IN.db.insert({
				'table' : 'log.nabar_active',
				'columns' : ['nabar_id', 'active'],
			}).execute([
				[nabar_id, now]
			])
		
		IN.db.connection.commit()
		
	except Exception as e:
		IN.logger.debug()
	