import traceback

from In.themer.object_themer_base import *


# Themer class for Object class

@IN.register('Object', type = 'Themer')
class ObjectThemer(ObjectThemerBase):

	
	sort_children = True #False #
	merge_children = True
	
	#default_children_view_mode = None
	
	# invokes the theme hooks per object theme functions
	__invoke_theme_hook__ = False
	__invoke_theme_format_view_mode_alter__ = False

	def __init__(self, objcls, key, mem_type):
		''''''
		
		# we need this __init__
		# dont remove


		
	def theme(self, obj, format, view_mode, args):
		'''themer method is reponsible for themering IN 'Object' Object.

		It should consider the format & view_mode arguments supplied to this function.
		By default it theme Object as self.theme_output[html][prop] = { content : content, weight : 0 } if format is 'html'.
		You can initiate the buit-in templating process by calling
		<code>
		output = IN.themer.theme(self, **args)
		</code>
		where args is the dict of all values to be availabe in the template context.
		'''
		#print(obj.type, 'Themer', obj.Themer)

		#context = args['context']

		theme_output = obj.theme_current_output

		theme_output['content']['value'] = self.theme_value(obj, format, view_mode, args)
		
		## theme cache tokens
		
		#tokens = theme_output['output']['tokens']
		
		#obj_type = obj.__type__
		
		#if obj_type not in tokens:
			#tokens[obj_type] = []
		
		#tokens_obj_type = tokens[obj_type]
		#tokens_obj_type.append(obj.id)
		

	def theme_done(self, obj, format, view_mode, args):

		#wrap the rendered output
		wrapper = obj.item_wrapper
		
		if not wrapper:
			return
			
		if type(wrapper) is str:
			
			typ = IN.register.get_class(obj.item_wrapper, 'Object')
			if typ:
				wrapper = Object.new(wrapper, {})
			else:
				return
		
		output = obj.theme_current_output['output']['final']
		
		wrapper.value = output
		
		themer = args['__theme_engine__']
		
		output = themer.theme(wrapper, format, view_mode)

		obj.theme_current_output['output']['final'] = output

	def theme_items(self, obj, format, view_mode, args):
		'''themers all of its childern.'''

		if not obj: # emtpy
			return

		theme_output = obj.theme_current_output

		children = theme_output['content']['children']

		_theme = IN.themer.theme
		
		if self.sort_children:
			si = sorted(obj.values(), key = lambda obj: obj.weight) # int
		else:
			si = obj.values()
		
		sub_view_mode = obj.default_children_view_mode or view_mode
		context = args['context']
		
		for child in si: #obj.items():
			try:
				#idx += 1
				#weight = child.weight #or idx
				
				#subargs = {
					#'context' : context,
					##'item_index' : weight,
				#}
				
				#child_theme_output = _theme(child, format, sub_view_mode, subargs)

				children[child.id] = {
					'content' : _theme(child, format, sub_view_mode, {
						'context' : context
					}),
					'weight' : child.weight, # keep order
				}
				
			except Exception as e:
				IN.logger.debug()
		
		# use yield
		#children.update(self._theme_child(obj, args))

		c = ''

		if self.merge_children:
			cs = ' '
			if obj.child_separator:
				cs = obj.child_separator

			c = cs.join( v['content'] for v in children.values())

		
		theme_output['output']['children'] = c
		

##    def __getitem__(self, key):
##        return self.items.get(key)

##    def __setitem__(self, key, v):
##        if isinstance(other, Object):
##            self.items[key] = v

##    def __len__(self):
##        if self.items:
##            return len(self.items)
##        return len(self.getval())
##

