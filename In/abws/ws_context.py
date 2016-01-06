import json
from In.core.context import Context
from autobahn.asyncio.websocket import WebSocketServerProtocol


class WSContext(Context, WebSocketServerProtocol):
	'''Websocket context'''
	
	def __init__(self, app, **args):
		''''''
		
		dummy = lambda: None
		
		Context.__init__(self, app, {}, dummy, **args)
		WebSocketServerProtocol.__init__(self)
		
		self.messages = []
		
	def onConnect(self, request):
		#print("Client connecting: {}".format(request.peer))
		
		self.ws_request = request
		
		#print('headers', request.headers)
		'''{
			'dnt': '1', 
			'sec-websocket-version': '13', 
			'accept-language': 'en-US,en;q=0.5', 
			'cache-control': 'no-cache', 
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
			'sec-websocket-key': 'MkMq9r30jDdODq1vkApmmQ==', 
			'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0', 
			'connection': 'upgrade', 
			'pragma': 'no-cache', 
			'accept-encoding': 'gzip, deflate', 
			'upgrade': 'websocket', 
			'host': 'In.linux.local', 
			'x-forwarded-for': '127.0.0.1', 
			'origin': 'http://In.linux.local', 
			'cookie': 'k=v', 
			'sec-websocket-extensions': 'permessage-deflate'
		}
		
		'''
		# TODO: init nabar, environ
		
		# always set
		self.environ['SERVER_PORT'] = 80
		self.environ['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'	# ajax on
		
		self.environ['HTTP_HOST'] = request.headers.get('host', '')
		self.environ['HTTP_X_FORWARDED_FOR'] = request.headers.get('x-forwarded-for', '')
		self.environ['HTTP_COOKIE'] = request.headers.get('cookie', '')
		self.environ['HTTP_USER_AGENT'] = request.headers.get('user-agent', '')
		self.environ['HTTP_ACCEPT'] = request.headers.get('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		
		self.environ['sec-websocket-key'] = request.headers.get('sec-websocket-key', '')
		self.environ['sec-websocket-version'] = request.headers.get('sec-websocket-version', '')
		self.environ['sec-websocket-extensions'] = request.headers.get('sec-websocket-extensions', '')
		
		# init cookie		
		self.request.init_cookie(self.environ['HTTP_COOKIE'])
		
		# init nabar
		nabar = None
		
		try:
			
			# ignore nabar for static files path
			nabar_id = IN.nabar.auth_cookie(self)

			if nabar_id:
				nabar = IN.entitier.load('Nabar', nabar_id)
				
				if nabar_id in IN.APP.contexts:
					IN.APP.contexts[nabar_id].append(self)
				else:
					IN.APP.contexts[nabar_id] = [self]
				
		except Exception as e:
			IN.logger.debug()
			
		if nabar is None: # use the default
			nabar = In.nabar.anonymous()

		self.nabar = nabar
		
		# set json response
		self.response = In.core.response.JSONResponse(output = {})
		
	def onMessage(self, payload, isBinary):
		## echo back message verbatim
		#print('message from client', payload, isBinary)
		#res = 'nabar id :' + str(self.nabar.id)
		#res = res.encode('utf-8')
		#self.sendMessage(res, isBinary)
		try:
			if not isBinary:
				message = payload.decode('utf-8')
				if message == '{}':
					return
				
				message = json.loads(message)
				
				if 'ws_action' not in message:
					return
				
				self.messages.append(message)
				
				#IN.APP.remaining_messages += 1
				
				# switch to this greenlet
				#IN.__context__ = self
				self.switch()
				#self.run()
				#IN.__context__ = None
				
		except Exception as e:
			IN.logger.debug()
			
	def run(self):
		''''''
		# TODO: ws context switch
		while True:
			
			for message in self.messages:
				# process all messages
				IN.hook_invoke('ws_action_' + message['ws_action'], self, message)
				
				#IN.APP.remaining_messages -= 1
				
			# all messages processed
			self.messages = []
			
			self.parent.switch()
			#IN.APP.switch()
		
		
	def send(self, dict):
		'''send a dict as messsage'''
		
		try:
			message = json.dumps(dict, skipkeys = True, ensure_ascii = False)
			message = message.encode('utf-8')
			self.sendMessage(message, False)		
		except Exception as e:
			IN.logger.debug()
		
	#def onOpen(self):
		#print("WebSocket connection open.")
		#self.sendMessage(b'{"hi" : "client"')
	
	def onClose(self, wasClean, code, reason):
		#print('client closed', code, reason)
		
		# inbuilt by autobahn
		#self.factory = None
		
		nabar_id = self.nabar.id
		if nabar_id in IN.APP.contexts:
			try:
				IN.APP.contexts[nabar_id].remove(self)
			except Exception as e:
				pass
			
		IN.APP.context_pool.free(self)
	
