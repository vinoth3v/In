
import datetime

from In.core.object_meta import ObjectMetaBase

class TaskMeta(ObjectMeta):

	__class_type_base_name__ = 'TaskBase'
	__class_type_name__ = 'Task'


class TaskBase(Object, metaclass = TaskMeta):
	'''Base class of all IN TaskBase.

	'''
	__allowed_children__ = None
	__default_child__ = None


@IN.register('Task', type = 'Task')
class Task(TaskBase):
	'''Base class of all IN Task.
	'''

	status = 0
	weight = 0
	retries = 0
	run_at = None
	error = None
	last_run = None
	
	def __init__(self, data = None, items = None, **args):
		
		self.args = {}
		
		self.created = datetime.datetime.now()
		
		super().__init__(data, items, **args)
	
	
	@staticmethod
	def new(type, data, items = None, **args):
		'''Overrides Object.new to get object of type Task.
		'''
		
		objclass = IN.register.get_class(type, 'Task')
		
		if objclass is None:
			# use the default
			objclass = Task

		obj = objclass(data, items, **args)
		
		return obj
	
	def __run__(self):
		
		self.run()
		return IN.tasker.FINISHED
		
	def run(self):
		'''nothing ro run'''
	
builtins.Task = Task