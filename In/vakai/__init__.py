
from .entity_vakai import *
from .vakai_list import *
from .form import *
from .action import *
from .field_vakai import *
from .vakaigal import *
from .field_vakai_field_formatter import *
from .page import *

from .admin import *


@IN.hook
def In_app_init(app):
	# set the Vakaigal

	IN.vakaigal = Vakaigal()
