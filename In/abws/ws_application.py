from In.core.application import Application
from autobahn.asyncio.websocket import WebSocketServerFactory

#import tracemalloc

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
		
		#self.a = 0
		
		#tracemalloc.start()
		
	def __call__(self):
		
		
		#try:
			
			#self.a += 1
			
			#if self.a == 5:
				#self.snapshot = tracemalloc.take_snapshot()
			#if self.a == 10:
				#snapshot2 = tracemalloc.take_snapshot()

				#top_stats = snapshot2.compare_to(self.snapshot, 'lineno')

				#print("[ Top 10 differences ]")
				#for stat in top_stats[:20]:
					#print(stat)
				

		#except Exception as e:
			#IN.logger.debug()
		
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
		
