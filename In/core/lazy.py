import json

from In.core.action import ActionObject

@IN.hook
def __context_early_action__(context):
	'''entry point: handle the submitted form

	'''

	if context.request.ajax_lazy:

		lazys = context.request.args['post']['lazy_load']
		
		if not lazys:
			return

		args = {
			'handler' : process_lazy,
			'handler_arguments' : {
				'lazys' : lazys
			},
			'pass_next' : False  # pass to default page loading
		}

		action_object = ActionObject(**args)

		return action_object


def process_lazy(context, action, lazys, **args):
	'''Process lazy_box_request

	used to lazy load object, forms, boxes, ...
	'''

	output_obj = Object()

	for key, l in lazys.items():
		try:
			args = l.get('args', {})
			load_args = args.get('load_args', {})

			if 'base_type' not in args:
				args['base_type'] = 'Object'
			
			# get the entity type class
			objclass = IN.register.get_class(args['type'], args['base_type'])
			if objclass:
				obj = objclass(**load_args)
				output_obj.add(obj)
		except Exception:
			IN.logger.debug()
			# ignore
			continue

	context.response = In.core.response.PartialResponse(output = output_obj)



class HTMLObjectLazy(In.html.tags.HTMLObject):

	delay = 2000
	lazy_args = {}
	
	#def __init__(self, data = None, items = None, **args):
		#super().__init__(data, items, **args)


@IN.register('HTMLObjectLazy', type = 'Themer')
class HTMLObjectLazyThemer(In.html.tags_themer.HTMLObjectThemer):
	
	__invoke_theme_format_view_mode_alter__ = True
	
	def __theme_format_view_mode_alter__(self, format, view_mode, args):
		# lazy in lazy?
		if args['context'].request.ajax_lazy:
			return format, view_mode
		else:
			return format, 'lazy'
		
	def theme(self, obj, format, view_mode, args):
		obj.attributes['id'] = str(obj.id)
		if view_mode != 'lazy':
			super().theme(obj, format, view_mode, args)

	def theme_done(self, obj, format, view_mode, args):
		if view_mode != 'lazy':
			super().theme_done(obj, format, view_mode, args)

	def theme_items(self, obj, format, view_mode, args):
		if view_mode != 'lazy':
			super().theme_items(obj, format, view_mode, args)

	def theme_process_variables(self, obj, format, view_mode, args):
		theme_output = obj.theme_current_output
		args['delay'] = obj.delay
		if view_mode != 'lazy':
			super().theme_process_variables(obj, format, view_mode, args)
			args['children'] = theme_output['output']['children']
		else:
			# return ajax placeholder
			obj.lazy_args['type'] = obj.__type__
			try:
				json_args = json.dumps(obj.lazy_args, skipkeys = True, ensure_ascii = False)
			except Exception as e:
				raise e
			args['id'] = obj.id
			args['type'] = obj.__type__
			args['delay'] = obj.delay
			args['args'] = json_args
			
builtins.HTMLObjectLazy = HTMLObjectLazy
builtins.HTMLObjectLazyThemer = HTMLObjectLazyThemer
