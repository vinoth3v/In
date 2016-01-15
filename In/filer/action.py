from .path import *

@IN.hook
def actions():

	actns = {}

	fpaths = IN.hook_invoke('public_file_paths')
	
	public_file_path_prefix = IN.APP.config.public_file_path_prefix
	
	for pathres in fpaths:
		for path_type, args in pathres.items():
			try:
				handler = args['handler']
			except KeyError:
				handler = file_action_default_handler

			actns['/'.join((public_file_path_prefix, path_type))] = {
				'title' : 'IN File Handler',
				'handler' : handler,
				'type' : 'hidden',
				'handler_arguments' : {
					'base_path' : args['base_path'],
					'path_type' : path_type,
				},
			}

	IN.APP.file_actions = actns
	return actns
