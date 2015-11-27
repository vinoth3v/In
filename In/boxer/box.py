import json
from In.html.tags import HTMLObject
from In.core.object_meta import ObjectMetaBase


class BoxMeta(ObjectMeta):

	__class_type_base_name__ = 'BoxBase'
	__class_type_name__ = 'Box'

class BoxBase(Object, metaclass = BoxMeta):
	'''Base class of all IN BoxBase.

	'''
	__allowed_children__ = None
	__default_child__ = None

@IN.register('Box', type = 'Box')
class Box(BoxBase):
	'''Base Box class.

	'''

	def __init__(self, data = None, items = None, **args):
		if data is None:
			data = {
				'lazy' : args.get('lazy', False)
			}
		if 'id' not in data:
			data['id'] = self.__type__
		
		super().__init__(data, items, **args)



class BoxText(Box):
	'''Box containing Text'''

class BoxLazy(Box):
	'''LazyBox Box class'''
	delay = 2000
	lazy_args = {}
	

class BoxFile(Box):
	'''Box that get contents from file.
	
	this is not a template file.
	use only in rare cases, as it do file.read on every request.
	'''
	
	file = None
	

@IN.register('BoxBase', type = 'Themer')
class BoxBaseThemer(In.themer.ObjectThemer):
	''''''

@IN.register('Box', type = 'Themer')
class BoxThemer(BoxBaseThemer):
	''''''
	
	#theme_tpl_type = 'tpl.py'

	#def theme(self, obj, format, view_mode, args):
		#pass

	#def theme_done(self, obj, format, view_mode, args):
		#pass

	#def theme_items(self, obj, format, view_mode, args):
		#pass

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		args['title'] = obj.title or ''


@IN.register('BoxFile', type = 'Themer')
class BoxFileThemer(BoxBaseThemer):

	def theme_plateit(self, obj, format, view_mode, args):

		with open(obj.file) as f:
			obj.theme_current_output['output']['final'] = f.read()


@IN.register('BoxLazy', type = 'Themer')
class BoxLazyThemer(BoxThemer):
	
	__invoke_theme_format_view_mode_alter__ = True
	
	def __theme_format_view_mode_alter__(self, format, view_mode, args):
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
			
	#def theme_plateit(self, obj, format, view_mode, args):
		#theme_output = obj.theme_current_output
		#if args['context'].request.ajax:
			## return fully themed output
			#args['children'] = theme_output['output']['children']
			#output = self.template_string.format_map(args)
		#else:
			## return ajax placeholder
			#obj.lazy_args['type'] = obj.__type__
			#json_args = json.dumps(obj.lazy_args, skipkeys = True, ensure_ascii = False)
			#tpl_args = {
				#'id' : obj.id,
				#'type' : obj.__type__,
				#'delay' : obj.delay,
				#'args' : json_args,
			#}
			#output = self.lazy_template_string.format_map(tpl_args)
		#theme_output['output']['final'] = output
