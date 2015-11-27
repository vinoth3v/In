import json
import datetime, time
from multiprocessing import Process
from autobahn.asyncio.websocket import WebSocketServerProtocol

class TaskerContext(In.core.context.Context, WebSocketServerProtocol):
	
	def __init__(self, tasker, app, **args):
		'''__init__ the Context.
		'''
		self.tasker = tasker
		dummy = lambda: ''
		super().__init__(app, {}, dummy, **args)
		
	def run(self):
		
		while True:
			
			try:
				self.tasker.run()
			except Exception as e:
				IN.logger.debug()
			
			
			time.sleep(2)
			
			
			try:
				
				IN.hook_invoke('tasker_cron')
				
			except Exception as e:
				IN.logger.debug()
				
			
			#asyncio.sleep(self.tasker.sleep_seconds_between_task)
			#self.parent.switch()
			#IN.APP.switch()

class Tasker:
	'''Task queue system'''
	
	DISABLED = 0
	ACTIVE = 1
	RUNNING = 2
	ERROR = 3
	DEAD = 4
	FINISHED = 5
	
	running_process = None
	
	#def __init__(self):
		
		#self.task_types = RDict()
		
		#returns = IN.hook_invoke('tasker_task_type')
		
		#for types in returns:
			#self.task_types.update(types)
		
		##if IN.APP.__class__.__name__ == 'WSApplication':
			## only start the tasker process if APP is WS, so multiple processes will not be started
			
		
	def start_the_process(self):
		
		if self.running_process is None:
			
			self.context = TaskerContext(self, IN.APP)
			
			self.running_process = Process(target = self.init_context)
			self.running_process.start()
		
			#self.running_process.join()
		
		
		
	def add(self, task):
		'''add task into queue'''
		
		connection = IN.db.connection
		
		try:
			
			args = json.dumps(task.args, skipkeys = True, ensure_ascii = False)
			
			values = [
				task.__type__, args, task.status,
				task.weight, task.created, 
				task.last_run, task.retries, task.run_at
			]
			
			cursor = IN.db.insert({
				'table' : 'log.task',
				'columns' : [
					'type', 'args', 'status', 
					'weight', 'created', 
					'last_run', 'retries', 'run_at'
				],
				'returning' : 'id',
			}).execute([values])

			if cursor.rowcount == 1:
				id = cursor.fetchone()[0]
				
				# commit
				connection.commit()
				
				return id
			
		except Exception as e:
			IN.logger.debug()
			connection.rollback()

	def init_context(self):
		
		self.context = TaskerContext(self, IN.APP)
		
		self.context.switch()
		

	def run(self):
		
		try:
			db = IN.db
			connection = db.connection
			
			# find new task
			q = '''SELECT * FROM log.task 
				WHERE status = 1 
				ORDER BY weight, created
				limit 1
				FOR UPDATE
			'''
			
			cursor = db.execute(q)
			
			if cursor.rowcount == 0:
				connection.rollback()
				return
			
			row = cursor.fetchone()
			
			status = row['status']
			
			task = Task.new(row['type'], {
				'id' : row['id'],
				'args' : row['args'],
				'status' : status,
				'weight' : row['weight'],
				'created' : row['created'],
				'last_run' : row['last_run'],
				'retries' : row['retries'],
				'run_at' : row['run_at'],
				'error' : row['error'],
			})
			
			try:
				
				status = task.__run__()
				error = ''
			except Exception as e1:
				IN.logger.debug()
				status = self.ERROR
				error = str(e1)
				
			db.update({
				'table' : 'log.task',
				'set' : [
					['status', status],
					['last_run', datetime.datetime.now()],
					['error', error],
				],
				'where' : [
					['id', task.id],
				],
			}).execute()
			
		except Exception as e:
			IN.logger.debug()
			
		connection.commit()
		
