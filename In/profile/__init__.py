from functools import *

from .entity_profile import *

from .action import *
from .form import *
from .page import *

from .hook import *

#@lru_cache(maxsize = 500) # TODO: Cache clear
def nabar_profile(nabar_id, profile_bundle):
	
	profiles = IN.entitier.select('Profile', [
		['nabar_id', nabar_id], 
		['type', profile_bundle], 
		['status', 1]
	])
	
	if not profiles:
		return None

	return profiles
