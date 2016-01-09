from collections import OrderedDict
from functools import *

import In.core.response

@IN.hook
def __In_app_init__(app):
	build_actions(app, True)

def build_actions(app, refresh = False):

	if app.actions and not refresh:
		return app.actions

	actns = IN.hook_invoke('actions', __inc_module__ = True)

	token_actns = {}
	#convert {arg} to *
	for res in actns:
		mactns = {}

		for mod, paths in res.items():

			for path, path_def in paths.items():
				if not path: continue

				path_def['tokens'] = OrderedDict() # must! to keep token values in correct order
				path_def['path'] = path

				parts = path.split('/')

				token_paths = []
				for pi in parts:

					if pi.startswith('{') and pi.endswith('}') and len(pi) > 2:
						token_paths.append('*')
						path_def['tokens'][pi.replace('{', '').replace('}', '')] = ''

					else:
						token_paths.append(pi)

				token_path = '/'.join(token_paths)

				path_def['token_path'] = token_path

				token_actns[token_path] = path_def

	app.actions = token_actns

	return token_actns


def path_to_token_path(path):
	parts = path.split('/')
	token_parts = []
	tokens = []
	if len(parts) > 1:
		for pi in parts:
			#check wether it has arguments in numeric or num,num, or num+num, or num|num, or !string
			if pi.isnumeric() or \
				all([i.isnumeric() for i in pi.split(',') if i]) or \
				all([i.isnumeric() for i in pi.split('+') if i]) or \
				all([i.isnumeric() for i in pi.split('|') if i]):
				token_parts.append('*') # * as wildchar
				tokens.append(pi)
			elif pi.startswith('!'): # all text args prefixed with !
				token_parts.append('*') # * as wildchar
				tokens.append(pi.replace('!', ''))
			else:
				token_parts.append(pi)

		return '/'.join(token_parts), tokens
	else:
		return path, []

@lru_cache(maxsize = 15000)
def route_path_from_alias(alias):

	try:
		
		cursor = IN.db.select({
			'table' : 'config.path_alias',
			'columns' : ['path'],
			'where' : ['alias', alias]
		}).execute()
		
		if cursor.rowcount == 0:
			return alias

		return cursor.fetchone()['path']
		
	except Exception as e:
		IN.logger.debug()
	
	return alias

def path_action():
	'''
	#TODO: Rewrite it, use DB and optimize'''


	actions = IN.APP.actions
	context = IN.context
	action  = ActionContainer()
	
	request = context.request
	
	path = request.path

	if not path:
		return None
	
	# moved from request.py
	if request.path_parts[0] != IN.APP.config.pfpp:
		sys_path = route_path_from_alias(path)
		if sys_path != path:
			request.path_alias = path
			request.path_parts = sys_path.split('/')
			request.path = sys_path
			path = sys_path
			
	token_path, token_values = path_to_token_path(path)
	
	request.path_tokenized = token_path
	request.path_tokenized_values = token_values
	
	
	# use In defined action
	
	action_def = find_path_in_action_dict(token_path)
	# assign token values
	if action_def:
		for tv in zip(action_def['tokens'], token_values): # ordereddict
			action_def['tokens'][tv[0]] = tv[1]
		#print('*************', action_def)
		action_object = ActionObject(**action_def)
		action.add(action_object)

	if action.has_actions():
		return [action]

	return []


def find_path_in_action_dict(token_path):
	actions = IN.APP.actions
	if token_path in actions:
		return actions[token_path].copy()
	else:
		
		token_paths = token_path.split('/')
		
		while(token_paths):
			#token_paths = token_paths[:-1]
			del token_paths[-1]
			
			new_token_path = '/'.join(token_paths)
			if new_token_path in actions:
				return actions[new_token_path].copy()
			


def combine(atns):
	atn = ActionContainer()
	for a in atns:
		if (a and (a is not None) and isinstance(a, ActionObject)):
			atn.add(a)
	return atn

def __page_not_found__(context, action, **args):

	if not context.request.ajax:
		# we server normal response for ajax requests
		context.response.status = In.http.Status.NOT_FOUND
		
	if not context.page_title:
		context.page_title = s('Page not found')
		
	text = s('The requested page is not found!. Please check whether the path is right.')
	
	context.response.output.add('Text', {'value' : text})

