import random
import datetime


@IN.hook
def actions():

	actns = {}
	# verify token, register, email, ...
	actns['token/verify/{token_type}/{token}'] = {
		'handler' : action_handler_token_verification,
	}

	return actns

def action_handler_token_verification(context, action, token_type, token):
	'''verify if token is right one?'''

	db = IN.db
	try:
		
		data = token_valid(token, token_type)
		if not data:
			IN.context.bad_request()
			return

		# find action handler for this token_type
		result = IN.hook_invoke('_'.join(('token', token_type, 'verification')), context, action, data)

		# delete this token if processed
		for res in result:
			if res:			# some module processed it
				cursor = db.delete({
					'table' : 'log.token',
					'where' : [
						['token', token],
						['type', 'register']
					],
				}).execute()
				
				db.connection.commit()
				
	except Exception as e:
		IN.logger.debug()

def token_valid(token, token_type):
	
	try:
		
		db = IN.db
		
		cursor = db.execute('''SELECT data, expire FROM log.token
		WHERE
			type = %(type)s and token = %(token)s
		''', {
			'type' : token_type,
			'token' : token,
		})
		if cursor.rowcount != 1:
			#print('token not found')
			return False

		result = cursor.fetchone()
		expire = result['expire']

		if expire < datetime.datetime.now(): # expired
			#print('token expired')
			return False

		return result['data']
		
	except Exception as e:
		IN.logger.debug()
		

def create_random_token():
	return random.getrandbits(128)
