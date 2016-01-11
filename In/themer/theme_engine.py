import os
import json
import shutil
import re
import hashlib
import imp
import importlib

from collections import defaultdict, OrderedDict


class INThemeEngine:
	'''IN Core Theme Engine'''

	
	__default_format__ = 'html'
	__template_handlers__ = {}
	__themes__ = {}

	default_theme_name = 'In.themes.ilai'

	# all template paths ordered by weight
	# light weight is most effective here
	__template_paths__ = {}

	__cache_tpl_file___ = {}
	__cache_tpl_file_content___ = {}
	__cache_object_dynamic_theme_function__ = {}
	__cache_string_dynamic_theme_function__ = {}

	TOKEN_TEXT      = 0
	TOKEN_VAR       = 1
	TOKEN_PY        = 2
	TOKEN_COMMENT   = 3
	TOKEN_PY_CLOSE  = 5
	TOKEN_PY_OPEN   = 4
	TOKEN_TEXT_NL   = 6
	TOKEN_TEXT_TAB  = 7
	TOKEN_TEXT_WS   = 8
	TOKEN_PY_INLINE = 9
	TOKEN_PY_INLINE_STR = 10
	TOKEN_BRACE_OPEN = 11
	TOKEN_BRACE_END = 12
	TOKEN_PY_INLINE_S = 11
	
	token_tags = (
		('<?py '	, '?>'      , '%s.*?%s', TOKEN_PY),
		('<py>'		, '</py>'   , '%s.*?%s', TOKEN_PY),
		('<py '		, '/>'      , '%s.*?%s', TOKEN_PY),
		('<% '		, '%>'      , '%s.*?%s', TOKEN_PY),
		('<% '		, '/>'      , '%s.*?%s', TOKEN_PY),
		('<py '		, '>'       , '%s.*?%s', TOKEN_PY_OPEN),
		('<% '		, '>'       , '%s.*?%s', TOKEN_PY_OPEN),
		('</py>'	, '' 	    , '%s.*?%s', TOKEN_PY_CLOSE),
		('</%>'		, ''        , '%s.*?%s', TOKEN_PY_CLOSE),
		('<%= '		, '%>'      , '%s.*?%s', TOKEN_PY_INLINE),
		('<%str= '	, '%>'      , '%s.*?%s', TOKEN_PY_INLINE_STR),
		('<%s= '	, '%>'      , '%s.*?%s', TOKEN_PY_INLINE_S),
		('<%= '		, '%/>'     , '%s.*?%s', TOKEN_PY_INLINE),
		('{{'		, ''		, '%s.*?%s', TOKEN_BRACE_OPEN),	# {{  is escape
		('}}'		, ''		, '%s.*?%s', TOKEN_BRACE_END),	# }}  is escape
		('{'		, '}'		, '%s.*?%s', TOKEN_PY_INLINE),
		#('{[^\{]'	, '}[^\}]'	, '%s.*?%s', TOKEN_PY_INLINE),		# {{  is escape
	)

	estags = ()
	stags = ''

	for st, et, ts, tt in token_tags:
		estags += re.escape(st), re.escape(et)
		if stags:
			stags = '|'.join((stags, ts))
		else:
			stags = ts
	stags = ''.join(('(', stags, ')'))

	tag_regex = re.compile(stags % estags)

	
	def __init__(self, default_theme_name):

		self.load_theme(default_theme_name, True)


	def theme(self, obj, format = 'html', view_mode = 'default', args = None):
		'''Theme themer main function.

		'''
		
		if not obj or not obj.visible:
			return ''
		
		if args is None:
			args = {}

		args['__theme_engine__'] = self
		
		if 'context' not in args:
			args['context'] = IN.context
		
		#if isinstance(obj, Object):
		
		obj_themer = obj.Themer
		
		# some themer may change view_mode
		if obj_themer.__invoke_theme_format_view_mode_alter__:
			format, view_mode = obj_themer.__theme_format_view_mode_alter__(format, view_mode, args)
		
		# static theme output cache
		theme_cacher = obj.ThemeCacher
		
		if theme_cacher.theme_cache_enabled:
			cached_result = theme_cacher.get(obj, format, view_mode, args)
			
			if cached_result:
				cached_result = theme_cacher.process_cached_output(obj, cached_result, format, view_mode, args)
				return cached_result
		
		# TODO: it always raise error first time for all objects
		#try:
			#if obj.theme_output is not None:
				#return obj.theme_current_output['output']['final']
		#except Exception as e:
			#pass

		# always use object themer suggested tpl type
		

		#tpl_type = obj_themer.theme_tpl_type

		#handler_obj = self.template_handler(tpl_type)

		##print('handler_class ', handler.__name__, tpl_type)

		#if handler_obj is None:

			#raise In.themer.ThemeException('Unable to find the appropriate handler for the template type \'' + tpl_type + '\'.')

		args['__tpl_item_type__'] = obj.__class__

		#theme hooks

		prefix = '_'.join(('theme_object', obj.__type__))
		invoke_hook = obj_themer.__invoke_theme_hook__
		hook_invoke = IN.hook_invoke

		# create theme_output variables
		self.theme_object_prepare(obj, format, view_mode, args)
		
		cache_already_set = False
		
		if not obj.theme_current_output['themed']: # already themed
			
			if invoke_hook:
				
				obj_themer.theme_prepare(obj, format, view_mode, args)
				hook_invoke('_'.join((prefix, 'prepare')), obj, format, view_mode, args)

				hook_invoke('_'.join((prefix, 'pre')), obj, format, view_mode, args)
				
				obj_themer.theme(obj, format, view_mode, args)
				hook_invoke(prefix, obj, format, view_mode, args)
				
				# after theme call object may set it invisible depends on empty values
				if not obj.visible:
					return ''
				
				obj_themer.theme_items(obj, format, view_mode, args)
				hook_invoke('_'.join((prefix, 'theme_items')), obj, format, view_mode, args)
					
				obj_themer.theme_attributes(obj, format, view_mode, args)
				hook_invoke('_'.join((prefix, 'theme_attributes')), obj, format, view_mode, args)
				
				
				obj_themer.theme_process_variables(obj, format, view_mode, args)
				hook_invoke('_'.join((prefix, 'theme_process_variables')), obj, format, view_mode, args)
				
				self.theme_object_plateit(obj, format, view_mode, args)
				
				
				#callback for the final touch
				obj_themer.theme_done(obj, format, view_mode, args)
				hook_invoke('_'.join((prefix, 'theme_done')), obj, format, view_mode, args)
				
			else:
				
				obj_themer.theme_prepare(obj, format, view_mode, args)
				
				obj_themer.theme(obj, format, view_mode, args)
				
				# after theme call object may set it invisible depends on empty values
				if not obj.visible:
					return ''
				
				obj_themer.theme_items(obj, format, view_mode, args)
					
				obj_themer.theme_attributes(obj, format, view_mode, args)
				
				obj_themer.theme_process_variables(obj, format, view_mode, args)
				
				self.theme_object_plateit(obj, format, view_mode, args)
				
				#callback for the final touch
				obj_themer.theme_done(obj, format, view_mode, args)
				
			# theme completed
			obj.theme_current_output['themed'] = True
			
		else:
			cache_already_set = True
			
		try:
			theme_output = obj.theme_current_output['output']['final']
		except KeyError as e:
			IN.logger.debug()
			theme_output = ''
		
		# theme cache set
		if theme_output and theme_cacher.theme_cache_enabled and not cache_already_set:
			try:
				theme_cacher.set(obj, theme_output, format, view_mode, args)
			except Exception as e:
				IN.logger.debug()
		
		try:
			del args['__tpl_item_type__']
		except KeyError as e:
			pass

		return theme_output

		#else:
			#print(obj, args )
