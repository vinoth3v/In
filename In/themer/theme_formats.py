import os



@IN.register('TEXT', type = 'theme_format')
class TEXT:
	'''Base Theme fotmat class
	'''

	def __str__(self):
		return self.__class__.__name__

	def __repr__(self):
		return self.__class__.__name__

	@property
	def def_template_path(self):
		tp = ''.join((IN.root_path, os.sep, str(self), os.sep, 'templates', os.sep))

		return tp

	def template_path(self, format = ''):
		if not format:
			format = str(self)

		def_path = self.def_template_path

		path = def_path
		#if not os.path.exists(path):
			#print('Templates not found for ' + format + ' format or access denied!. Current ' + format + ' templates path: ' + path)
			#pass

		return path


@IN.register('html', type = 'theme_format')
class html(TEXT):
	'''html Theme fotmat class
	'''

@IN.register('JSON', type = 'theme_format')
class JSON(html):
	'''JSON Theme fotmat class
	'''

@IN.register('XML', type = 'theme_format')
class XML(html):
	'''XML Theme fotmat class
	'''

@IN.register('RSS', type = 'theme_format')
class RSS(XML):
	'''RSS Theme fotmat class
	'''

