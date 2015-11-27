from .commenter import *
from .comment import *
from .box import *
from .action import *
from .form import *
from .hook import *
from .task import *

from .admin import *

'''

Comment Entity
	Comment bundle
	page comment
	kavithai comment
	status comment
	

Content
	bundle Kavithai
		kavithai comment
	bundle page
		page comment

Status
	bundle status message
		status comment

'''


@IN.hook
def __entity_view__(entity):

	IN.commenter.entity_view(entity)
	
