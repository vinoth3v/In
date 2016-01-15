import os

class Filer:
	'''Filter file handler'''
	
	
	def process_uploaded_file(self, fileobj):
		'''Saves the uploaded file to disk file.
		'''
		
		uploaded_file = fileobj.file

		filename, ext = os.path.splitext(fileobj.filename)

		# module should move this file to another location
		file_path = self.__get_random_file__(ext)

		newfile = open(file_path, 'wb')
		while True:
			fbytes = uploaded_file.read(1024)
			if not fbytes:
				break
			newfile.write(fbytes)
		newfile.close()

		return {
			'__upload__' : True, 
			'path' : file_path
		}


	def create_file_entity(self, path, default_file_bundle, nabar_id = None):
		'''path is temporary uploaded path'''

		# invalid?
		if not os.path.exists(path):
			IN.logger.debug(path + ' not exists')
			return
		
		os_path_join = os.path.join
		os_path_exists = os.path.exists
		
		size = os.path.getsize(path)
		
		# returns bytes
		mime = magic.from_file(path, mime = True).decode("utf-8")
		mime1, mime2 = mime.split('/', 1)
		
		# TODO: private files
		public_file_dir = IN.APP.config.public_file_dir
		
		# TODO: custom nabar id
		save_to_prefix = 'images/' + str(IN.context.nabar.id)
		save_to_prefix = os.path.join(public_file_dir, save_to_prefix)						
		
		# create folder
		os.makedirs(save_to_prefix, exist_ok = True)
		
		
		file_name = os.path.split(path)[1]
		save_to = os_path_join(save_to_prefix, file_name)
		
		tmp, ext = os.path.splitext(file_name)
		
		while os_path_exists(save_to):
			
			file_name = str(random.getrandbits(128)) + ext
			save_to = os_path_join(save_to_prefix, file_name)
			
		shutil.move(path, save_to)
		
		path = save_to
		
		# TODO: strip the path prefix
		
		path = path.replace(public_file_dir + '/', '', 1)
		
		# create new File entity
		file = Entity.new('File', {
			'type' : default_file_bundle,
			'nabar_id' : nabar_id or IN.context.nabar.id,	# current user # 
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
		
	def __get_random_file__(self, ext):
		
		os_path_join = os.path.join
		os_path_exists = os.path.exists
		tmp_file_dir = IN.APP.config.tmp_file_dir
		
		while True: # get a new file name
			file_name = str(random.getrandbits(128)) + ext
			file_path = os_path_join(tmp_file_dir, file_name)
			if not os_path_exists(file_path):
				return file_path
