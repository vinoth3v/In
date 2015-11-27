
class EMailMeta(ObjectMeta):

	__class_type_base_name__ = 'EMailBase'
	__class_type_name__ = 'EMail'

class EMailBase(Object, metaclass = EMailMeta):
	'''Base class of all IN EMail.

	'''
	__allowed_children__ = None
	__default_child__ = None
	

@IN.register('EMail', type = 'EMail')
class EMail(EMailBase):
	'''Base EMail class.

	'''
	
	#subject # obj.title
	
	to_name = None
	to_address = None
	
	# email body
	body_text = None
	body_html = None
	
	# optional 
	from_address = None
	from_name = None
	reply_to = None
	
	# not used for now
	attachments = None
	inline_images = None
	
	#def __init__(self, data = None, items = None, **args):
		#super().__init__(data, items, **args)
	
	def send(self):
		IN.mailer.send(self)
		
	@staticmethod
	def new(type, *pargs, **kargs):
		'''Helper function to create appropriate type of object.

		'''

		# get the class type
		objclass = IN.register.get_class(type, 'EMail')
		
		if objclass is None:
			# use the default
			objclass = EMail

		obj = objclass(*pargs, **kargs)

		return obj

@IN.register('EMail', type = 'Themer')
class EMailThemer(ObjectThemer):
	'''EMail themer'''

	def view_modes(self):
		modes = super().view_modes()
		#modes.add('html') # default is html
		modes.add('text')
		return modes
	
	def theme_process_variables(self, obj, format, view_mode, args):
		
		super().theme_process_variables(obj, format, view_mode, args)
		
		args['app_url'] = 'http://' + IN.APP.config.app_domain
		args['app_name'] = IN.APP.config.app_name
		args['app_title'] = IN.APP.config.app_title
		
		args['to_name'] = obj.to_name
		args['from_name'] = obj.from_name
		
		args['body_text'] = obj.body_text or ''
		args['body_html'] = obj.body_html or ''
		
		
builtins.EMail = EMail
