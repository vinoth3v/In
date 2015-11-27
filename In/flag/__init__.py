from .entity_flag import *
from .entity_flag_type import *
from .form import *

from .flagger import *
from .access import *
from .action  import *
from .admin import *





'''
like unlike

like 	:	like
unlike	:	liked


like	->		liked[unlike]		-> unliked[like]

'''


@IN.hook
def In_app_init(app):
	# set the Flagger

	IN.flagger = Flagger()

@IN.hook
def __entity_context_links__(entity, context_type, output, format, view_mode):
	''''''
	
	if view_mode == 'full' or view_mode == 'default':
		
		IN.flagger.__entity_context_links__(entity, context_type, output, format, view_mode)
