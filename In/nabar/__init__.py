from functools import *

from .nabar import *
from .form import *
from .auth import *
from .box import *
from .page import *
from .hook import *
from .email import *

from .action import *
from .access import *

from .ws_action import *

from .admin import *

class AccountExceptionBase(Exception):
	'''base AccountException.
	'''

class AccountException(AccountExceptionBase):
	'''base AccountException.
	'''


class AccountCreateException(Exception):
	'''Create AccountException.
	'''


@IN.hook
def box():
	
	return {
		'admin_nabar_role_access_group' : {
			'handler' : BoxAdminNabarRoleAccessGroup,
			'panel' : 'sidebar1',
		},
	}



@IN.hook
def token_register_verification(context, action, data):
	
	return IN.nabar.nabar_register_token_verification(context, data)

@IN.hook
def token_recovery_verification(context, action, data):
	
	return IN.nabar.nabar_recovery_token_verification(context, data)


@lru_cache(maxsize = 1)
def anonymous():	
	return IN.nabar.anonymous()


