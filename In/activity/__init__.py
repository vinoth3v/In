from In.activity.activity import *

@IN.hook
def entity_view_modes_alter(entity_type, view_modes, entity_bundle = ''):
	view_modes.add('notification')
	
