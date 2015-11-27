from In.core.application import Application
from autobahn.asyncio.websocket import WebSocketServerFactory

class WSApplication(WebSocketServerFactory, Application):
	
	
	def __init__(self, config_file):
		
		# init before get called
		self.contexts = {}
		self.context_subscriptions = {}
		
		Application.__init__(self, config_file)
		WebSocketServerFactory.__init__(self)
		
		#greenlet.greenlet.__init__(self)
		
		# start the separate tasker process
		IN.tasker.start_the_process()
		
		#self.tasker_context = IN.tasker.tasker_context(self) # pass self/app
		
		#self.remaining_messages = 0
		
	def __call__(self):
		
		# create context
		protocol = In.abws.WSContext(self)
		protocol.factory = self
		
		self.context_pool.put(protocol)
		
		return protocol

	
	#def run(self):
		#'''greenlet custom switch'''
		
		#while True:
			
			#if not self.remaining_messages:
				#self.tasker_context.switch()
		
			## switch to parent
			#IN.context.parent.switch()
		
