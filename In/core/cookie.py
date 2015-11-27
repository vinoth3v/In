from http import cookies
import re
import datetime
import In.core.util as util

class Cookie:
	'''General SimpleCookie container for request and response objects.
	'''

	#__In_cookie_name__ = 'N'

	def __init__(self, rawcookie = None):
		self.cookie = cookies.SimpleCookie()
		if rawcookie is not None:
			self.cookie.load(rawcookie)

	def load(self, rawcookie):
		'''load the cookie from raw cookie string'''
		try:
			self.cookie.load(rawcookie)
		except Exception as e:
			IN.logger.debug()

	def get(self, name, default = None):
		'''Gets the value of the cookie with the given name, else default.'''
		try:
			return self.cookie[name].value
		except KeyError as e:
			return default

	def has_key(self, name):
		'''Returns True if cookie name exists.'''
		try:
			self.cookie[name]
			return True
		except KeyError as e:
			return False

	def set(self, name, value, domain = None, expires = None, path = "/", expires_days = None, **kwargs):
		'''Sets the given cookie name/value with the given options.

		Additional keyword arguments are set on the Cookie.Morsel
		directly.
		See http://docs.python.org/library/cookie.html#morsel-objects
		for available attributes.
		'''

		if re.search(r"[\x00-\x20]", name + value):
			IN.logger.debug("Invalid cookie %r: %r" % (name, value))
			return

		self.cookie[name] = value
		morsel = self.cookie[name]

		if domain is None: # use the default domain
			domain = IN.APP.config.cookie_domain

		morsel["domain"] = domain

		if expires_days is not None and not expires:
			expires = datetime.datetime.utcnow() + datetime.timedelta( days = expires_days)
		if expires:
			morsel["expires"] = util.format_timestamp(expires)
		if path:
			morsel["path"] = path
		for k, v in kwargs.items():
			if k == 'max_age':
				k = 'max-age'
			morsel[k] = v

	def clear(self, name, path = '/', domain = None):
		# invalidate it by expire and empty value
		expires = datetime.datetime.utcnow() - datetime.timedelta(days=365)
		self.set(name, value = '', path = path, domain = domain, expires = expires)

	def values(self):
		return self.cookie.values()

	#def set_secret(self):
		#'''Set secret cookie wih name N.

		#'''

		#self.set(self.__In_cookie_name__, self.get_secret())

	#@staticmethod
	#def get_secret():
		#c = ()
		#time = time.time()
		#nabar_agent = IN.context.environ['HTTP_USER_AGENT']
		#hash = IN.APP.config.cookie_hash
