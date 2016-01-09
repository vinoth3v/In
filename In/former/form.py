
class Form(HTMLObject):
	
	__always_add_id_attribute__ = True
	
	def __init__(self, data = None, items = None, post = None, **args):

		self.has_errors = self.submitted, self.prepared, self.processed = False, False, False

		self.method = 'POST'
		self.action = None
		self.ajax_redirect = True
		self.enctype = 'multipart/form-data'
		
		# TODO: make it {}, allow add/remove
		self.error_message = ''
		
		self.form_token = None
		
		# after form submit, redirected to this path if set
		self.redirect = None
		
		# all form processed data goes here, submit handler just save/process it
		self.processed_data = {}
		
		# partial rendering. we only theme and server these elements on
		# partial form ajax submit
		self.partial = False
		self.ajax_elements = []

		# after submit, form can add custom commands here.
		# it will be processed in addition to normal form response
		self.result_commands = None
		
		# if set to True, former will not set FormResponse
		# default form response will not be processed
		self.context_response_changed = None
		
		if data is None:
			data = {}

		if 'form_id' in data:
			data[id] = data['form_id']
		
		# save it here, so former can use it
		self.args = args
		
		super().__init__(data, items, **args)

		# replaced by former
		#self.submit_handler = data.get('submit_handler', None)
		#self.validate_handler = args.get('validate_handler', None)

		# creats the new random form token
		if self.form_token is None:
			self.form_token = IN.former

	
		self.css.append('ajax')
		
		# prevent browser to refill
		self.attributes['autocomplete'] = 'off'
		
	def get_attributes(self):
		super().get_attributes()

		self.attributes['method'] = self.method

		if self.action is None:
			self.action = '/' + IN.context.request.path_with_query

		self.attributes['action'] = self.action
		self.attributes['enctype'] = self.enctype

		return self.attributes


@IN.register('Form', type = 'Themer')
class FormThemer(ObjectThemer):

	def theme(self, obj, format, view_mode, args):
		super().theme(obj, format, view_mode, args)
		
		obj.css.append(obj.__type__)
		
		if obj.__type__ != obj.id:
			obj.css.append(obj.id)
			
		obj.css.append('ajax i-form')
		#obj.css.append('i-panel i-panel-box')

	def theme_process_variables(self, form, format, view_mode, args):
		super().theme_process_variables(form, format, view_mode, args)

		args['form_id'] = form.id
		args['form_type'] = form.__type__
		args['form_token'] = form.form_token

		if form.has_errors:
			excls = IN.APP.config.css['extra']
			if 'form_error_message' in excls:
				cls = excls['form_error_message']
			else:
				cls = ''
			if form.error_message:
				args['error_message'] = ''.join(('<div class="', cls, '">', form.error_message, '</div>'))
			else:
				args['error_message'] = ''
		else:
			args['error_message'] = ''
		
		args['info'] = form.info or ''
		args['title'] = form.title or ''
		

class FormFormerBase:

	@classmethod
	def load_arguments(cls, form_id, post, args):
		'''returns the arguments needed to pass to form class.'''
		return {}

	def load(self, form_id, post):
		''''''

	def submit(self, form, post):
		''''''		
	def submit_partial(self, form, post):
		''''''
		
	def submit_prepare(self, form, post):
		''''''	
	def submit_prepare_partial(self, form, post):
		''''''

	def validate(self, form, post):
		''''''	
	def validate_partial(self, form, post):
		''''''
	
	def ajax(self, form):
		''''''

@IN.register('Form', type = 'Former')
class FormFormer(FormFormerBase):

	def __init__(self, objcls, key, mem_type):
		self.form_class = objcls

	def load(self, form_type, post, args):
		
		# get the form class
		objclass = IN.register.get_class(form_type, 'Object')
		if objclass is None:
			objclass = Form
		if not issubclass(objclass, Form):
			raise In.form.InvalidFormIdException(s('Form id {form_type} is invalid.', {'form_type' : form_type}))

		# create form instance
		form = objclass(post = post, **args)

		return form


builtins.Form = Form
builtins.FormFormer = FormFormer
builtins.FormThemer = FormThemer
