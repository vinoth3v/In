import os, random, json, shutil, magic

from In.core.action import ActionObject
from .entity_file import *
from .field_file import *

from .admin import *

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

	public_prefix = config.public_file_path_prefix
	if not path.startswith(public_prefix + '/'):
		# not public file path
		return

	for action_path, action_def in IN.APP.file_actions.items():
		apath = action_path
		action_path = action_path + '/'
		
		if path.startswith(action_path):
			path = path.replace(action_path, '', 1)
			
			action_def['handler_arguments']['path'] = path
			action_def['handler_arguments']['path_type'] = apath.replace(public_prefix + '/', '', 1)
			action_object = ActionObject(**action_def)

			return action_object


@IN.hook
def actions():

	actns = {}

	fpaths = IN.hook_invoke('public_file_paths')

	for pathres in fpaths:
		for path, args in pathres.items():
			try:
				handler = args['handler']
			except KeyError:
				handler = file_action_default_handler

			actns['/'.join((IN.APP.config.public_file_path_prefix, path))] = {
				'title' : 'IN File Handler',
				'handler' : handler,
				'type' : 'hidden', # | link | button | hidden | menu
				'handler_arguments' : {
					'base_path' : args['base_path'],
				},
			}

	IN.APP.file_actions = actns
	return actns

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

def file_action_default_handler(context, action_object, path, base_path, path_type = '', **args):
	'''Default file handler
	'''
	os_path = os.path
	#base_path = action_object.params['arguments']['base_path']
	#ex_path = action_object.params['arguments']['path']
	
	full_path = os_path.join(base_path, path) # not ''.join
	
	
	try:

		ext = os_path.splitext(full_path)[1]

		if not ext[1:] in IN.APP.config.default_files_allowed:
			context.response = In.core.response.EmptyResponse(status=In.http.Status.UNSUPPORTED_MEDIA_TYPE)
			return

		if os_path.exists(full_path):
			
			context.response = In.core.response.FileResponse(file = open(full_path, 'rb'), file_path = full_path, file_extension = ext)
			return True

		# try dynamic file generator, image styles, dynamic css, js bundle
		generated = IN.hook_invoke('file_generator', ext, path, base_path, path_type)
		if generated:
			for gen in generated:
				if gen:
					full_path = gen
					if os_path.exists(full_path):			
						context.response = In.core.response.FileResponse(file = open(full_path, 'rb'), file_path = full_path, file_extension = ext)
						return True
		
				
		# file not found

		#context.response = In.core.response.NotFoundResponse()

		#return
	except Exception as e:
		IN.logger.debug()

	context.response = In.core.response.EmptyResponse(status=In.http.Status.NOT_FOUND)

def process_uploaded_file(fileobj):
	'''Saves the uploaded file to disk file.
	'''
	uploaded_file = fileobj.file

	filename, ext = os.path.splitext(fileobj.filename)

	# module should move this file to another location
	file_path = get_random_file(ext)

	newfile = open(file_path, 'wb')
	while True:
		fbytes = uploaded_file.read(1024)
		if not fbytes:
			break
		newfile.write(fbytes)
	newfile.close()

	return {'__upload__' : True, 'path' : file_path}

def get_random_file(ext):
	while True: # get a new file name
		file_name = str(random.getrandbits(128))
		file_path = os.path.join(IN.APP.config.tmp_file_dir, file_name + ext)
		if not os.path.exists(file_path):
			return file_path


def create_file_entity(path, default_file_bundle):
	'''path is temporary uploaded path'''

	# invalid?
	if not os.path.exists(path):
		IN.logger.debug(path + ' not exists')
		return
	
	size = os.path.getsize(path)
	
	# returns bytes
	mime = magic.from_file(path, mime=True).decode("utf-8")
	mime1, mime2 = mime.split('/', 1)
	
	public_file_dir = IN.APP.config.public_file_dir
	
	save_to = 'images/' + str(IN.context.nabar.id)
	
	save_to = os.path.join(public_file_dir, save_to)						
	
	# create folder
	os.makedirs(save_to, exist_ok = True)
	file_name = os.path.split(path)[1]
	save_to = os.path.join(save_to, file_name)
	
	shutil.move(path, save_to)
	
	path = save_to
	
	# TODO: strip the path prefix
	
	path = path.replace(public_file_dir + '/', '', 1)
	
	# create new File entity
	file = Entity.new('File', {
		'type' : default_file_bundle,
		'nabar_id' : IN.context.nabar.id,	# current user
		'status' : 1,			# active
		'path' : path,
		'size' : size,
		'mime1' : mime1,
		'mime2' : mime2,
		'remote': 0,
		'data'	: json.dumps({}, skipkeys = True, ensure_ascii = False),
	})
	file_id = IN.entitier.save(file)
	
	return file_id