
from .hook import *
from .entity import *

from .entitier import *

from .form import *
from .box import *
from .entity_list import *

from .access import *

from .admin import *

# moved to application
#@IN.hook
#def __In_app_init__(app):
	## set the Entity

	#IN.entitier = EntitierEngine()
	
	
class EntityException(Exception):
	'''Base Entity Exception
	'''
	
class InvalidEntityException(EntityException):
	'''InvalidEntity'''

