import greenlet
import wsgiref, wsgiref.headers

import datetime

import logging
#import In.nabar
import In.core.response
import In.core.action as action
from In.core.asset import Asset
from In.core.cookie import Cookie
from In.html.menu import PageMenuTab


class ContextEnd(RuntimeError):
	'''Context has been explicitly ended.

	'''

class ContextRedirect(RuntimeError):
	'''Context has been explicitly redirected.

	'''
	def __init__(self, path, status = None, ajax_redirect = True, **args):
		self.path = path
		self.status = status
		self.ajax_redirect = ajax_redirect
		super().__init__(**args)


class ContextBadRequest(RuntimeError):
	'''Context request is bad.'''

class ContextNotFound(RuntimeError):
	'''Exception: Page not found.'''

class ContextAccessDenied(RuntimeError):
	'''Exception: Nabar has no access.'''


class ContextInitFailedException(BaseException):
	'''Context faled to init.'''
	
class ContextPool(greenlet.greenlet):
	'''Main Greenlet'''
	

	def __init__(self, pool = None):
		
		# just simple list of contexts
		# application will switch to any context randomly
		# keyed by id() of context
		if pool is None:
			self.pool = {}
		else:
			self.pool = pool
		super().__init__(self.run)
	
	def run(self):

		#while True:
		
		try:
			
			if not self.pool:
				#asyncio.sleep(5)
				#continue
				return
		
			values = self.pool.values()
			
			context = next(iter(values))
			
			if context is None or context.dead:
				self.free(context)
				#sleep(.2)
				# no break,
				#continue
				return
			
			# run another context

			context.switch()
			
			#result = context.switch()
			#if result is not None:
				#self.free(context)
				#return result
		except Exception:
			IN.logger.debug()

	def put(self, context):
		'''Add context to pool'''
		
		self.pool[id(context)] = context
		
	def free(self, context):
		'''Delete this context from pool and del it'''
		
		context_id = id(context)
		try:
			# add db connection as free
			IN.db.free(context)
			
			del self.pool[context_id]
		except Exception:
			IN.logger.debug()
			
		try:
			del context
		except Exception:
			pass
		
		#IN.__context__ = None
		
	#def switch(self):
		#'''run another event'''
		#if self.dead:
			## create new ContextPool
			#IN.APP.context_pool = ContextPool(self.pool)
			#IN.APP.context_pool.switch()
		#else:
			#super().switch()
		

