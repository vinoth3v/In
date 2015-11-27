import sys, io, multiprocessing
import logging, logging.config, logging.handlers, traceback

# add new logging level to be used for displaying message on the page

class TerminalColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class LogMessage():
	'''Base Object for the IN.logger.'''

	def __init__(self, message = '', severity = logging.INFO, **args):

		self.message = message
		self.severity = severity
		#self.msg_args = msg_args
		self.exc_info = None

		if message == '':

			#use the exc_info
			self.exc_info = sys.exc_info()

		else:

			# exc_info for the exception
			self.exc_info = args.get('exc_info', None)



class Logs(dict): # no OrderedDict
	'''This is the wrapper Object for the python logging modue.

	'''

	__logger__ = None

	@property
	def logger(self):
		'''
		'''
		return self.__logger__

	def __init__(self, config = None):

		if config:
			# set the logging configuration from application
			logging.config.dictConfig(config)
		else:
			logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.NOTSET)

		self.__logger__ = logging.getLogger('In.context.' + str(id(self)))

		self.last_error = None
		self.update({
			logging.CRITICAL : [],
			logging.ERROR : [],
			logging.WARNING : [],
			logging.INFO : [],
			logging.DEBUG : [],
			logging.NOTSET : [],
		})

	def info(self, text, args = None):

		return self.log(logging.INFO, text, args)

	def warning(self, text, args = None):

		return self.log(logging.WARNING, text, args)

	def debug(self, text = '', args = None):

		return self.log(logging.DEBUG, text, args)

	def error(self, text='', args = None):

		return self.log(logging.ERROR, text, args)

	def exception(self, text='', args = None):

		return self.log(logging.ERROR, text, args)

	def critical(self, text='', args = None):

		return self.log(logging.CRITICAL, text, args)

	def log(self, level, text = '', args = None):
		
		
		# DEBUG
		#return
		oargs = args
		#if msg == '':
			#return

		#if msg_args is None:
			#msg_args = {}

		if not text:
			exc_info = sys.exc_info()
			if exc_info[1]:
				text = exc_info[1]
				
				print(traceback.format_exc().join((TerminalColor.FAIL, TerminalColor.ENDC)))

		if type(text) is not str:
			text = str(text)
		if args is None:
			args = {}
		try:
			text = text.format_map(args)
		except Exception as e:
			print(level, text, oargs)

		print(text)

		return self.__logger__.log(level, text) # , **args

#class LoggingContextFilter(logging.Filter):
	#"""
	#This is a filter which injects contextual informations (nabar, ip, uri) into the IN IN.logger.

	#"""

	#def filter(self, record):

		#context = IN.context

		#record.nabar = context.nabar.name
		#record.uri = context.request_uri

		#return True

class LoggingFormatter(logging.Formatter):
	'''
	Logging Formatter class.

	'''

	def __init__(self, fmt=None, datefmt=None, style='{'):
		style = '{' # In always uses {} style formating
		super().__init__(fmt, datefmt, style)


#class LoggingNabarMessageHandler(OrderedDict):

	#def __init__(self):
		#super().__init__()

	#def emit(self, record):
		#'''
		#Appends the record to the buffer. If shouldFlush() returns true, calls flush() to process the buffer.

		#'''
		#print('LoggingNabarMessageHandler', record)


	#def flush(self):
		#'''
		#You can override this to implement custom flushing behavior. This version just zaps the buffer to empty.

		#'''
		#return super().flush()

	#def shouldFlush(self, record):
		#'''
		#Returns true if the buffer is up to capacity. This method can be overridden to implement custom flushing strategies.

		#'''

		## always return False
		#return False


def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None: # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record) # No level or filter logic applied - just do it!
        except Exception:
            
            print('Error: ', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