def __index_page__(context, action, **args):
	''''''
	
	context.page_title = s('Welcome to ') + IN.APP.config.app_title
	
def __invalid_request__(context, action, **args):
	
	page.title = s('Invalid Request')

def __internal_server_error__(context, action, **args):
	
	page.title = s('Internal server error')



class ActionContainer:

	def __init__(self):
		self.actions = []
		self.path_pattern = ''
		self.pass_next = False

	#def process(self, idx = -1):

		#if idx == -1: # Process all action items one by one

			#self.__run_action__(self)	# Run the action

		#elif idx > -1:

			#self.__run_action__(self.actions[idx]) # Run the action

		#else:

			#pass # dummy action - just to refresh

	def add(self, atn):
		if not atn: return
		if isinstance(atn, ActionObject):
			self.actions.append(atn)
		if isinstance(atn, ActionContainer):
			for a in atn.actions:
				self.add(a)

	def has_actions(self):
		return len(self.actions)

	def __call__(self, context):
		'''Run the Action Object'''
		for a in self.actions:
			return a.__call__(context)


class ActionObject:

	def __init__(self, **args):

		self.title = ''					# Action Title
		self.handler = None		 		# Handle function
		self.params = {}				# parameters
		self.arguments = {}				# args
		self.tokens	= {}				# tokens and its values
		self.load_arguments = {}		# args and its callbacks
		self.load_modules = []			# any additional module to load
		self.secured = False			# is HTTPS?
		self.definedin = None			# Module where it is defined
		self.result = None				# Action Result
		self.process = False			# Run as Separate Process?
		self.wait = True				# parent should Wait for Exit?
		self.error = None				# holds the Error Object
		self.error_handler = None		# which handler handles the error
		self.pass_next = False			# should continue to next action even if this action is executed

		#if 'definedin' in args:
			#args['handler'] = In.util.raw_eval(args['definedin'] + '.' + args['handler'])
		if 'error_handler' in args:
			args['error_handler'] = In.util.raw_eval(args['definedin'] + '.' + args['error_handler'])

		if 'tokens' in args:
			self.tokens = args['tokens']

		#if 'arguments' in args:
			#self.arguments = args['arguments']

		if 'load_arguments' in args:
			self.load_arguments = args['load_arguments']

		#if 'params' in args:
			#self.params.update(args['params'])

		self.handler_arguments = args.get('handler_arguments', {})

		self.title			= args.get('title' , self.title)
		self.handler		= args.get('handler' , self.handler)
		self.load_modules	= args.get('load_modules' , self.load_modules)
		self.secured		= args.get('secured' , self.secured)
		self.result			= args.get('result' , self.result)
		self.process		= args.get('process' , self.process)
		self.wait			= args.get('wait' , self.wait)
		self.error			= args.get('error' , self.error)
		self.error_handler	= args.get('error_handler' , self.error_handler)
		self.pass_next		= args.get('pass_next' , False)


	## handler = None					#
	## params = {}					# parameters
	## load_modules = []		# any additional module to load
	## secured = False			# is HTTPS
	## defined= None				# Module where it is defined
	## result = None				# Action Result
	## process = False			# Run as Separate Process?
	## wait = True					# Wait for Exit?
	## error = None				 # holds th Error Object
	## error_handler = None					 # which handler handles the error
	def __call__(self, context):

		try:

			#importing any modules prior to run
			for m in self.load_modules:
				try:
					__import__(m)
				except Exception as me:
					IN.logger.debug()

			# update token valaues
			self.handler_arguments.update(self.tokens)

			# load if needed
			for arg, token_value in zip(self.load_arguments, self.tokens):
				self.handler_arguments[arg] = self.load_arguments[arg](token_value)

			#if self.arguments:
				#self.params.update(self.arguments)

			self.result = self.handler(context, self, **self.handler_arguments)

			return self.result

		except Exception as e:
			self.error = e
			self.result = None

			if self.error_handler is not None:
				try:
					self.error_handler(self)
				except Exception as ee:
					IN.logger.debug()
			else:
				IN.logger.debug()
				raise e


def def_token_handler(part):
	def_parts = ['{nabar}', '{term}']
	if part in def_parts:
		pass