class Context(greenlet.greenlet): # , asyncio.Task
	'''Main request/response logic class.

	'''
	
	
	
	## __disabled_hooks__ - to disable the hook invoke on some hooks temporaryly
	## IN.Registry will use this - for context based state.
	#__disabled_hooks__ = []

	## hooks will be added here if those are not allowed for recursive calls
	#__not_recursive_hooks__ = []

	## contains all the hook names which are in action. We have to check
	## for ignore the recursive hook invoke calls.
	#__hooks_in_action__ = []

	def __init__(self, app, environ, start_response, **args):
		'''__init__ the Context.

		'''
		
		super().__init__()
		
		
		# application Object
		#self.APP        = app
		
		# use this for now request_time
		self.now = datetime.datetime.now()
		
		self.environ    = environ
		
		self.wsgi_callback = start_response

		# available when doing request process
		self.active_action = None

		# assets of css and js. it is still here even response type is changed from Page to Form.
		# response may make use of it if needed
		self.asset	= Asset()
		self.page_menu_tab = PageMenuTab()
		self.page_menu_sub_tab = PageMenuTab()
		self.page_menu_sub_tab_2 = PageMenuTab()
		
		# themer will use it
		self.page_title = ''
		self.display_title = True

		self.headers= wsgiref.headers.Headers([])
		self.cookie = Cookie()

		# additional args for this context
		self.args       = args

		#moved to IN
		# theme for the current context. each context output may be rendered by different theme engine.
		#self.themer      = None
		
		themer = IN.themer
		APP = IN.APP

		default_theme_name = APP.config.default_theme_name
		context_theme_name = APP.decide_theme(self)

		# current theme for this request

		if default_theme_name != themer.default_theme_name:
			self.current_theme  = themer.load_theme(context_theme_name)
		else:
			self.current_theme  = themer.default_theme

		# simple dict cache for the current context
		self.static_cache = {}

		# TODO: session for the current nabar
		self.session    = {}

		# database connection class
		self.db_connections = []

		# __disabled_hooks__ - to disable the hook invoke on some hooks temporarly
		# IN.Registry will use this - for context based state.
		self.__disabled_hooks__ = []

		# hooks will be added here if those are not allowed for recursive calls
		self.__not_recursive_hooks__ = []

		# TODO
		self.__In_static__ = {} # context static value container

		# init the request

		self.request = In.core.request.Request(self)
		#IN.hook_invoke('__context_request_process__', self, self.request)

		# current logged in nabar


		path_parts = self.request.path_parts

		nabar = None

		# ignore nabar for static files path
		if len(path_parts) == 0 or path_parts[0] != IN.APP.config.pfpp:
			
			try:
				nabar_id = IN.nabar.auth_cookie(self)

				if nabar_id:
					nabar = IN.entitier.load('Nabar', nabar_id)
			except Exception as e:
				IN.logger.debug()
			
				# TODO: delete the cookie if nabar is None

		if nabar is None: # use the default
			nabar = In.nabar.anonymous()

		self.nabar = nabar

		# init the response

		#IN.hook_invoke('__context_response_init__', self, self.request)

		# use default page from default theme

		# SPEED # TODO: do we want this even for Form submit /  File request?
		res_args = {}
		page_class = APP.decide_page_class(self)
		if type(page_class) is str:
			page = Object.new(page_class)
		else:
			page = page_class()
			
		#res_args['output'] = page_class()

		# default to PageResponse
		self.response = In.core.response.PageResponse(output = page)

		IN.hook_invoke('__context_init__', self)
	
	
	@property
	def application_uri(self):
		return wsgiref.util.application_uri(self.environ)

	@property
	def request_uri(self):
		return wsgiref.util.request_uri(self.environ)

	def request_end(self):
		raise ContextEnd('ContextEnd')

	def redirect(self, path, status = None, ajax_redirect = True):
		# set redirect processor
		if status is None:
			status = In.http.Status.SEE_OTHER

		self.response = In.core.response.RedirectResponse(path = path, status = status, ajax_redirect = ajax_redirect)

		raise ContextRedirect(path, status, ajax_redirect = ajax_redirect)

	def bad_request(self, output = None, status = None):
		if status is None:
			status = In.http.Status.BAD_REQUEST

		self.response = In.core.response.BadResponse(output = output, status = status)

		raise ContextBadRequest() # raise it
		
	def not_found(self, message = None, title = None):
		
		current_reponse = self.response
		
		output = current_reponse.output
		args = {'output' : output}
		
		self.response = In.core.response.NotFoundResponse(**args)
		
		# set the new path, so blocks can be added by this
		self.request.path = '__page_not_found__'
		
		self.page_title = title or s('Page not found')
		
		#if not message:
			#message = IN.APP.config.message_page_not_found
		
		if message:
			self.response.output.add('Text', {'value' : message})
		
		atn = IN.APP.__page_not_found__(self)
		
		if atn:
			try:
				self.run_actions(atn)
			except Exception as e:
				IN.logger.debug()
		
		raise ContextNotFound()
		
	def send_headers(self):
		'''Calls the WSGI specific start_response method to send headers to client.

		'''
		response_headers = self.headers.items()

		# set the cookies
		for c in self.cookie.values():
			response_headers.append(('Set-Cookie', c.OutputString(None)))

		## set the output so application __call__ will return it.
		self.environ['In_output'] = self.response.output
		
		#self.In_output.put([str(self.response.status), response_headers, self.response.output])

		self.wsgi_callback(str(self.response.status), response_headers)
	
	def run(self):
		
		try:
			
			self.run_actions()
			
		except ContextEnd as end:
			IN.hook_invoke('__context_end__', self.environ, self.wsgi_callback, end)

		except ContextRedirect as red:
			IN.hook_invoke('__context_redirect__', self.environ, self.wsgi_callback, red)

		except ContextBadRequest as bad:
			IN.hook_invoke('__context_bad_request__', self.environ, self.wsgi_callback, bad)
			
		except ContextNotFound as nf:
			IN.hook_invoke('__context_not_found__', self.environ, self.wsgi_callback, nf)
			
		except: # internal server error?
			IN.logger.debug()
		
		#IN.APP.wait()
		
		
		self.process_response()
		
		IN.hook_invoke('__context_request_process_done__', self)
		
		return self.environ['In_output']
		
		#try:
			
		#except:
			## TODO:
			#IN.logger.debug()
			#return [''.encode('utf-8')]
		
	def process_response(self):

		# if no response set
		if self.response is None:
			return self.bad_request()

		#if not type(self.response) is response.ResponseBase:
			#return self.bad_request()


		# process the response

		IN.hook_invoke('__context_response_preprocess__', self, self.response)

		# set output, headers
		self.response.process(self)

		IN.hook_invoke('__context_response_process__', self, self.response)

		# start the response
		self.send_headers()
	
	
	def set_active_action(self, action):
		self.active_action = action
		
		# set title
		self.set_page_title_from_action(action)
		
	def set_page_title_from_action(self, action):
		# set page title
		if isinstance(action, In.core.action.ActionObject):
			if type(action.title) is str:
				self.page_title = action.title
			else: # call the function
				self.page_title = action.title(a)
		elif action.actions:
			action = action.actions[-1]
			self.set_page_title_from_action(action)
			
	def run_actions(self, actions = None):
		'''check for the suitable action for the request
		'''
		if actions is None:
			actions = self.actions()
			
		if type(actions) is In.action.ActionObject:
			self.set_active_action(actions)
			actions.__call__(self)
		else:
			for action in actions:
				if action:
					# set it, so modules can change pass_next to continue to next or break it
					self.set_active_action(action)
					action.__call__(self)

					if not action.pass_next: # pass to next action

						break

	#def __call__(self):
		#return self.run()


	def actions(self):
		'''get action based on request.

		'''

		'''Handle direct actions such as form submit'''
		for atn in IN.hook_invoke_yield('__context_early_action__', self):
			if atn:
				yield atn
				if not atn.pass_next:
					return

		'''Find action by path'''
		path = self.request.path

		if path:
			# TODO: REMOVE UNWANTED
			p = path.replace('/', '_')

			for atn in IN.hook_invoke('_'.join(('direct_path_action', p)), self):
				if atn:
					yield atn
					if not atn.pass_next:
						return

			for atn in action.path_action():
				if atn:
					yield atn
					if not atn.pass_next:
						return

			# path not found
			
			self.not_found()

			return

		# no path # use index page
		yield IN.APP.__index_page__(self)

		return

	def ensure_page_response(self):
		'''make sure that the response is type if PageResponse'''
		
		if not isinstance(self.response, In.core.response.ObjectResponse): # Object like
			self.response = In.core.response.PageResponse()

	def access(self, key, account = None, deny = False):
		'''shortcut methof to IN.access
		return true if account has access key

		if context.access('view_content'):
			do something

		account : nabar object. context.nabar by default
		deny: redirect to access denied page if True
		
		TODO: cache?		
		'''
		
		if account is None:
			account = IN.context.nabar

		result = IN.nabar.access(key, account)

		if deny and not result:
			self.access_denied()

		return result
	
	def access_denied(self, message = None, title = None):
		
		current_reponse = self.response
		
		output = current_reponse.output
		args = {'output' : output}
			
		self.response = In.core.response.AccessDeniedResponse(**args)

		if isinstance(output, Object):
			# set this only if output is IN Object like
			
			if title is None:
				title = s('Access Denied!')
				
			self.response.output.title = title
			
			if message is None:
				message = IN.APP.config.message_access_denied
				
			self.response.output.add('Text', {'value' : message})

		raise ContextAccessDenied()
		
	#def switch(self):
		#'''overrides greenlet switch to set the context.'''
		
		#IN.__context__ = self
		#super().switch() # greenlet.greenlet
	