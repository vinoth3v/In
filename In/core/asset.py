from collections import OrderedDict


class Asset:

	def __init__(self, **args):

		self.css = args.get('css', {})
		self.js = args.get('js', {})

	def add_js(self, js, key, type = 'file', group = 'header', weight = 0):
		try:
			container = self.js[group]
		except KeyError:
			self.js[group] = OrderedDict() # keep order
			container = self.js[group]

		container[key] = {'js' : js, 'weight' : weight, 'type' : type}

	def add_css(self, css, key, type = 'file', group = 'header', media = 'all', weight = 0):
		'''Add css to assets.

		css: string. path or inline css
		key: to indentiy the added css
		type: file | inline
		group: header | footer | custom
		media : media type for this css
		'''
		try:
			container = self.css[group]
		except KeyError:
			self.css[group] = OrderedDict() # keep order
			container = self.css[group]

		container[key] = {'css' : css, 'weight' : weight, 'type' : type, 'media' : media}

	def theme_css(self, group = 'header'):
		try:
			container = self.css[group]
		except KeyError:
			return ''

		# group by group, media, type
		out = []
		
		cdn = IN.APP.config.cdn.get('css', '')
		version = IN.APP.config.asset_version
		
		for key, css in container.items():
			if css['type'] == 'file':
				out.append(''.join(('<link type="text/css" rel="stylesheet" href="//', cdn, css['css'], '" media="', css['media'], '" />')))
			elif css['type'] == 'inline':
				if css['media'] == 'all':
					out.append(css['css'].join(('<style type="text/css" >\n<!--\n', '\n//-->\n</style>')))
				else:
					out.append(''.join(('<style type="text/css" >\n<!--\n@media(', css['media'], '){', css['css'], '}\n//-->\n</style>')))

		return '\n'.join(out)

	def theme_js(self, group = 'header'):
		try:
			container = self.js[group]
		except KeyError:
			return ''

		# group by group, type
		out = []
		
		cdn = IN.APP.config.cdn.get('js', '')
		version = IN.APP.config.asset_version
		
		for key, js in container.items():
			if js['type'] == 'file':
				out.append(''.join(('<script type="text/javascript" src="//', cdn, js['js'], '"></script>')))
			elif js['type'] == 'inline':
				out.append(''.join(('<script type="text/javascript" >\n<!--\n', js['js'], '\n//-->\n</script>')))

		return '\n'.join(out)

		
