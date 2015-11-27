
class TexterContainer(dict):

	def __missing__(self, key):
		vcls = IN.register.get_class(key, 'Texter')
		obj = vcls()
		self[key] = obj
		return obj

class TexterEngine:
	'''TexterEngine'''
	
	def __init__(self):
		
		self.texters = TexterContainer()
		self.texter_styles = IN.APP.config.texter
		self.html_parser = IN.APP.config.html_parser
		
	def format(self, text, style):
		output = text
		
		try:
			if style not in self.texter_styles:
				return ''
			style_texters = self.texter_styles[style]
			for texter_config in style_texters:
				try:
					
					texter = self.texters[texter_config[0]]
					# TODO: pass config
					config = texter_config[1] if len(texter_config) == 2 else {}
					
					output = texter.format(output, config)
				except:
					IN.logger.debug()
					
			return output
			
		except Exception as e:
			IN.logger.debug()
			# return empty if exception			
			return ''
		
