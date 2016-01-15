import os

from In.core.action import ActionObject

@IN.hook
def public_file_paths():
	config = IN.APP.config
	return {
		'assets' : { # IN path
			'base_path' : os.path.join(IN.root_path, 'assets'),
		},
		'libraries' : { # libraries path
			'base_path' : config.libraries_path,
		},
		'themes' : { # themes path
			'base_path' : config.themes_path,
		},
		'public' : { # files path
			'base_path' : config.public_file_dir
		},
	}



@IN.hook
def __context_early_action__(context):
	'''Default serve files action entry point

	'''

	config = IN.APP.config

	if not config.serve_static_files:
		return

	path = context.request.path
	if not path:
		return

	path_parts = context.request.path_parts
	
	# files/version/path_type/path
	
	if len(path_parts) < 4:
		return
	
	public_prefix = config.public_file_path_prefix
	
	if not path_parts[0] == public_prefix:
		# not files path
		return
	
	path_type = path_parts[2]
	
	for action_path, action_def in IN.APP.file_actions.items():
		apath = action_path
		action_path = action_path + '/'
		
		if action_def['handler_arguments']['path_type'] == path_type:
			
			action_def['handler_arguments']['path'] = '/'.join((path_parts[3:])) #path.replace(action_path, '', 1)
			action_def['handler_arguments']['version'] = path_parts[1]
			
			action_object = ActionObject(**action_def)

			return action_object
	
	# files path
	# but no handler
	#context.not_found()
	
	ao = ActionObject()
	ao.handler = empty_not_found
	
	return ao
	
def empty_not_found(context, action, **args):
		context.response = In.core.response.EmptyResponse(status = In.http.Status.NOT_FOUND)
	