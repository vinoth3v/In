import os

class ThemeException(Exception):
	'''Base Exception for Theme related tasks.
	'''

class TemplateNotFound(ThemeException):
	'''Template Not Found Exception.
	'''

from .theme_engine import *

from .theme_formats import *
from .object_themer import *
from .page_themer import *

from .object_theme_cacher import *

@IN.register
def register():
	'''
	instance :
		class - class type if assigned directly
		instance - instance will be created and assigned, all object will use the same member instance
		#instance_class - class will be created and assigned for per object on __init__
		#instance_instance - instance will be created and assigned for per object on __init__
	'''
	return {
		# all object type class should have Themer member of type which is
		'class_members' : {								# register for
			'Object' : {								# type of object - arg to class members
				'Themer' : {						# key
					'name' : 'Themer',				# member name
					'instance' : 'instance',			# type of instance
				},
				'ThemeCacher' : {						# key
					'name' : 'ThemeCacher',				# member name
					'instance' : 'instance',			# type of instance
				},
			},
		},
	}

@IN.hook
def template_path():
	return [{
		'path' : ''.join((IN.root_path, os.sep, 'templates', os.sep)),
		'weight' : 10,	# go last
	}]
	
#@IN.hook
#def __In_app_init__(app):
	## set the themer

	#IN.themer = In.themer.INThemeEngine()

class ThemeArgs(Object):

	def __init__(self, obj, args):
		super().__init__()
		self.add(obj)
		self.args = args

builtins.ThemeArgs = ThemeArgs