##        else:
##
##            if isinstance(obj, Object):
##
##                #resursive through parent items
##
##                if not '__tpl_search_parent__' in args:
##                    args['__tpl_search_parent__'] = True
##
##                args['__tpl_item_type__'] = obj.__class__
##
##                for handler_class in __template_handlers__:
##
##                    try:
##                        #print('handler_class ', handler_class.__name__)
##
##                        handler_obj = handler_class()
##                        args['tpl_type'] = handler_obj.tpl_type
##
##                        with IN.output_catcher() as output:
##                            pass
##                        ret = handler_obj.theme(obj, args)
##
##                        result = output.output()
##
##                        if ret is not None:
##                            result += str(ret)
##                        #print(result)
##
##
##                    except ThemeException as e:
##                        print(e)
##                        continue
##
##                if '__tpl_search_parent__' in args: del args['__tpl_search_parent__']
##                if '__tpl_item_type__' in args: del args['__tpl_item_type__']
##
##                return result


		#print('BREAK FOR NOW, Themer is only theme Object objects, for now.', 'got', obj.__class__.__name__)
		return obj

		# TODO :
##        for handler_class in __template_handlers__:
##
##            try:
##                handler_obj = handler_class()
##                with IN.output_cacher() as output:
##                    res = handler_obj.theme(obj, args)
##                if res is not None:
##                    return str(res) + output.output()
##                return output.output()
##
##            except ThemeException as e:
##                #print(e)
##                continue

		#print('NOT HANDLED theme type : ' + type(obj).__name__)

		#if no handler use the default
		tobj = Template_Py()
		args['__use_default_handler__'] = True

		return tobj.theme(obj, rgs)


	##    if isinstance(obj, str): #may have a function to themer.
	##        return theme_py(obj, args)
	##
	##    if isinstance(obj, Object):#IN Object Themer logic
	##        return theme_object(obj, args)
	##


	def get_theme(self):
		return IN.context.current_theme or self.default_theme

	@property
	def default_format(self):
		return self.__default_format__

	def load_theme(self, theme_name, set_default = False):

		if theme_name in self.__themes__:
			return self.__themes__[theme_name]

		theme_module = importlib.import_module(theme_name)

		if set_default:
			self.default_theme = theme_module
			self.default_theme_name = theme_module.__name__

		#if not hasattr(theme_module, '__version__'):
			#theme_module.__version__ = IN.__version__

		IN.hook_invoke('theme_load_theme', theme_name, theme_module)

		self.__themes__[theme_name] = theme_module

		
		self.build_template_paths(theme_name)
		
		return theme_module

	def theme_def_path(self, format = __default_format__):
		if not format:
			return ''

		def_path = ''.join((IN.root_path, os.sep, 'templates', os.sep, format, os.sep ))
		path = def_path
		if not os.path.exists(path):
			parent = self.parent_format(format)
			if not parent:
				#print('Templates not found for ' + format + ' format or access denied!. ' + format + ' templates should be in ' + def_path)
				pass
			else:
				path = self.theme_def_path(parent)
		return path

	def theme_path(self):
		theme = self.get_theme()
		return theme.__path__[0]

	def def_panels(self):
		return [
			'header_top', 'header', 'header_bottom',
			'side_1', 'side_2', 'side_3', 'side_4',
			'content_top', 'content_header', 'content', 'content_bottom',
			'footer_top', 'footer', 'footer_bottom',
		]

	def panels(self):
		theme = self.get_theme()
		if theme:
			return theme.panels
		return self.def_panels()

	def theme_attributes(self, arbs = None):
		output = ''
		if not arbs:
			return output
		#if len(arbs) == 1:
			#for k, v in arbs.items():
				#return k if v is None else ''.join((k, '="', str(v), '"'))

		#attrlist = []
		#for k, v in arbs.items():
			##if v is None:
				##attrlist.append(k)
			##else:
			#attrlist.append(k if v is None else ''.join((k, '="', str(v), '"')))

		output = ' '.join(k if v is None else ''.join((k, "='", str(v), "'")) for k, v in arbs.items())

		return output

	@staticmethod
	def parent_format(format):
		'''Helper function to get the parent format name.

		'''

		if format == 'TEXT':
			# return empty...
			return '' #text is final

		this_class = IN.register.get_class(format, 'theme_format')
		if not this_class:
			raise In.themer.ThemeException(s('Theme: Unknown theme format : {name}.', {'name' : format}))

		parent_class = this_class.__bases__[0]

		#TODO: need fix, parent class name may be different from registered theme format
		parent_format = parent_class.__type_alias__ or parent_class.__name__

		return parent_format


	def theme_object_prepare(self, obj, format, view_mode, args):

		#try:
			#if obj.__theme_prepared__: return
		#except AttributeError as e:
			#pass

		if obj.theme_output is None or args.get('retheme', False):
			obj.theme_output = {
				format : {
					view_mode : {
						'themed': False, 		# not themed yet
						'content' : {			# USED BY Templates, theme functions
							'children' : OrderedDict(),	# keep order
						},
						'output' : {
							'children' : '', 			# optional children merged output
							'final_output'	: '', 		# final output
						}
					}
				}
			}
			
			obj.theme_current_output = obj.theme_output[format][view_mode]
			
			return
		
		obj_theme_output_format = obj.theme_output[format]
		
		if view_mode not in obj_theme_output_format:
			obj_theme_output_format[view_mode] = {
				'themed': False, 		# not themed yet
				'content' : {			# USED BY Templates, theme functions
					'children' : OrderedDict(),	# keep order
				},
				'output' : {
					'children' : '', 			# optional children merged output
					'final_output'	: '', 		# final output
				}
			}
		
		# short cut attribute, we can use this if we dont know which format which view_mode
		obj.theme_current_output = obj_theme_output_format[view_mode]

		#'''
		#obj.theme_output = {
			#format : {
				#view_mode : {
					#'themed': False, 		# not themed yet
					#'content' : {			# USED BY Templates, theme functions
						#'children' : {},	# output of childred keyed by child id
						#'other variables' : {},
					#},
					#'output' : {
						#'children' : '', 			# optional children merged output
						#'final'	: '', 		# final output
					#}
				#}
			#}
		#}
		#'''

		#print('Themer....... ', obj, obj.Themer)

	def build_template_paths(self, theme_name):
		'''
		per theme basis

		theme:
			base path:
				format:
					obj-viewmode.tpl.py
					obj.tpl.py

		'''
		
		theme = self.__themes__[theme_name]

		cur_theme_path = ''.join((theme.__path__[0], os.sep, 'templates'))

		self.__template_paths__[theme_name] = defaultdict(dict)
		_theme = self.__template_paths__[theme_name]

		formats = []
		for register_for, register_for_dict in IN.register.registered_classes_sorted.items():
			for register_as, register_as_list in register_for_dict.items():
				if register_as == 'theme_format' and register_as_list:
					formats.append(register_for)
		
		# collect theme tpls
		
		self.__collect_templates__(cur_theme_path, formats, _theme)
		
		# colect other tpls
		paths = []
		
		hook_paths = IN.hook_invoke('template_path')
		for _paths in hook_paths:
			paths.extend(_paths)

		# sort by weight
		paths = sorted(paths, key = lambda obj: obj['weight'])
		
		for path in paths:
			self.__collect_templates__(path['path'], formats, _theme)

		
	def __collect_templates__(self, base, formats, saveto, theme_ext = '.tpl.py'):
		
		for format in formats:
			_format = saveto[format]
			dir = os.path.join(base, format)
			
			for root, dirs, files in os.walk(dir):
				
				for file in files:
					if file.endswith(theme_ext):
						name = file.replace(theme_ext, '')
						if name not in _format:
							_format[name] = []
						_obj = _format[name]
						_obj.append(os.path.join(root, file))
						
				break # one level only

	def get_object_template(self, obj, theme_name, format, view_mode, tpl_item_class = None):

		if tpl_item_class is None:
			obj_type = str(obj.__type__)
			iclass = obj.__class__
		else:
			obj_type = tpl_item_class.__name__
			iclass = tpl_item_class

		cache_key = '-'.join((theme_name, obj_type, format, view_mode))

		try:
			file = self.__cache_tpl_file___[cache_key]
			return file
		except KeyError:
			#IN.logger.debug() not needed
			pass

		search_keys = ['-'.join((obj_type, view_mode)), obj_type]

		__tpls__ = self.__template_paths__[theme_name][format]
		
		for key in search_keys:
			try:
				file = __tpls__[key][0]
				self.__cache_tpl_file___[cache_key] = file
				return file
			except KeyError:
				#IN.logger.debug() # not needed
				pass

		# not found, goto parent obj
		if obj_type != 'Object': # fix endless loop

			for cls in reversed(iclass.__bases__):
				if issubclass(cls, Object) or cls is Object:
					tpl_item_class = cls
					file = self.get_object_template(obj, theme_name, format, view_mode, tpl_item_class)

					if file:
						self.__cache_tpl_file___[cache_key] = file
						return file

		raise In.themer.TemplateNotFound(s('Template File for {type} not found! format : {format}, view_mode : {view_mode}', {'type': obj_type, 'format' : format, 'view_mode' : view_mode}))
		
		
	#def __get_object_template__(self, obj, format, view_mode, theme_name, tpl_item_class = None):

		#if tpl_item_class is None:
			#obj_type = str(obj.__type__)
			#iclass = obj.__class__
		#else:
			#obj_type = tpl_item_class.__name__
			#iclass = tpl_item_class

		#search_keys = ['-'.join((obj_type, view_mode)), obj_type]

		#__tpls__ = self.__template_paths__[theme_name][format]
		
		#for key in search_keys:
			#try:
				#return __tpls__[key][0]
			#except:
				#pass

		## not found, goto parent obj
		#if obj_type != 'Object': # fix endless loop

			#for cls in reversed(iclass.__bases__):
				#if issubclass(cls, Object) or cls is Object:
					#tpl_item_class = cls
					#f = self.get_object_template(obj, format, view_mode, tpl_item_class)

					#if f:
						#return f
		

	def theme_object_plateit(self, obj, format, view_mode, args):
		
		if not obj.visible:
			return
		
		theme_output = obj.theme_current_output

		context = args['context']
		
		tpl = ''

		#tpl_type = args.get('tpl_type', self.tpl_type)

		cache_key = '-'.join((obj.__type__, format, view_mode));

		try:
			output = self.__cache_object_dynamic_theme_function__[cache_key](args)
			obj.theme_current_output['output']['final'] = output
			return
		except KeyError:
			IN.logger.debug() # not needed
			pass

		try:

			tpl_item_class = args.get('__tpl_item_type__', None)

			theme_name = context.current_theme.__name__
		
			file = self.get_object_template(obj, theme_name, format, view_mode)
			
			#print('TPL file ', obj.__type__, view_mode, file)

		except In.themer.TemplateNotFound as e:
			#print(e)
			raise e

		tpl_content = None
		
		try:
			# use cached tpl content
			tpl_content = self.__cache_tpl_file_content___[file]
		except Exception:
			with open(file, 'r') as f:
				tpl_content = f.read()
			
		if tpl_content is None:

			# raise error
			raise ThemeException(s('Unable to get the template content for {type}! format : {format}, view_mode : {view_mode}', {'type': obj_type, 'format' : format, 'view_mode' : view_mode}))

		# cache
		self.__cache_tpl_file_content___[file] = tpl_content

		# compile the template string
		function = self.__compile__(tpl_content)

		# cache it
		self.__cache_object_dynamic_theme_function__[cache_key] = function

		args['obj'] = obj
		
		output = function(args)

		obj.theme_current_output['output']['final'] = output

	def __compile__(self, string):
		'''Compile the string into py function and return it'''
		
		pycode = [self.content_to_tokens(b) for b in filter(None, self.tag_regex.split(string))]
		pycode = self.__token_to_py_function__(pycode)
		
		md5 = hashlib.md5(pycode.encode('utf-8')).hexdigest()
		
		name = 'py_' + str(md5)
		
		path = ''.join((IN.APP.config.tmp_file_dir, '/tpl.py/', name, '.py'))
		
		if not os.path.exists(path):
			with open(path, 'w') as file:
				file.write(pycode)

		mod = imp.load_source(name, path)
		
		return mod.theme


	def __token_to_py_function__(self, tokens):
		pycode = ['''
		
def theme(_):
	
	_o_ = []
	write = _o_.append
	debug = IN.logger.debug
		
''']
		indent = 1
		for t in tokens:

			if t['token'] == self.TOKEN_TEXT:
				content = t['contents'].replace('"','\\"').replace("'","\\'")
				pycode.append(''.join(('\n',  '\t' * indent, '''write("""''', content, '""")')))
			elif t['token'] == self.TOKEN_BRACE_OPEN:
				content = '{'
				pycode.append(''.join(('\n\t' * indent, '''write("""''', content, '""")')))
			elif t['token'] == self.TOKEN_BRACE_END:
				content = '}'
				pycode.append(''.join(('\n\t' * indent, '''write("""''', content, '""")')))
			elif t['token'] == self.TOKEN_PY_INLINE:
				pycode.append(''.join(('\n',  '\t' * indent, '''try:''')))
				pycode.append(''.join(('\n',  '\t' * (indent+1), '''write(_["''', t['contents'].strip(), '''"])''')))
				pycode.append(''.join(('\n',  '\t' * indent, '''except:''')))
				pycode.append(''.join(('\n',  '\t' * (indent+1), '''pass''')))
				#pycode.append(''.join(('\n',  '\t' * (indent+1), '''pprint(_)''')))
				#pycode.append(''.join(('\n',  '\t' * (indent+1), '''debug()\n''')))
			elif t['token'] == self.TOKEN_PY_INLINE_STR:
				pycode.append(''.join(('\n',  '\t' * indent, '''try:''')))
				pycode.append(''.join(('\n',  '\t' * (indent+1), '''write(str(_["''', t['contents'].strip(), '''"]))''')))
				pycode.append(''.join(('\n',  '\t' * indent, '''except:''')))
				pycode.append(''.join(('\n',  '\t' * (indent+1), '''pass''')))
				#pycode.append(''.join(('\n',  '\t' * (indent+1), '''pprint(_)''')))
				#pycode.append(''.join(('\n',  '\t' * (indent+1), '''debug()\n''')))
			elif t['token'] == self.TOKEN_PY_INLINE_S:
				pycode.append(''.join(('\n',  '\t' * indent, '''try:''')))
				pycode.append(''.join(('\n',  '\t' * (indent+1), '''write(s(_["''', t['contents'].strip(), '''"]))''')))
				pycode.append(''.join(('\n',  '\t' * indent, '''except:''')))
				pycode.append(''.join(('\n',  '\t' * (indent+1), '''pass''')))
				#pycode.append(''.join(('\n',  '\t' * (indent+1), '''pprint(_)''')))
				#pycode.append(''.join(('\n',  '\t' * (indent+1), '''debug()\n''')))
			elif t['token'] == self.TOKEN_PY:
				pycode.append(''.join(('\n',  '\t' * indent, t['contents'], '\n')))
			elif t['token'] == self.TOKEN_PY_OPEN:
				pycode.append(''.join(('\n', '\t' * indent, t['contents'], '\n')))
				indent += 1
			elif t['token'] == self.TOKEN_PY_CLOSE:
				pycode.append(''.join(('\n', '\t' * indent, t['contents'], '\n')))
				indent -= 1
			elif t['token'] == self.TOKEN_TEXT_NL:
				pycode.append(''.join(('''write("""''', t['contents'], '""")')))
			elif t['token'] == self.TOKEN_TEXT_TAB:
				pycode.append(''.join(('''write("""''', t['contents'], '""")')))
			elif t['token'] == self.TOKEN_TEXT_WS:
				pycode.append(''.join(('''write("""''', t['contents'], '""")')))
				
		pycode.append(''.join(('\n', '\t' * indent, '''return "".join(_o_)''', '\n')))
		pycode = ''.join(pycode)
		return pycode


	def content_to_tokens(self, contents):
		for st, et, ts, tt in self.token_tags:
			if contents.startswith(st) and contents.endswith(et):
				return {'token' : tt,
						'contents' : contents[len(st):-len(et)],
						'st' : st,
						'et' : et,
						}
		return {'token' : self.TOKEN_TEXT, 'contents' : contents}
		
	def string_format(self, string, args):
		
		try:
			return self.__cache_string_dynamic_theme_function__[string](args)
		except:
			
			function = self.__compile__(string)

			# cache it
			self.__cache_string_dynamic_theme_function__[string] = function

			return function(args)

		
