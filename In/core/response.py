import os
import json
from wsgiref.util import FileWrapper


class ResponseBase:
	'''A base IN HTTP response class.'''

	def __init__(self, **args):
		self.status = args.get('status', In.http.Status.OK)
		self.output = args.get('output', None)

	def process(self, context):

		# output must be set previously
		output = self.output
		if output is None:
			output = ''

		output = output.encode('utf-8')
		context.headers.add_header('Content-Length', str(len(output)))
		self.output = [output]

	def __call__(self, context):
		self.process(context)

	#def __del__(self):
		##del self.output
		#self.output = None

	def set_output(self, output):
		self.output = output

class ObjectResponse(ResponseBase):
	'''Theme any Object and respond as string

	self.output will be IN Object.
	'''

	def process(self, context):

		output_format = context.request.output_format
		if not context.headers.get('Content-Type', False):
			if output_format == 'html':
				context.headers.add_header('Content-Type', 'text/html', charset='utf-8')
			if output_format == 'json':
				context.headers.add_header('Content-Type', 'application/json', charset='utf-8')
			if output_format == 'xml':
				context.headers.add_header('Content-Type', 'text/xml', charset='utf-8')

		#theme = IN.themer.theme
		#t0 = datetime.datetime.now()
		#self.output.Themer.theme_tpl_type = 'py'
		#for i in range(9999):
			#theme(self.output, format = output_format)
			#self.output.theme_output = None


		output = IN.themer.theme(self.output, format = output_format)

		#Python3 needs unicode bytes
		output = output.encode('utf-8')
		context.headers.add_header('Content-Length', str(len(output)))

		self.output = [output]

class PageResponse(ObjectResponse):
	'''Page response '''

	def process(self, context):

		output_format = context.request.output_format

		format = output_format
		
		if self.output:
			IN.boxer.decide_page_boxes(context, self.output, format)
			IN.APP.decide_page_assets(context, self.output, format)
			

		# if not ajax
		if not context.request.ajax:
			return super().process(context)

		output = []

		ajax_args = context.request.ajax_args or {}
		
		#TODO: fix: content panel classes not updated if panel supplied
		
		# theme and return only ajax elements
		panel = None
		if 'panel' in ajax_args:
			panel = ajax_args['panel']
		ajax_children = self.output.Themer.ajax_children(self.output, panel = panel)
		for key, child in ajax_children.items():
			output.append({
				'method' : 'replace',
				'args' : ['#' + key, IN.themer.theme(child, format = output_format)],
			})
		
		output.append({
			'method' : 'title',
			'args' : [IN.context.page_title or IN.APP.config.app_title]
		})
		
		output = {
			'commands' : output,
		}
		

		output = json.dumps(output, skipkeys = True, ensure_ascii = False)
		output = output.encode('utf-8')
		context.headers.add_header('Content-Length', str(len(output)))

		if not context.headers.get('Content-Type', False):
			if output_format == 'html':
				context.headers.add_header('Content-Type', 'text/html', charset='utf-8')
			if output_format == 'json':
				context.headers.add_header('Content-Type', 'application/json', charset='utf-8')


		self.output = [output]

class FormResponse(ObjectResponse):
	'''Form response '''

	def process(self, context):

		output_format = context.request.output_format
		if not context.headers.get('Content-Type', False):
			if output_format == 'html':
				context.headers.add_header('Content-Type', 'text/html', charset='utf-8')
			if output_format == 'json':
				context.headers.add_header('Content-Type', 'application/json', charset='utf-8')


		ajax = context.request.ajax
		form = self.output
		
		_theme = IN.themer.theme
		
		if ajax:
			if not self.output.partial:

				output = _theme(self.output, format = output_format)
				
				element_id = context.request.args['post']['form_id']
				output = {
					'commands' : [{
						'method' : 'replace',
						'args' : ['#' + element_id, output]
					}],
				}
				
			else:
				output = {'commands' : []}
				
				for id in form.ajax_elements:
					if type(id) is str:
						element = form.get_item(id)
					else:
						element = id
						id = element.id
					if element:
						themed_element = _theme(element, format = output_format)
						output['commands'].append({
							'method' : 'replace',
							'args' : ['#' + id, themed_element]
						})
						
			# add additional commands
			if form.result_commands is not None:
				output['commands'].extend(form.result_commands)
			
			# prevent empty result
			# output the whole form if no ajax elements and no result commands
			if not form.ajax_elements and not form.result_commands:
				themed_form = _theme(self.output, format = output_format)
				
				element_id = context.request.args['post']['form_id']
				output['commands'].append({
					'method' : 'replace',
					'args' : ['#' + element_id, themed_form]
				})
			
			
			if form.redirect:
				output.redirect = form.redirect
			
			output = json.dumps(output, skipkeys = True, ensure_ascii = False)
		else:
			
			output = _theme(self.output, format = output_format)
			
		output = output.encode('utf-8')
		context.headers.add_header('Content-Length', str(len(output)))

		self.output = [output]

