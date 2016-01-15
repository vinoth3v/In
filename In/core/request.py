import json
import urllib
import cgi, tempfile, os, random


from In.core.cookie import Cookie
from http.cookies import CookieError

class Request:

	def __init__(self, context):
		
		environ = context.environ
		
		self.referrer = environ.get('HTTP_REFERER', None)
		
		self.referrer_parsed = None
		
		self.path = environ.get('PATH_INFO', '')
		
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
		
		self.method = environ.get('REQUEST_METHOD', 'GET').upper()
		
		
		#if len(self.path_parts) > IN.APP.config.max_request_path_parts:
			#context.bad_request()
		
		# moved to action
		# set original path from path alias
		#if self.path and self.path_parts[0] != IN.APP.config.pfpp:
			#path = In.core.action.route_path_from_alias(self.path)
			#if path != self.path:
				#self.path_parts = path.split('/')
				#self.path = path
		
		self.path_tokenized = self.path
		self.path_tokenized_values = {}
		
		self.__path_hook_tokens__ = None
		
		# for property args
		self.args_parsed = False		
		self.__args__ = None
		
		self.ajax_parsed = False
		self.__ajax__ = False
		
		self.ajax_args_parsed = False
		self.__ajax_args__ = None
		
		
		self.output_format = 'html' # default

		# if context.environ['REQUEST_METHOD'] == 'GET': # always query values available
		
		self.init_cookie(environ.get('HTTP_COOKIE', ''))
		
		#pprint(context.environ)
		
	
	@property
	def args(self):
		
		if self.args_parsed:
			return self.__args__
		
		self.__args__ = {
			'query' : {},
			'post'  : {},
		}
		
		query = self.__args__['query']
		post = self.__args__['post']
		
		context = IN.context
		
		environ = context.environ
		
		if 'QUERY_STRING' in environ:
			
			query_vars = urllib.parse.parse_qs(environ['QUERY_STRING'])
			
			for key in query_vars:
				data = query_vars[key]

				l = key.split('[')
				lpost, lkey = self.__process_query_key(l, query)

				if len(data) == 1:
					lpost[lkey] = data[0]
				else:
					lpost[lkey] = data

		if self.method == 'POST' and 'wsgi.input' in environ:
			'''Process the file/form uploads.

			GET form submits are not supported now. you can handle that with your custom action.
			'''

			post_data = cgi.FieldStorage(fp = environ['wsgi.input'], environ = environ, keep_blank_values = True )
			
			#pprint(post_data)
			
			process_file = IN.filer.process_uploaded_file
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
		
		self.args_parsed = True
		
		#pprint('PPPOOSSSSSSST', self.__args__)
		
		return self.__args__
		
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
		environ = IN.context.environ
		try:
			return environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
		except Exception:
			return environ['REMOTE_ADDR']

	@property
	def ajax(self):
		
		if self.ajax_parsed:
			return self.__ajax__
		
		if 'HTTP_X_REQUESTED_WITH' in IN.context.environ:
			self.__ajax__ = IN.context.environ['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest'
		else:
			self.__ajax__ = 'ajax' in self.args['query']
		
		self.ajax_parsed = True
		
		return self.__ajax__
		
	@property
	def ajax_lazy(self):
		return self.ajax and 'lazy_load' in self.args['post']

	@property
	def ajax_args(self):
		# form has post, a args may be in query
		if self.ajax_args_parsed:
			self.__ajax_args__
		
		self.__ajax_args__ = self.args['post'].get('ajax_args', None) or self.args['query'].get('ajax_args', {})
		
		self.ajax_args_parsed = True
		
		return self.__ajax_args__
	
	
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

	def path_hook_tokens(self):
		'''used to decide tabs, boxes by paths.
		
		# node/62094/edit
		[
			'node___edit',
			'node___edit_anything_after',
			'node___anything_after',
			'node_anything_after'
		]
		
		'''
		
		if self.__path_hook_tokens__ is not None: # prepare once
			return self.__path_hook_tokens__
		
		tokens = []
		
		org_path_tokenized = self.path_tokenized
		
		if org_path_tokenized:
			
			path_tokenized = org_path_tokenized.replace('*', '_').replace('/', '_').replace('-', '_')
			
			tokens.append(path_tokenized)
			
			# hook by anything_after path
			
			# content/*/edit
			# content___edit_anything_after
			# content___anything_after
			# content_anything_after
			
			token_paths = org_path_tokenized.split('/')
			while(token_paths):
				
				new_token_path = '/'.join(token_paths)
				new_token_path = new_token_path.replace('*', '_').replace('/', '_').replace('-', '_')

				new_token_path += '_anything_after'
				
				tokens.append(new_token_path)
				
				#token_paths = token_paths[:-1]
				del token_paths[-1]

		self.__path_hook_tokens__ = tokens
		#pprint(tokens)
		return self.__path_hook_tokens__
