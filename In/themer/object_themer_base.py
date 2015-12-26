


class ObjectThemerBase:
	'''Theme Themer Base class.
	'''

	def pre_process_theme_args(self, obj, format, view_mode, args):
		'''This function will be called by the theme.themer method to prepare any custom args.
		'''

	def theme_process_variables(self, obj, format, view_mode, args):
		'''This function will be called by the theme.themer method to prepare any custom args.
		'''


	def theme_prepare(self, obj, format, view_mode, args):
		'''This function will be called by the themer method to prepare any custom properties.
		'''


	def theme(self, obj, format, view_mode, args):
		'''themer method is reponsible for theming IN Object Object. It should consider the format & view_mode arguments supplied to this function.

		By default it themers Object as self.html[prop] = { content : content, weight : 0 } if format is 'html'.
		You can initiate the buit-in templating process by calling <code>output = themer.theme(obj, **args)</code>. where args is the dict of all values to be availabe in the template context.
		'''


	def theme_items_pre(self, obj, format, view_mode, args):
		'''This function will be called by the themer method to prepare any custom properties.
		'''


	def theme_items(self, obj, format, view_mode, args):
		'''Called to themer the child items.
		'''

	def theme_done(self, obj, format, view_mode, args):
		'''Called when all the themering is done and final rendered output is available.
		'''

	def theme_value(self, obj, format, view_mode, args):
		return obj.def_value if obj.value is None else obj.value

	def theme_attributes(self, obj, format, view_mode, args):
		'''Called when themer wants lets object theme its attributes.
		'''
		return ''


