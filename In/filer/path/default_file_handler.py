import os

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
				context.response = In.core.response.EmptyResponse(status = In.http.Status.UNSUPPORTED_MEDIA_TYPE)
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
		
		#context.not_found() # do we need to pass to full page process to render not found page?
		context.response = In.core.response.EmptyResponse(status = In.http.Status.NOT_FOUND)
