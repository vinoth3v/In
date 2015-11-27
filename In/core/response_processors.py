import os
from wsgiref.util import FileWrapper



def page_response_default_processor(start_response):
	context = IN.context
	if not context.response.headers.get('content-type', False):
		if context.request.output_format == 'html':
			context.response.headers.add_header('content-type', 'text/html', charset='utf-8')
		if context.request.output_format == 'json':
			context.response.headers.add_header('content-type', 'text/javascript', charset='utf-8')
		if context.request.output_format == 'xml':
			context.response.headers.add_header('content-type', 'text/xml', charset='utf-8')

	response_headers = context.response.headers.items()

	for c in context.response.cookies.values():
		response_headers.append(('Set-Cookie', c.output(header='')))

	args = {} #OrderedDict()
	#args[] = context.themer.def_tpl_type
	output = context.themer.theme(context.response.page, format = context.request.output_format, args)

	context.response.output = [bytes(output, 'utf-8')]

	start_response(str(context.response.status), response_headers)






def file_response_default_processor(start_response):

	response = IN.context.response

	if not response.headers.get('content-type', False):

		if response.file_path and not response.file_extension:
			response.file_extension = os.path.splitext(response.file_path)
		#print(response.file_extension)
		#print(httpgate.MimeTypes.mime_type(response.file_extension))
		response.headers.add_header('content-type', In.http.MimeTypes.mime_type(response.file_extension))
	#else:
		#print(IN.context.response.headers.get('content-type', False))

	response_headers = response.headers.items()

	response.output = FileWrapper(response.file)

	start_response(str(response.status), response_headers)

