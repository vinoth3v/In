from functools import *

class INHooker:
	'''The IN Hook system.

	'''

	# for hook registration
	__In_hooks__ = {} #OrderedDict()

	# to notify the callbacks of the interest about the new hook.
	hook_callbacks = {}


	################### __ recusrsive hooks __ ######################

	# context needs to be initiated before registry
	#def add_not_recursive_hooks(self, hook):
		#IN.context.__not_recursive_hooks__.append(hook)

	#def remove_not_recursive_hooks(self, hook):
		#IN.context.__not_recursive_hooks__.remove(hook)

	#def clear_not_recursive_hooks(self, hook):
		#IN.context.__not_recursive_hooks__ = []


	########################## __ hooks __ #######################


	def hook(self, func):
		'''The IN hook system.

		IN using decorator to mark the hooks. All hooks which has 
		the same name of the key provided in IN.hook_invoke function 
		will be notified/called and returns the results.

		'''

		@wraps(func)
		def hook(*args, **kwds):
			return func(*args, **kwds)

		#if not self.registration_disabled:
		fun_name = func.__name__
		try:
			In_hooks = self.__In_hooks__[fun_name]
		except KeyError:
			self.__In_hooks__[fun_name] = []
			In_hooks = self.__In_hooks__[fun_name]

		In_hooks.append(hook)

		# notify the callbacks
		self.notfy_hook_callbacks(fun_name, func)

		return hook

	def registered_hooks(self, hook, sort = False):
		'''Returns the IN hooks registered for hook.

		TODO: orderby the hooks based on the module weight
		'''
		hooks = self.__In_hooks__.get(hook, [])

		return hooks

	#def hook_implements(self, hook):
		#'''Returns all modules that has implemented the hook.

		#'''
		#for func in self.registered_hooks(hook):
			#yield func


	#def hook_disable(self, hook = '', disable = True):
		#'''

		#'''
		## if called with empty hook, return all disabled hooks
		#if hook == '':
			#return IN.context.__disabled_hooks__ # per request based

		#if disable:
			#IN.context.__disabled_hooks__.append(hook)
			#return IN.context.__disabled_hooks__

		#try:
			#IN.context.__disabled_hooks__.remove(hook)
		#except:
			#pass

		#return IN.context.__disabled_hooks__

	def hook_invoke(self, hook, *args, __max_hooks__ = None, __inc_result__ = None, __error_handler__ = None, __inc_module__ = None, **kargs):
		'''Invoke all the hook methods which are registered for the hook 'hook'.

		The following keyword arguments can be passed to this function.

		__inc_module__: The module name of the hooks will be included in the result .

		__inc_result__: The result will be included in arguments as '__result__' key
		which lets the hooks to inspect and return appropriate results.

		__max_hooks__: This lets you control how many hooks it should invoke,
		Please note that all the hooks will be sorted by the module position
		before invoking.

		__error_handler__: [any function, return, ignore] This error handler function will be invoked
		if any erros occured during the hook invocation. The default is to IN.logger the error.

		__return_yield__: if True it will yield the result instead of return. __inc_module__ apply.
		'''
		result = []

		#IN.context.__hooks_in_action__.append(hook)

		hooks = self.registered_hooks(hook)

		if not hooks:
			return result

		if __max_hooks__ is not None:
			funs_to_call = hooks[:__max_hooks__]
		else:
			funs_to_call = hooks

		if __inc_result__: # if __inc_result__ supplied the current result wil be available to hooks on __result__ variable.
			kargs['__result__'] = result

		#whether the result includes the module name?

		if __inc_module__:
			return [{fun.__module__ : self.__function_invoke__(fun, args, kargs, __error_handler__)} for fun in funs_to_call]
		else:
			return [self.__function_invoke__(fun, args, kargs, __error_handler__) for fun in funs_to_call]
			#result = list(map((lambda fun: self.__function_invoke__(fun, args, kargs, __error_handler__)), funs_to_call))
			return result

		# remove hook.
		#IN.context.__hooks_in_action__.remove(hook)

		# IN.add_debug('invoke : ' + n + '.' + hook)

	def hook_invoke_yield(self, hook, *args, __max_hooks__ = None, __inc_result__ = None, __error_handler__ = None, __inc_module__ = None, **kargs):
		'''Invoke all the hook methods which are registered for the hook 'hook' and yield the results one by one so you can stop at where you want.

		The following keyword arguments can be passed to this function.

		__inc_module__: The module name of the hooks will be included in the result .

		__inc_result__: The result will be included in arguments as '__result__' key
		which lets the hooks to inspect and return appropriate results.

		__max_hooks__: This lets you control how many hooks it should invoke,
		Please note that all the hooks will be sorted by the module position
		before invoking.

		__error_handler__: [any function, return, ignore] This error handler function will be invoked
		if any erros occured during the hook invocation. The default is to IN.logger the error.

		__return_yield__: if True it will yield the result instead of return. __inc_module__ apply.
		'''

		#IN.context.__hooks_in_action__.append(hook)

		hooks = self.registered_hooks(hook)

		if not hooks:
			return

		if __max_hooks__ is not None:
			funs_to_call = hooks[:__max_hooks__]
		else:
			funs_to_call = hooks

		if __inc_result__: # if __inc_result__ supplied the current result wil be available to hooks on __result__ variable.
			kargs['__result__'] = result

		#whether the result includes the module name?

		if __inc_module__:
			for fun in funs_to_call:
				yield {fun.__module__ : self.__function_invoke__(fun, args, kargs, __error_handler__)}
		else:
			for fun in funs_to_call:
				yield self.__function_invoke__(fun, args, kargs, __error_handler__)


	def __function_invoke__(self, fun, args, kargs, __error_handler__ = None):
		'''Helper function to invoke the hook function instance.
		'''

		try :

			return fun(*args, **kargs)

		except Exception as e :
			IN.logger.debug('Callback error: Function: {f}, Error handler: {err}', {'err' : str(__error_handler__), 'f' : str(fun)})

			if __error_handler__ is None: # default
				raise

			if type(__error_handler__) is str:
				if __error_handler__ == 'ignore': # ignore the error
					IN.logger.debug()
					return
				if __error_handler__ == 'return' :
					# return the error
					IN.logger.debug()
					return e

				raise

			if hasattr(__error_handler__, '__call__'):
				# if __error_handler__ is not none, notify that, here is an Exception.
				try :
					__error_handler__(fun, *args, **kargs)
					return
				except Exception as err :
					# double Error?
					# TODO : add to IN.logger.
					IN.logger.debug()
					# TODO :
					raise # re raise the error

			raise

	def clear_hooks(self):

		# TODO: how? to find the decorators again?
		# but we need this to rebuld, if any module uninstalled.
		# IN Reboot? reinstance registry?
		pass

	def add_hook_callback(self, hook_name, callback):
		'''adds the callback when IN got the new hook defined
		'''
		try:
			hook_callbacks = self.hook_callbacks[hook_name]
		except KeyError:
			self.hook_callbacks[hook_name] = []
			hook_callbacks = self.hook_callbacks[hook_name]

		hook_callbacks.append(callback)

	def notfy_hook_callbacks(self, hook_name, hook):
		'''notifies all callbacks which are registered for the hook hook_name
		'''
		
		try:
			hooks = self.hook_callbacks[hook_name]
			if not hooks:
				return
			for func in hooks:
				try:
					func(hook_name, hook)
				except Exception as e:
					IN.logger.debug()
					#print(e)
		except KeyError:
			pass

	################################## X Invoker ################
	class XHook:
		'''XHook class provides the context manager based auto hook invoker.

		before = ['before']
			This can be list of strings or functions.
			if string, it will be included in hook invoke.
			or it will be called directly

		after = ['after']
			same as before

		callthis
			which function or hook it should be called. it uses the same wrapped function name if it is empty.

		suffix
			should before or after string suffxed with the hook name?

		@example

		@IN.hooker.xhook()
		def fun():
			pass

		@IN.hook
		def fun_before():
			#called before fun call
			pass

		@IN.hook
		def fun_after():
			#called after fun call
			pass

		'''

		def __init__(self, func, before = ['before'], after = ['after'], callthis = '', suffix = False, ignoreerror = False, args=None, kargs=None):

			self.before = before
			self.after = after

			self.func = func
			self.callthis = callthis

			self.suffix = suffix

			self.ignoreerror = ignoreerror
			if args is None:
				args = []
			if kargs is None:
				kargs = {}
			self.args = args
			self.kargs = kargs

			self.func_result = None


		def call_hook(self, when):
			hook = ''
			if not self.callthis:
				hook = self.func.__name__
			elif type(self.callthis) is str:
				hook = self.callthis
			else:
				hook = '' #because invokeall is not to be called
			if hook and self.suffix:
				hook = '_'.join((hook, when))
			return hook

		def __call__(self):
			'''This method returns another invoke function decorator.
			'''

			return self.invoke(self.before, self.after, self.callthis, self.suffix, self.ignoreerror, self.args, self.kargs)

		def __invoke_calls__(self, calls, when):

			for call in calls:

				if type(call) is str:
					hook = ''
					if not self.callthis:
						hook = self.func.__name__
					elif type(self.callthis) is str:
						hook = self.callthis
					else:
						hook = '' #because invokeall is not to be called

					if hook:
						if self.suffix:
							hook = '_'.join((hook, call))
						IN.hook_invoke(hook, *self.args, **self.kargs)
				else:
					call(*args, **kargs)

		def __enter__(self):
			'''Context enter'''

			self.__invoke_calls__(self.before)

			return self

		def __exit__(self, exc_type, exc_value, traceback):
			'''Context exit'''

			self.__invoke_calls__(self.after)

			return self.ignoreerror


	def xhook(before = ['before'], after = ['after'], callthis = '', suffix = True, ignoreerror = False, args=None, kargs=None):
		'''Decorator for XInvoker

		@see class XInvoker:
		'''
		if args is None:
			args = []
		if kargs is None:
			kargs = {}
		def hookfunc(func):

			@wraps(func)
			def hook(*args, **kargs):

				with XHook(func, before, after, callthis, suffix, ignoreerror, args, kargs) as __invoker__:

					res = func(*args, **kargs)
					__invoker__.func_result = res
					return res

			return hook

		return hookfunc


def function_invoke(f, *args, **keys):
	'''Helper function.'''

	try:
		return f(*args,**keys)
	except Exception as e:
		IN.logger.debug('Invoke : {f} {e} in module {m}', {'f' : f.__name__, 'e' : str(e), 'm' : f.__module__})


def invoke(m, hook, *args, **keys):
	try:
		if hasattr(m, hook):
			#IN.logger.add_debug('Invoking : ' + m.__name__ + '.' + hook + '()')
			f = getattr(m, hook)
			return f(*args,**keys)
		#else:
			#IN.logger.add_debug(m.__name__ + ': has no ' + hook + '() hook defined!')
	except Exception as e:

		IN.logger.debug('Invoke : {hook} {e} in module {m}', {'hook' : hook, 'e' : str(e), 'm' : f.__module__})