class PartialResponse(ObjectResponse):
	'''Page response '''

	def process(self, context):

		output_format = context.request.output_format

		output = []

		# theme and return only ajax elements
		for key, child in self.output.items():
			id = str(key)
			if not id.startswith('#') and not id.startswith('.'):
				id = '#' + id
			output.append({
				'method' : 'replace',
				'args' : [id, IN.themer.theme(child, format = output_format)],
			})

		output = {
			'commands' : output,
		}

		output = json.dumps(output, skipkeys = True, ensure_ascii = False)
		output = output.encode('utf-8')
		context.headers.add_header('Content-Length', str(len(output)))

		if not context.headers.get('Content-Type', False):
			if output_format == 'html':
				context.headers.add_header('Content-Type', 'text/html', charset='utf-8')
			if output_format == 'json':
				context.headers.add_header('Content-Type', 'application/json', charset='utf-8')


		self.output = [output]

class CustomResponse(ObjectResponse):
	'''Custom response '''

	def process(self, context):

		output_format = context.request.output_format

		output = {
			'commands' : self.output,
		}

		output = json.dumps(output, skipkeys = True, ensure_ascii = False)
		output = output.encode('utf-8')
		context.headers.add_header('Content-Length', str(len(output)))

		if not context.headers.get('Content-Type', False):
			if output_format == 'html':
				context.headers.add_header('Content-Type', 'text/html', charset='utf-8')
			if output_format == 'json':
				context.headers.add_header('Content-Type', 'application/json', charset='utf-8')

		self.output = [output]

class JSONResponse(ObjectResponse):
	'''Custom response '''

	def process(self, context):

		output_format = 'json'

		output = json.dumps(self.output, skipkeys = True, ensure_ascii = False)
		output = output.encode('utf-8')
		context.headers.add_header('Content-Length', str(len(output)))

		context.headers.add_header('Content-Type', 'application/json', charset='utf-8')

		self.output = [output]
		
		self.status = In.http.Status.OK

class FileResponse(ResponseBase):
	'''Page response.'''

	def __init__(self, file = None, file_path = '', file_extension = '', file_length = 0, **args):
		super().__init__(**args)

		self.file = file

		# it can be empty because the file can be wrapped object or custom stream
		# and it can be the original file path if the url is a alias or secured.
		self.file_path      = file_path

		# can be set
		self.file_extension = file_extension

		# if set it will be added to the header
		self.file_length    = file_length

		if self.file_path:
			if self.file is None:
				self.file = open(self.file_path, 'rb')
			if not self.file_extension:
				self.file_extension = os.path.splitext(self.file_path)[1]

	def process(self, context):
		if self.file is None:
			# TODO: if no file set
			pass

		if not context.headers.get('Content-Type', False):
			if not self.file_extension and self.file_path:
				self.file_extension = os.path.splitext(self.file_path)[1]
			context.headers.add_header('Content-Type', In.http.MimeTypes.mime_type(self.file_extension))

		self.output = FileWrapper(self.file)


class EmptyResponse(ResponseBase):
	'''just send http status code and optional output.

	EmptyResponse(status = In.http.Status.NOT_MODIFIED)
	'''

	def __init__(self, **args):
		super().__init__(**args)

class BadResponse(EmptyResponse):
	'''send Bad request response.'''

	def __init__(self, **args):
		args['status'] = args.get('status', In.http.Status.BAD_REQUEST)
		super().__init__(**args)

	def process(self, context):

		if self.output is None:
			self.output = '''<!DOCTYPE HTML><html><head><title>400 Bad Request</title></head>
		<body><h1>Bad Request</h1></body>
		</html>'''
		super().process(context)

class RedirectResponse(EmptyResponse):
	'''Send Bad request response.'''

	def __init__(self, **args):
		args['status'] = args.get('status', In.http.Status.SEE_OTHER)
		super().__init__(**args)

		self.path = args.get('path', '/')
		if not self.path.startswith(('/', 'http:', 'https:')):
			self.path = '/' + self.path
		
		if self.path.startswith(('//', 'http:', 'https:')):
			args['ajax_redirect'] = False
			
		self.ajax_redirect = args.get('ajax_redirect', True)

	def process(self, context):

		ajax = context.request.ajax

		if ajax:
			output = {
				'commands' : [{
						'method' : 'redirect',
						'args' : [self.path, 1 if self.ajax_redirect else 0],
					}
				],
			}

			# TODO: attach css and js assets

			output = json.dumps(output, skipkeys = True, ensure_ascii = False)

			context.headers.add_header('Content-Type', 'application/json', charset='utf-8')

			output = output.encode('utf-8')
			context.headers.add_header('Content-Length', str(len(output)))

			# use OK response for ajax redirect otherwise browser will see 303 SEE_OTHER
			self.status = In.http.Status.OK
		else:
			output = self.output
			if output is None:
				output = ''
			context.headers.add_header('Location', self.path)

		self.output = [output]

class NotFoundResponse(PageResponse):
	'''Not Found response.'''

	def __init__(self, **args):

		if not IN.context.request.ajax:
			# 404 only if normal page
			args['status'] = In.http.Status.NOT_FOUND
		else:
			# TODO: find other status code
			args['status'] = In.http.Status.OK

		args['status'] = args.get('status', In.http.Status.NOT_FOUND)
		super().__init__(**args)

class AccessDeniedResponse(PageResponse):
	'''AccessDenied response.'''

	def __init__(self, **args):

		if not IN.context.request.ajax:
			# 403 only if normal page
			args['status'] = In.http.Status.FORBIDDEN
		else:
			# TODO: find other status code
			args['status'] = In.http.Status.OK

		args['status'] = args.get('status', In.http.Status.FORBIDDEN)
		super().__init__(**args)

