
import datetime

#import In.entity

#class NabarConfig(In.entity.Entity):
	## TODO:
	#def __init__(self, data = None, items = None, **args):
		#super().__init__(data, items, **args)
		#self.language = 'ta'
	
class Nabar(In.entity.Entity):
	'''Nabar Entity class.
	'''
	
	name = 'Guest'
	created = datetime.datetime.now()
	status = 0
	language = 'ta'
	picture = None

	@property
	def nabar_id(self):
		'''All entities except Nabar has nabar_id attribute. nabar.nabar_id is mapped to nabar.id'''
		return self.id
		
	@nabar_id.setter
	def nabar_id(self, id):
		self.id = id
	
	@property
	def email_address(self):
		'''nabar has no direct email attribute'''
		
		if not self.id:
			return ''
		
		try:
			return self.data['primary_email']			
		except Exception as e:
			IN.logger.debug()
			return ''
		
	def __init__(self, data = None, items = None, **args):
		
		self.roles = set() # set, fast lookup, unique
		self.data = {}
		
		super().__init__(data, items, **args)

		if type(self.id) is str:
			if self.id.isnumeric():
				self.id = int(self.id)
			else:
				self.id = None
		
		if type(self.roles) is list:
			self.roles = set(self.roles)
			
		#self.lastlogin = args.get('lastlogin', datetime.datetime.now())
		#self.online = args.get('online', False)
	
	def picture_uri(self, style = 'xsmall'):
		
		if self.picture:
			return ''.join(('/files/public/style/', style, '/', self.picture))
		else:
			return ''
		
# set to builtin
builtins.Nabar = Nabar

@IN.register('Nabar', type = 'Entitier')
class NabarEntitier(In.entity.EntityEntitier):
	'''Base Nabar Entitier'''

	# we need nabar entity insert/update/delete hooks
	invoke_entity_hook = True
	
	
	def load_single(self, id):
		'''load single entity. Special case for id 0: anonymous
		
		TODO: apply anonymous loading for load multiple?
		'''
	
		if not id:
			return In.nabar.anonymous()
		
		return super().load_single(id)
		
	
@IN.register('Nabar', type = 'Model')
class NabarModel(In.entity.EntityModel):
	'''Nabar Model'''

	json_columns = ['data']
	
	def insert_prepare(self, entity, values):
		super().insert_prepare(entity, values)
		self.__prepare_roles_column__(entity, values)
		
	def update_prepare(self, entity, values):
		super().update_prepare(entity, values)
		self.__prepare_roles_column__(entity, values)

	def __prepare_roles_column__(self, entity, values):
		
		if 'roles' in values:
			data = values['roles']
			if type(data) is not list:
				values['roles'] = list(data)
				

# nabar Login

class NabarLogin(In.entity.Entity):
	'''Nabar Login class.
	'''

@IN.register('NabarLogin', type = 'Entitier')
class NabarLoginEntitier(In.entity.EntityEntitier):
	'''NabarLogin Entitier'''


@IN.register('NabarLogin', type = 'Model')
class NabarLoginModel(In.entity.EntityModel):
	'''Nabar Model'''

# nabar password
class NabarHash(In.entity.Entity):
	'''Nabar Hash class.
	'''

@IN.register('NabarHash', type = 'Entitier')
class NabarHashEntitier(In.entity.EntityEntitier):
	'''NabarHash Entitier'''


@IN.register('NabarHash', type = 'Model')
class NabarHashModel(In.entity.EntityModel):
	'''NabarHash Model'''
	
	not_updatable_columns = ['id', 'nabar_id', 'type', 'created']
	

@IN.hook
def entity_model():
	return {
		'Nabar' : {						# entity name
			'table' : {				# table
				'name' : 'nabar',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'nabar_id' : {},	# same id
					'name' : {},	# display name
					'gender' : {},
					'dob' : {},
					'roles' : {},
					'created' : {},
					'status' : {},
					'language' : {},
					'data' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
		'NabarLogin' : {						# entity name
			'table' : {
				'name': 'login',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'nabar_id' : {},
					'type' : {},
					'value' : {},
					'created' : {},
					'status' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
		'NabarHash' : {						# entity name
			'table' : {				# tables
				'name' : 'hash',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'nabar_id' : {},
					'type' : {},
					'hash' : {},
					'hint' : {},
					'created' : {},
					'status' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('Nabar', type = 'Themer')
class NabarThemer(In.themer.ObjectThemer):
	'''nabar themer'''

	def theme_process_variables(self, obj, format, view_mode, args):

		super().theme_process_variables(obj, format, view_mode, args)
		
		nabar = obj
		
		args['nabar_name'] = nabar.name
		args['nabar_id'] = nabar.id
		args['nabar_picture'] = IN.nabar.nabar_profile_picture_themed(nabar, 'usmall')


class NabarPicture(HTMLObject):
	'''themeable nabar picture'''
	
	style = 'xsmall'
	
	def __init__(self, data = None, items = None, **args):
		self.nabar = IN.nabar.anonymous()
		super().__init__(data, items, **args)
		
@IN.register('NabarPicture', type = 'Themer')
class NabarPictureThemer(In.html.tags_themer.HTMLObjectThemer):
	'''Comment themer'''
	
	def theme_prepare(self, obj, format, view_mode, args):
		obj.css.append('nabar-picture-' + obj.style)
		
		super().theme_prepare(obj, format, view_mode, args)
		
	def theme_process_variables(self, obj, format, view_mode, args):

		super().theme_process_variables(obj, format, view_mode, args)
		
		nabar = obj.nabar
		
		args['nabar_name'] = nabar.name
		args['nabar_id'] = nabar.id
		
		cdn = IN.APP.config.cdn.get('img', '')
		args['nabar_picture_uri'] = ''.join(('//', cdn, nabar.picture_uri(obj.style)))
		
		args['image_style'] = obj.style
		
