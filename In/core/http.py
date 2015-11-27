
class WSGIServerException(Exception):
	pass

class HTTPStatus:
	def __init__(self, code, message, description = ''):
		self.code = code
		self.message = message
		self.description = description

	def __str__(self):
		return ' '.join((str(self.code), self.message))

	def __repr__(self):
		return self.__str__()

class Status:
	'''HTTP Status Messages & Codes
	'''

	# See http://www.w3.org/hypertext/WWW/Protocols/HTTP/HTRESP.html

	CONTINUE                     = HTTPStatus(100, 'CONTINUE', 'Request received, please continue')
	SWITCHING_PROTOCOLS          = HTTPStatus(101, 'SWITCHING PROTOCOLS', 'Switching to new protocol; obey Upgrade header')
	PROCESSING                   = HTTPStatus(102, 'PROCESSING', 'PROCESSING')

	OK                           = HTTPStatus(200, 'OK', 'Request fulfilled, document follows')
	CREATED                      = HTTPStatus(201, 'CREATED', 'Document created, URL follows')
	ACCEPTED                     = HTTPStatus(202, 'ACCEPTED', 'Request accepted, processing continues off-line')
	NON_AUTHORITATIVE            = HTTPStatus(203, 'NON AUTHORITATIVE', 'Request fulfilled from cache')
	NO_CONTENT                   = HTTPStatus(204, 'NO CONTENT', 'Request fulfilled, nothing follows')
	RESET_CONTENT                = HTTPStatus(205, 'RESET CONTENT', 'Clear input form for further input.')
	PARTIAL_CONTENT              = HTTPStatus(206, 'PARTIAL CONTENT', 'Partial content follows.')
	MULTI_STATUS                 = HTTPStatus(207, 'MULTI STATUS')

	MULTIPLE_CHOICES             = HTTPStatus(300, 'MULTIPLE CHOICES', 'Object has several resources -- see URI list')
	MOVED_PERMANENTLY            = HTTPStatus(301, 'MOVED PERMANENTLY', 'Object moved permanently -- see URI list')
	MOVED_TEMPORARILY            = HTTPStatus(302, 'MOVED TEMPORARILY', 'Object moved temporarily -- see URI list')
	SEE_OTHER                    = HTTPStatus(303, 'SEE OTHER', 'Object moved -- see Method and URL list')
	NOT_MODIFIED                 = HTTPStatus(304, 'NOT MODIFIED', 'Document has not changed since given time')
	USE_PROXY                    = HTTPStatus(305, 'USE PROXY', 'You must use proxy specified in Location to access this resource.')
	TEMPORARY_REDIRECT           = HTTPStatus(307, 'TEMPORARY REDIRECT', 'Object moved temporarily -- see URI list')

	BAD_REQUEST                  = HTTPStatus(400, 'BAD REQUEST', 'Bad request syntax or unsupported method')
	UNAUTHORIZED                 = HTTPStatus(401, 'UNAUTHORIZED', 'No permission -- see authorization schemes')
	PAYMENT_REQUIRED             = HTTPStatus(402, 'PAYMENT REQUIRED', 'No payment -- see charging schemes')
	FORBIDDEN                    = HTTPStatus(403, 'FORBIDDEN', 'Request forbidden -- authorization will not help')
	NOT_FOUND                    = HTTPStatus(404, 'NOT FOUND', 'Nothing matches the given URI')
	METHOD_NOT_ALLOWED           = HTTPStatus(405, 'METHOD NOT ALLOWED', 'Specified method is invalid for this server.')
	NOT_ACCEPTABLE               = HTTPStatus(406, 'NOT ACCEPTABLE', 'URI not available in preferred format.')
	PROXY_AUTHENTICATION_REQUIRED= HTTPStatus(407, 'PROXY AUTHENTICATION REQUIRED' 'You must authenticate with this proxy before proceeding.')
	REQUEST_TIME_OUT             = HTTPStatus(408, 'REQUEST TIME OUT', 'Request timed out; try again later.')
	CONFLICT                     = HTTPStatus(409, 'CONFLICT', 'Request conflict.')
	GONE                         = HTTPStatus(410, 'GONE', 'URI no longer exists and has been permanently removed.')
	LENGTH_REQUIRED              = HTTPStatus(411, 'LENGTH REQUIRED', 'Client must specify Content-Length.')
	PRECONDITION_FAILED          = HTTPStatus(412, 'PRECONDITION FAILED', 'Precondition in headers is false.')
	REQUEST_ENTITY_TOO_LARGE     = HTTPStatus(413, 'REQUEST ENTITY TOO LARGE', 'Entity is too large.')
	REQUEST_URI_TOO_LARGE        = HTTPStatus(414, 'REQUEST URI TOO LARGE', 'URI is too long.')
	UNSUPPORTED_MEDIA_TYPE       = HTTPStatus(415, 'UNSUPPORTED MEDIA TYPE', 'Entity body in unsupported format.')
	RANGE_NOT_SATISFIABLE        = HTTPStatus(416, 'RANGE NOT SATISFIABLE', 'Cannot satisfy request range.')
	EXPECTATION_FAILED           = HTTPStatus(417, 'EXPECTATION FAILED', 'Expect condition could not be satisfied.')
	UNPROCESSABLE_ENTITY         = HTTPStatus(422, 'UNPROCESSABLE ENTITY', 'UNPROCESSABLE ENTITY')
	LOCKED                       = HTTPStatus(423, 'LOCKED', 'LOCKED')
	FAILED_DEPENDENCY            = HTTPStatus(424, 'FAILED DEPENDENCY', 'FAILED DEPENDENCY')

	INTERNAL_SERVER_ERROR        = HTTPStatus(500, 'INTERNAL SERVER ERROR', 'Server got itself in trouble')
	NOT_IMPLEMENTED              = HTTPStatus(501, 'NOT IMPLEMENTED', 'Server does not support this operation')
	BAD_GATEWAY                  = HTTPStatus(502, 'BAD GATEWAY', 'Invalid responses from another server/proxy.')
	SERVICE_UNAVAILABLE          = HTTPStatus(503, 'SERVICE UNAVAILABLE', 'The server cannot process the request due to a high load')
	GATEWAY_TIME_OUT             = HTTPStatus(504, 'GATEWAY TIME OUT', 'The gateway server did not receive a timely response')
	HTTP_VERSION_NOT_SUPPORTED   = HTTPStatus(505, 'HTTP VERSION NOT SUPPORTED', 'Cannot fulfill request.')
	VARIANT_ALSO_VARIES          = HTTPStatus(506, 'VARIANT ALSO VARIES', 'VARIANT ALSO VARIES')
	INSUFFICIENT_STORAGE         = HTTPStatus(507, 'INSUFFICIENT STORAGE', 'INSUFFICIENT STORAGE')
	NOT_EXTENDED                 = HTTPStatus(510, 'NOT EXTENDED', 'NOT EXTENDED')



