import string
from collections import defaultdict


from .admin import *


class Stringer:
	'''String translator'''

	
	def __init__(self):

		#self.__collect__ = False
		#self.site_language = site_language

		# strings = {language : {context : strings}}
		self.strings = defaultdict(lambda : defaultdict(dict))


		# override default
		builtins.s = self.s

		# build strings from db to locale inmemory cache
		self.build_translated_strings()
		
	def build_translated_strings(self):
		try:
			# nabar name auth
			cursor = IN.db.execute('''select * FROM config.config_string''')
			
			if cursor.rowcount == 0:
				return

			for row in cursor:
				language = row['language']
				translated = row['translated']
				tstring = row['tstring']
				context = row['context']
				string = row['string']
				
				lang_lc = self.strings[language]
				lang_strings = lang_lc[context]
				
				lang_strings[string] = {
					'string' : tstring,
					'translated' : translated, # set always as translated, so update_db will not insert this again to db
					'new' : 0,
				}

		except Exception as e:
			IN.logger.debug()

		
	def s(self, string, args = None, lc = '', language = None):
		'''This is the wrapper function for i18n strings.

		lc : language context
		'''

		themer = IN.themer
		
		if args is None:
			args = {}

		#language = self.site_language
		if language is None:
			try:
				language = IN.context.language
			except AttributeError as e:
				language = IN.APP.config.language
		
		if language != 'en': # get translation only if not en
			try:
				string = self.strings[language][lc][string]['string']
			except KeyError as e:
				
				self.strings[language][lc][string] = {
					'string' : string,
					'translated' : 0,
					'new' : True
				}

		return themer.string_format(string, args)
		#return string.format_map(args)

	#def collect(self, yes = True):
		#self.__collect__ = yes
	


dt_formats = {
	'simple' : '%d/%m/%y',
	'medium' : '%a %d. %b %Y',
	'long' : '%A, %d. %B %Y %I:%M%p',
}


def dtformat(dt, format = 'medium'):
	f = dt_formats.get(format, '')
	if f:
		return dt.strftime(f)
	return dt.strftime(format)