##    def __add__(self, other):
##        self.add(**arg)


	def theme_attributes(self, obj, format, view_mode, args):

		theme_output = obj.theme_current_output
		themer = args['__theme_engine__']

		attrbs = obj.get_attributes()

		css = self.theme_css(obj)
		
		if css:
			attrbs['class'] = css

		theme_attrbs = themer.theme_attributes(attrbs)

		theme_output['content']['attributes'] = theme_attrbs


	def theme_css(self, obj):

		if not obj.css:
			return ''
		
		return ' '.join(obj.css)

	def theme_process_variables(self, obj, format, view_mode, args):

		theme_output = obj.theme_current_output['content']

		# make all content variables available to templates
		
		args.update(theme_output)
		
		theme_output = obj.theme_current_output
		
		children = theme_output['content']['children']
		for obj_id, obj_content in children.items():
			args[obj_id] = obj_content['content']
			
		if self.merge_children:
			
			# use merged version of children
			args['children'] = obj.theme_current_output['output']['children']
		
		args['id'] = obj.id
		
		config = IN.APP.config
		
		cdn = config.cdn
		
		args['cdn_img'] = cdn['img']
		args['cdn_css'] = cdn['css']
		args['cdn_js'] = cdn['js']
		
		args['asset_version'] = config.asset_version
		
		args['files_path'] = config.pfpp
		
		args['files_path_version'] = '/'.join((config.pfpp, config.asset_version))
		
	def theme_plateit(self, obj, format, view_mode, args):

		theme_output = obj.theme_current_output

		# use merged version of children
		args['children'] = theme_output['output']['children']

		#output = self.__template__.safe_substitute(args)
		output = self.template_string.format_map(args)
		#output = self.template_string % args

		# set the final output
		theme_output['output']['final'] = output

	def __theme_format_view_mode_alter__(self, format, view_mode, args):
		'''Themer will call this with existing args

		if we need, depends on some arguments, we can change it and return
		'''
		return format, view_mode

	def view_modes(self):
		return {'default'}
		
@IN.register('Text', type = 'Themer')
class TextThemer(ObjectThemer):

	pass
	
@IN.register('LogMessage', type = 'Themer')
class LogThemer(ObjectThemer):

	def theme(self, obj, format, view_mode, args):
		'''themer the exc_info as value if exists'''

		super().theme(obj, format, view_mode, args)

		if obj.exc_info:

			itm_format = obj.theme_current_output
			tb = traceback.format_exception(*obj.exc_info)
			itm_format['content']['content'] = ''.join(tb)

##    def theme_process_variables(self, args, kargs):
##        Object.theme_process_variables(self, args, kargs)
##
##        format = kargs.get('format', 'html')
##        theme_output = self.theme_output[format]
##
##        print(theme_output)



@IN.register('ThemeArgs', type = 'Themer')
class ThemeArgsThemer(ObjectThemer):

	def theme(self, obj, format, view_mode, args):
		pass

	def theme_done(self, obj, format, view_mode, args):
		pass

	def theme_items(self, obj, format, view_mode, args):
		'''themers all of its childern.

		Theme args object needs to theme children in different view_mode
		'''

		if not obj: # emtpy
			return

##        itms = sorted(self.values(), key=p)
##        itms.sort(Object.__pos_cmp__)

		#context = args['context']

		theme_output = obj.theme_current_output

		children = theme_output['content']['children']

		#idx = 0

		_theme = IN.themer.theme
		#for i in obj.values():
			#if i.weight is None:
				#print('222222222222222222222', i.__type__, i.id)
				
		if self.sort_children:
			si = sorted(obj.values(), key = lambda obj: obj.weight)
		else:
			si = obj.values()
		
		for child in si: #obj.items():
			try:
				#idx += 1
				weight = child.weight #or idx
				
				subargs = {
					'context'	: args['context'],
					'item_index' : weight,
				}
				
				subargs.update(obj.args)
				
				sub_view_mode = subargs.get('view_mode', view_mode)
				sub_format = subargs.get('format', format)
				
				# theme the children in specific view_mode
				child_theme_output = _theme(child, sub_format, sub_view_mode, subargs)

				children[child.id] = { 
					'content' : child_theme_output,
					'weight' : weight, # keep order
				}
				
			except Exception as e:
				IN.logger.debug()
		
		c = ''

		if self.merge_children:
			cs = ' '
			if obj.child_separator:
				cs = obj.child_separator

			c = cs.join( v['content'] for v in children.values())


		theme_output['output']['children'] = c

builtins.ObjectThemer = ObjectThemer

