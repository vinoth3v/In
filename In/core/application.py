import os, sys, imp
import logging.config
import datetime, time

from collections import OrderedDict


#Application Diretory
__app_dir__ = 'app'

class ApplicationBase:
	'''Base Application'''


class Application(ApplicationBase):

	def __init__(self, app_path):

		self.initialized = False

		self.app_path = app_path

		conf_path, conf_filename = os.path.split(app_path + '/config/config.py')
		conf_filename, conf_ext = os.path.splitext(conf_filename)

		try:
			conf_f, conf_filename, conf_desc = imp.find_module(conf_filename, [conf_path])
		except ImportError as e:
			IN.logger.debug()
			raise RuntimeError('Unable to import IN config.')

		self.config = imp.load_module(conf_filename, conf_f, conf_filename, conf_desc)

		# set global timezone
		os.environ['TZ'] = self.config.timezone_name
		time.tzset()

		#self.app_path = self.config.app_root + os.sep

		sys.path.append(self.app_path + '/themes/')
		sys.path.append(self.app_path + '/addons/')
		#sys.path.append(self.app_path + '/vendor/')

		# set the debug mode to true or false based on the configuration
		IN.debug = self.config.debug_mode

		self.scope  = 'Global'  #default Scope to Global     # future use
		self.access = 'Public'  #default Access to Public    # future use
		self.version = IN.__version__ #default to IN Version

		# set the Application Object to IN
		IN.APP = self


		self.static_cache = {}

		# contains all the actions built for this application.
		# TODO: memory !!!
		self.actions = None
		self.file_actions = None

		# override IN logger to app specific
		#logging.config.dictConfig(self.config.loggerging)
		#IN.logger = In.core.IN.logger.Logs(config = self.config.loggerging)

		# contains the list of all access keys
		self.access_keys = {}

		self.def_theme_engine = None
		self.def_theme = None

		self.addons = OrderedDict()

		'''per app based addons. load them on app init.
		'''
		self.load_addons()

		self.context_pool = In.core.context.ContextPool()

		# start the event
		#self.context_pool.switch()


		try:
			# assign database controller Object
			IN.db = In.db.DatabaseController(IN.APP.config.db_settings)

		except Exception as e :
			IN.logger.debug()
			raise In.db.DBEngineInitializationException(e)

		try:

			# connect to db server
			IN.db.connect()

		except Exception as e :
			#print(sys.exc_info()[0])
			IN.logger.debug()
			raise In.db.DBConnectionFailedException(e)

		IN.stringer = In.stringer.Stringer()
		IN.cacher = In.core.cacher.CacherEngine()

		# init default cacher
		IN.cacher.default

		IN.valuator = In.core.valuator.ValuatorEngine()

		IN.themer = In.themer.INThemeEngine(self.config.default_theme_name)

		IN.boxer = In.boxer.BoxEngine()

		IN.former = In.former.FormerEngine()

		IN.fielder = In.field.FielderEngine()
		IN.entitier = In.entity.EntitierEngine()

		IN.texter = In.texter.TexterEngine()
		IN.mailer = In.mailer.Mailer()

		# In.nabar is module
		# IN.nabar is Object
		# context.nabar is current nabar
		IN.nabar = In.nabar.AccountAuth()

		IN.commenter = In.comment.Commenter()

		# process the registers after In, app, application init.
		IN.register.process_registers()

		IN.hook_invoke('In_app_init', self)

		IN.hook_invoke('__In_app_init__', self)

		self.initialized = True

	def addon_enabled(self, name):
		'''TODO:
		'''
		try:
			return self.addons[name].enabled
		except:
			IN.logger.debug()

		return False

	def addon(self, name):
		'''TODO:
		'''
		try:
			return self.addons[name]
		except:
			IN.logger.debug()

		return None

	def load_addons(self):
		for addon in self.config.addons:
			try:
				__import__(addon)
			except:
				IN.logger.debug()

		#???: specific to app instance?? how?
		sys.path.append( ''.join((self.app_path, __app_dir__, os.sep, self.config.app_name, os.sep, 'addons')) )

		ret = [IN.load_extension(m) for m in self.addons if m.enabled]


	def app_verify(self):
		'''Runs various test against the Application and returns the result.
		'''

		self.load_addons()
		return True

	def load(self):
		#self.__load_configs()
		self.load_addons()

	def ensure_environ ( self, environ ) :
		pass

	def decide_page_class(self, context):
		'''Return Page class dynamically based on path/nabar/role/...'''
		return context.current_theme.decide_page_class(context)

	def decide_theme(self, context):
		'''Return theme name dynamically based on path/nabar/role/...'''
		return self.config.default_theme_name

	def decide_page_boxes(self, context, page, format):
		'''Return boxes dynamically based on path/nabar/role/...'''
		
		boxes = []
		
		path_hook_tokens = context.request.path_hook_tokens()
		
		for hook in path_hook_tokens:
			IN.hook_invoke('page_box_' + hook, boxes, context, page, format)
		
		# hook by all path
		IN.hook_invoke('page_box', boxes, context, page, format)
		
		return boxes

	def decide_page_assets(self, context, page, format):
		'''add/modify css js'''
		return

	def reload_config(self):
		'''Reload the config without restarting the server.
		TODO:
		'''
		pass


	def __page_not_found__(self, context):
		atn = In.action.ActionObject()
		atn.handler = In.action.__page_not_found__
		return atn

	def __invalid_request__(self, context):
		atn = In.action.ActionObject()
		atn.handler = In.action.__invalid_request__
		return atn

	def __index_page__(self, context):
		atn = In.action.ActionObject()
		atn.handler = In.action.__index_page__
		return atn

	def __internal_server_error__(self, context):
		atn = In.action.ActionObject()
		atn.handler = In.action.__internal_server_error__
		return atn


