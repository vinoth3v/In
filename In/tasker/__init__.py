from .tasker import *
from .task import *


class InvalidTaskException(Exception):
	'''InvalidTaskException'''

@IN.hook
def In_app_init(app):
	# set the tasker

	IN.tasker = Tasker()


#@IN.hook
#def __In_app_init__(app):
	## set the tasker

	

