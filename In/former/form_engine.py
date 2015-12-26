#import In.core.response
import json
import hashlib


class FormerEngine:
	'''FormerEngine that handle form submits, validations, flow ...

	forms : per form / form state / per nabar
	form process submit before unnecessary page building
	page redirect to prevent double submit on refresh
	'''
	
	
	def __init__(self):
		# initiated on App init.
		# no context variables available

		# form cache bin
		self.cacher = IN.cacher.form

	def load(self, form_type, post = None, args = None, form_token = None):
		'''load and return the form by form_type'''

		context = IN.context
		
		if args is None:
			args = {}
		if post is None:
			post = {}

		try:
			# used for static cache of forms **per request only**
			context.static_cache['forms']
		except KeyError:
			context.static_cache['forms'] = {}

		nabar_id = str(context.nabar.id)
		
		if form_token: # load args from token cache
			cache_key = ':'.join((form_type, nabar_id, form_token))
			args = self.cacher.get(cache_key)
			if args is None:
				args = {}
		else:
			# get form token
			try:
				form_token = args['data']['form_token']
			except:
				# generate form token
				json_hash = json.dumps(args, skipkeys = True, ensure_ascii = False, sort_keys = True)
				form_token = hashlib.md5(json_hash.encode('utf-8')).hexdigest()
			cache_key = ':'.join((form_type, nabar_id, form_token))
			
			# save the cache
			self.cacher.set(cache_key, args)

		
		if 'data' not in args:
			args['data'] = {}
		
		# always set form token
		args['data']['form_token'] = form_token
		
		# set if partial submit
		if 'partial' in post and int(post['partial']) == 1:
			args['data']['partial'] = True
		
		if cache_key in context.static_cache['forms']:
			# the form from same request, loaded in early action form process
			return context.static_cache['forms'][cache_key]
		

		former = None
		
		formclass = IN.register.get_class(form_type, 'Object')
		if formclass is None:
			# use default
			formclass = Form
			
		former = formclass.Former
		if not issubclass(former.__class__, FormFormer):
			former = Form.Former
		
		form = former.load(form_type, post, args)

		# unexpected error?
		if form is None:
			return None
		
		# invoke form hooks
		prefix = 'form_load'

		# hook form_load		
		IN.hook_invoke(prefix, form, post, args)

		# hook by form type
		IN.hook_invoke('_'.join((prefix, form.__type__)), form, post, args)

		# save the form for context inrequest memory
		# so later form load from in this request use this
		# no multiple load, no muliple hook invoke
		context.static_cache['forms'][cache_key] = form
		
		return form

	def process(self, context, action, form, post, **args):
		'''Process the form validate, submit.

		TODO: partial submit/ajax field update
		'''

		ajax = context.request.ajax

		if ajax:
			# if ajax, just process the form and return result, prevent to run next action
			# if no ajax, normal page processing will be continued
			action.pass_next = False

		form.has_errors = False # reset

		try:
			
			# former validations
			self.validate(form, post)

		except Exception as e:
			form.has_errors = True
			IN.logger.debug()
			if ajax: # display ajax validation errors
				context.response = In.core.response.FormResponse(output = form)
			return

		if form.has_errors:
			if ajax: # display ajax validation errors
				context.response = In.core.response.FormResponse(output = form)
			return

		# submit the form
		try:
			# submit
			self.submit(form, post)
		except Exception as e:
			form.has_errors = True
			IN.logger.debug()
			if ajax: # display ajax validation errors
				context.response = In.core.response.FormResponse(output = form)
			return
		
		# redirect
		go_path = context.request.go
		if go_path:
			return context.redirect(go_path, ajax_redirect = False)
			
		if form.redirect is not None:			
			return context.redirect(form.redirect, ajax_redirect = form.ajax_redirect)

		if ajax and not form.context_response_changed: # process ajax response for the form submit
			context.response = In.core.response.FormResponse(output = form)
			
	def validate(self, form, post):
		
		former = form.Former
		form_type = form.__type__
		
		if form.partial:
			
			IN.hook_invoke('_'.join(('form_process', form_type, 'pre_validate_partial')), form, post)
			former.validate_partial(form, post)
			IN.hook_invoke('_'.join(('form_process', form_type, 'validate_partial')), form, post)
			
		else:	
			
			# validate the form fields
			self.validate_form_fields(form)

			IN.hook_invoke('_'.join(('form_process', form_type, 'pre_validate')), form, post)
			former.validate(form, post)
			IN.hook_invoke('_'.join(('form_process', form_type, 'validate')), form, post)

	def submit(self, form, post):
		
		former = form.Former
		form_type = form.__type__
		
		if form.partial:
			
			# prepare data to submit
			former.submit_prepare_partial(form, post)
			
			IN.hook_invoke('_'.join(('form_process', form_type, 'pre_submit_partial')), form, post)
			former.submit_partial(form, post)
			IN.hook_invoke('_'.join(('form_process', form_type, 'submit_partial')), form, post)
			
		else:
			
			# prepare data to submit
			former.submit_prepare(form, post)
			
			IN.hook_invoke('_'.join(('form_process', form_type, 'pre_submit')), form, post)
			former.submit(form, post)
			IN.hook_invoke('_'.join(('form_process', form_type, 'submit')), form, post)

	def validate_form_fields(self, obj, form = None):
		'''Valuate all form fields'''

		if form is None:
			form = obj
			#form.has_errors = False # reset # Error: reset by other field validations
		obj.has_errors = False # reset

		try: # skip if obj dont need validation
			validation_rule = obj.validation_rule
			value = obj.value

			if validation_rule is not None: # and check value
				try:
					result = IN.valuator.validate(value, validation_rule)
					if not result[0]:
						obj.has_errors = form.has_errors = True # set to form too
						if result[1]:
							obj.error_message = result[1]
				except Exception as e: # error as False
					IN.logger.debug()
					obj.has_errors = form.has_errors = True

		except AttributeError as e:
			IN.logger.debug()

		# validate all items # no break
		for key, sub_obj in obj.items():
			# recursive validate
			self.validate_form_fields(sub_obj, form)

	def is_form_submit(self, request):

		post = request.args['post']
		if not post:
			return False
		try:
			post['form_id'],
			post['form_type']
			post['form_token']
			# validate form token
			return self.validate_form_token(post)
			
		except KeyError as e:
			return False

	def load_form_from_submit(self, post = None, same_domain_check = True):

		context = IN.context
		nabar_id = context.nabar.id
		
		if post is None:
			post = context.request.args['post']

		if not post:
			return None

		if same_domain_check:
			if not context.request.same_referrer:
				return context.bad_request()

		try:
			
			form_id = post['form_id'],
			form_type = post['form_type']
			form_token = post['form_token']
			
		except KeyError:
			return None

		# load the form
		try:
			
			#load args from token
			cache_key = ':'.join((form_type, str(nabar_id), form_token))
			#print('form cache get ', cache_key)
			args = self.cacher.get(cache_key)
			if args is None:
				args = {}
			form = self.load(form_type, post, args, form_token = form_token)

			return form
		except Exception as e:
			IN.logger.debug()

	def validate_form_token(self, post):
		# TODO: validate it
		
		form_id, token = post['form_id'], post['form_token']
		
		return True

	def new_form_token(self):
		return In.core.token_verification.create_random_token()
