
class File(In.entity.Entity):
	'''File Entity class.
	'''

	def __init__(self, data = None, items = None, **args):

		self.nabar_id = 0
		self.size = 0
		self.mime1 = None
		self.mime2 = None
		self.path = None
		self.tmp_path = None		# temporary uploaded path
		self.remote = 0
		self.private = 0
		self.data = {}
		
		super().__init__(data, items, **args)


@IN.register('File', type = 'Entitier')
class FileEntitier(In.entity.EntityEntitier):
	'''Base File Entitier'''

	# File needs entity insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = False
	
@IN.register('File', type = 'Model')
class FileModel(In.entity.EntityModel):
	'''File Model'''


@IN.hook
def entity_model():
	return {
		'File' : {					# entity name
			'table' : {				# table
				'name' : 'file',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'path' : {},	# file path
					'size' : {},	# bytes
					'mime1' : {},	# mime main type		: image, audio, video
					'mime2' : {},	# mime secondary type	: jpeg, mpeg
					'remote': {},	# 0 - local, 1 - remote file
					'private' : {},	# 0 - public, 1 - private file
					'data'	: {},	# file data
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('File', type = 'Themer')
class FileThemer(In.entity.EntityThemer):
	'''File themer'''


builtins.File = File