class MimeTypes:
	# http://www.isi.edu/in-notes/iana/assignments/media-types
	mime_types = {
		'.a'      : 'application/octet-stream',
		'.ai'     : 'application/postscript',
		'.aif'    : 'audio/x-aiff',
		'.aifc'   : 'audio/x-aiff',
		'.aiff'   : 'audio/x-aiff',
		'.au'     : 'audio/basic',
		'.avi'    : 'video/x-msvideo',
		'.bat'    : 'text/plain',
		'.bcpio'  : 'application/x-bcpio',
		'.bin'    : 'application/octet-stream',
		'.bmp'    : 'image/x-ms-bmp',
		'.c'      : 'text/plain',
		'.cdf'    : 'application/x-cdf',
		'.cdf'    : 'application/x-netcdf',
		'.cpio'   : 'application/x-cpio',
		'.csh'    : 'application/x-csh',
		'.css'    : 'text/css',
		'.dll'    : 'application/octet-stream',
		'.doc'    : 'application/msword',
		'.docx'   : 'application/msword',
		'.dot'    : 'application/msword',
		'.dvi'    : 'application/x-dvi',
		'.eml'    : 'message/rfc822',
		'.eps'    : 'application/postscript',
		'.etx'    : 'text/x-setext',
		'.exe'    : 'application/octet-stream',
		'.gif'    : 'image/gif',
		'.gtar'   : 'application/x-gtar',
		'.h'      : 'text/plain',
		'.hdf'    : 'application/x-hdf',
		'.htm'    : 'text/html',
		'.html'   : 'text/html',
		'.ief'    : 'image/ief',
		'.jpe'    : 'image/jpeg',
		'.jpeg'   : 'image/jpeg',
		'.jpg'    : 'image/jpeg',
		'.jsx'    : 'text/jsx',
		'.js'     : 'application/x-javascript',
		'.json'	  : 'application/json',
		'.ksh'    : 'text/plain',
		'.latex'  : 'application/x-latex',
		'.m1v'    : 'video/mpeg',
		'.man'    : 'application/x-troff-man',
		'.me'     : 'application/x-troff-me',
		'.mht'    : 'message/rfc822',
		'.mhtml'  : 'message/rfc822',
		'.mid'    : 'audio/midi',
		'.midi'   : 'audio/midi',
		'.mif'    : 'application/x-mif',
		'.mov'    : 'video/quicktime',
		'.movie'  : 'video/x-sgi-movie',
		'.mp2'    : 'audio/mpeg',
		'.mp3'    : 'audio/mpeg',
		'.mp4'    : 'audio/mpeg',
		'.mpa'    : 'video/mpeg',
		'.mpe'    : 'video/mpeg',
		'.mpeg'   : 'video/mpeg',
		'.mpg'    : 'video/mpeg',
		'.ms'     : 'application/x-troff-ms',
		'.nc'     : 'application/x-netcdf',
		'.nws'    : 'message/rfc822',
		'.o'      : 'application/octet-stream',
		'.obj'    : 'application/octet-stream',
		'.oda'    : 'application/oda',
		'.p12'    : 'application/x-pkcs12',
		'.p7c'    : 'application/pkcs7-mime',
		'.pct'    : 'image/pict',
		'.pbm'    : 'image/x-portable-bitmap',
		'.pdf'    : 'application/pdf',
		'.pfx'    : 'application/x-pkcs12',
		'.pgm'    : 'image/x-portable-graymap',
		'.pic'    : 'image/pict',
		'.pict'   : 'image/pict',
		'.pl'     : 'text/plain',
		'.png'    : 'image/png',
		'.pnm'    : 'image/x-portable-anymap',
		'.pot'    : 'application/vnd.ms-powerpoint',
		'.ppa'    : 'application/vnd.ms-powerpoint',
		'.ppm'    : 'image/x-portable-pixmap',
		'.pps'    : 'application/vnd.ms-powerpoint',
		'.ppt'    : 'application/vnd.ms-powerpoint',
		'.ps'     : 'application/postscript',
		'.pwz'    : 'application/vnd.ms-powerpoint',
		'.py'     : 'text/x-python',
		'.pyc'    : 'application/x-python-code',
		'.pyo'    : 'application/x-python-code',
		'.qt'     : 'video/quicktime',
		'.ra'     : 'audio/x-pn-realaudio',
		'.ram'    : 'application/x-pn-realaudio',
		'.ras'    : 'image/x-cmu-raster',
		'.rdf'    : 'application/xml',
		'.rgb'    : 'image/x-rgb',
		'.roff'   : 'application/x-troff',
		'.rtf'    : 'application/rtf',
		'.rtx'    : 'text/richtext',
		'.sgm'    : 'text/x-sgml',
		'.sgml'   : 'text/x-sgml',
		'.sh'     : 'application/x-sh',
		'.shar'   : 'application/x-shar',
		'.snd'    : 'audio/basic',
		'.so'     : 'application/octet-stream',
		'.src'    : 'application/x-wais-source',
		'.sv4cpio': 'application/x-sv4cpio',
		'.sv4crc' : 'application/x-sv4crc',
		'.swf'    : 'application/x-shockwave-flash',
		'.t'      : 'application/x-troff',
		'.tar'    : 'application/x-tar',
		'.tcl'    : 'application/x-tcl',
		'.tex'    : 'application/x-tex',
		'.texi'   : 'application/x-texinfo',
		'.texinfo': 'application/x-texinfo',
		'.tif'    : 'image/tiff',
		'.tiff'   : 'image/tiff',
		'.tr'     : 'application/x-troff',
		'.tsv'    : 'text/tab-separated-values',
		'.txt'    : 'text/plain',
		'.ustar'  : 'application/x-ustar',
		'.vcf'    : 'text/x-vcard',
		'.wav'    : 'audio/x-wav',
		'.wiz'    : 'application/msword',
		'.xbm'    : 'image/x-xbitmap',
		'.xlb'    : 'application/vnd.ms-excel',
	##    '.xls'    : 'application/excel',
		'.xls'    : 'application/vnd.ms-excel',
		'.xlsx'   : 'application/vnd.ms-excel',
		'.xml'    : 'text/xml',
		'.xpm'    : 'image/x-xpixmap',
		'.xsl'    : 'application/xml',
		'.xul'    : 'text/xul',
		'.xwd'    : 'image/x-xwindowdump',
		'.zip'    : 'application/zip',
	}

	@classmethod
	def mime_type(cls, ext, default = 'application/octet-stream'):
		try:
			return cls.mime_types[ext]
		except KeyError:
			return default


