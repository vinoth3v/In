import json
import urllib
import cgi, tempfile, os, random


from In.core.cookie import Cookie
from http.cookies import CookieError

class Request:

	def __init__(self, context):

		self.referrer = context.environ.get('HTTP_REFERER', None)
		
		self.referrer_parsed = None
		
		self.path = context.environ.get('PATH_INFO', '')
		
		# unicode from latin-1
		try:
			self.path = self.path.encode('latin-1').decode('utf-8')
		except Exception as e:
			IN.logger.debug()
		
		if self.path.startswith('/'):
			self.path = self.path[1:]
		
		self.path_alias = self.path
		
		# get assign system path
		self.path_parts = self.path.split('/')
		
		
		# set original path from path alias
		if self.path and self.path_parts[0] != IN.APP.config.pfpp:
			path = In.core.action.route_path_from_alias(self.path)
			if path != self.path:
				self.path_parts = path.split('/')
				self.path = path
		
		self.path_tokenized = self.path
		self.path_tokenized_values = {}
		
		self.method = context.environ.get('REQUEST_METHOD', 'GET').upper()

		self.args = {
			'query' : {},
			'post'  : {},
		}

		query = self.args['query']
		post = self.args['post']

		self.__args__ = []
		self.output_format = 'html' # default

		# if context.environ['REQUEST_METHOD'] == 'GET': # always query values available
		
		if 'QUERY_STRING' in context.environ:
			
			query_vars = urllib.parse.parse_qs(context.environ['QUERY_STRING'])
			
			for key in query_vars:
				data = query_vars[key]

				l = key.split('[')
				lpost, lkey = self.__process_query_key(l, query)

				if len(data) == 1:
					lpost[lkey] = data[0]
				else:
					lpost[lkey] = data

		if self.method == 'POST' and 'wsgi.input' in context.environ:
			'''Process the file/form uploads.

			GET form submits are not supported now. you can handle that with your custom action.
			'''

			post_data = cgi.FieldStorage(fp = context.environ['wsgi.input'], environ = context.environ, keep_blank_values = True )
			
			process_file = In.file.process_uploaded_file
			process_it = lambda data: process_file(data) if data.filename else data.value

			for key in post_data:

				data_item = post_data[key]

				l = key.split('[')
				lpost, lkey = self.__process_query_key(l, post)

				if type(data_item) is list: # multiple values
					if len(data_item) == 1:
						lpost[lkey] = process_it(data_item[0])
					else:
						lpost[lkey] = [process_it(v) for v in data_item]
						#post[key] = list(map(process_it, data_item))
				else:
					lpost[lkey] = process_it(data_item)

			# process ajax_args to dict
			if 'ajax_args' in post and type(post['ajax_args']) is str:
				try:
					post['ajax_args'] = json.loads(post['ajax_args'])
				except Exception:
					post['ajax_args'] = {} # must be dict
					IN.logger.debug()
					
			
		self.init_cookie(context.environ.get('HTTP_COOKIE', ''))
		
		#pprint(context.environ)
		#pprint('PPPOOSSSSSSST', self.args)
	
	def init_cookie(self, cookie = None):
		# load the cookie
		try:
			self.cookie = Cookie(cookie)
		except CookieError as e:
			IN.logger.debug()
			self.cookie = Cookie()

	def __process_query_key(self, l, parent):
		key = l[0].replace(']', '')
		if len(l) == 1:
			if key not in parent:
				parent[key] = None
			return parent, key
		else:
			if key not in parent:
				parent[key] = {}
			return self.__process_query_key(l[1:], parent[key])

	@property
	def path_with_query(self):
		if not self.args['query']:
			return self.path
		return '?'.join((self.path, IN.context.environ['QUERY_STRING']))

	@property
	def is_secure(self):
		return 'HTTPS' in IN.context.environ and IN.context.environ['HTTPS'] == 'on'

	@property
	def host(self):
		return IN.context.environ['HTTP_HOST'] or IN.context.environ['SERVER_NAME']

	@property
	def ip(self):
		try:
			return IN.context.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
		except Exception:
			return IN.context.environ['REMOTE_ADDR']

	@property
	def ajax(self):
		if 'HTTP_X_REQUESTED_WITH' in IN.context.environ:
			return IN.context.environ['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest'
		return 'ajax' in self.args['query']

	@property
	def ajax_lazy(self):
		return self.ajax and 'lazy_load' in self.args['post']

	@property
	def ajax_args(self):
		# form has post, a args may be in query
		return self.args['post'].get('ajax_args', None) or self.args['query'].get('ajax_args', {})
	
	
	@property
	def go(self):
		# form has post, a args may be in query
		return self.args['post'].get('go', None) or self.args['query'].get('go', None)
	
	@property
	def ajax_modal(self):
		return self.ajax and 'modal' in self.args['post']
	
	@property
	def same_referrer(self):
		'''Return True if request comes from same domain'''
		# TODO: use SERVER_NAME , SERVER_PORT  header?
		
		if self.referrer is None:
			return True
		if self.referrer_parsed is None:
			self.referrer_parsed = urllib.parse.urlparse(self.referrer)
		return self.host == self.referrer_parsed.netloc
	
	@property
	def referrer_path(self):
		'''returns path from referrer url'''
		
		if self.referrer is None:
			return ''
		if self.referrer_parsed is None:
			self.referrer_parsed = urllib.parse.urlparse(self.referrer)
		path = self.referrer_parsed.path
		if path.startswith('/'):
			path = path[1:]
		return path
		
	def validate(self):
		'''validate the request
		TODO:
		'''
		return True
