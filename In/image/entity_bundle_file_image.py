
#TODO: same name as entity type File
# fix: themer register
@IN.register('File', type = 'image')
class FileImage(File):
	'''FileImage bundle class.
	'''


@IN.register('FileImage', type = 'Themer')
class FileImageThemer(In.file.FileThemer):
	'''File themer'''
	
	def view_modes(self):
		modes = super.view_modes()
		modes.add('image')
		return modes
		
	def theme(self, obj, format, view_mode, args):
		
		theme_output = obj.theme_current_output
		
		path = obj.path
		
		config = IN.APP.config
		cdn = config.cdn.get('img', '')
		
		if not view_mode in config.image_style_filters:
			view_mode = 'default'
		
		if obj.private:
			path = ''.join(('//', cdn, '/files/private/style/', view_mode, '/', obj.path))
		else:
			path = ''.join(('//', cdn, '/files/public/style/', view_mode, '/', obj.path))
	
		# TODO: HACK
		path = path.join(('<img src="', '" />'))
		
		theme_output['content']['value'] = path
		
	#def theme_process_variables(self, field, format, view_mode, args):
		#super().theme_process_variables(field, format, view_mode, args)

		
		#args['title'] = field.title #field_config['title']
		

	#def theme_plateit(self, field, format, view_mode, args):
		#if args is None:
			#args = {}

		##output = self.__template__.safe_substitute(args)
		#output = self.template_string.format_map(args)
		##output = self.template_string % args

		#field.theme_current_output['output']['final'] = output