class WSGIApplication(Application):
	'''IN WSGIApplication class. '''



	def __call__(self, environ, start_response):

		#time.sleep(.6)

		#### Hello world test
		#status = '200 OK'
		#output = 'Hello World!'.encode('utf-8')
		#response_headers = [('Content-type', 'text/plain'),
                        #('Content-Length', str(len(output)))]
		#start_response(status, response_headers)
		#return [output] # Hello World test

		# handle our own
		
		debug = 0
		
		if debug:
			import cProfile, pstats, io
			pr = cProfile.Profile()
			pr.enable()

		In_output = self.__run_call__(environ, start_response)
		
		if debug:
			pr.disable()
			s = io.StringIO()
			sortby = 'cumulative'
			ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
			ps.print_stats()
			print(s.getvalue())

		return In_output


	def __run_call__(self, environ, start_response):

		#sys.stdout = open(os.devnull, 'w')
		# test

		self.ensure_environ(environ)

		try:

			context = In.context.Context(self, environ, start_response)

			#IN.hook_invoke('__request_handler_init__', environ, start_response)

		except In.context.ContextInitFailedException as context_failed:
			# could not init the Context
			# do some manual init before proceeding?
			#print(traceback.format_exc())
			# TODO: return plain error response
			IN.logger.debug()
			return

		# handle the request
		#self.handle_request(context)

		# add context to pool

		self.context_pool.put(context)

		#stime = datetime.datetime.now()

		# start this greenlet
		# TODO
		In_output = context.switch()

		#etime = datetime.datetime.now()

		##IN.logger.debug('Context start time: {stime}', {'stime' : stime})
		##IN.logger.debug('Context end time: {etime}', {'etime' : etime})
		#ms = etime - stime
		#IN.logger.debug('Context time {diff}', {'diff' : ms})


		# delete and free this context
		try:
			self.context_pool.free(context)
		except Exception:
			IN.logger.debug()


		return In_output

	#def handle_request(self, context):
		#'''Applications main request handler
		#'''

		#'''Check whether is any request handler is handled this.
		#'''
		##res = IN.hook_invoke('app_request_handler')

		##if res and any(res):
			##''' Request is handled by some other object'''
			##return True

		## run all actions

		#context.run_actions()

		#return True # Job Done! Return

	def load(self):
		#self.__load_configs()
		self.load_addons()

	def ensure_environ ( self, environ ) :
		pass

	def decide_page_class(self, context):
		'''Return Page class dynamically based on path/nabar/role/...'''
		return context.current_theme.decide_page_class(context)

	def decide_theme(self, context):
		'''Return theme name dynamically based on path/nabar/role/...'''
		return self.config.default_theme_name

	def decide_page_assets(self, context, page, format):
		'''add/modify css js'''
		return

	def reload_config(self):
		'''Reload the config without restarting the server.
		TODO:
		'''
		pass

	def action_page_not_found(self, context):
		return In.action.__page_not_found_action__()



