from .page import *

@IN.hook
def actions():
	actns = {}

	actns['field/image/browse'] = {
		'title' : 'image browser',
		'handler' : action_image_browse_form,
	}

	return actns
