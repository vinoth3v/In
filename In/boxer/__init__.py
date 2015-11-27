from In.boxer.box import *
from In.boxer.default_box import *


class BoxEngine:
	'''Boxer manages the boxes arround the pages.'''
	
	
	def boxes(self, context, page):
		'''return boxes by url, nabar, role, other conditions.'''
		return IN.hook_invoke('box', context, page)

	def decide_page_boxes(self, context, page, format):
		'''Add boxes to page'''
		
		boxes = IN.APP.decide_page_boxes(context, page, format)
		IN.hook_invoke('decide_page_boxes_alter', boxes, context, page, format)
		
		if boxes:
			for b in boxes:
				box = b[2]
				if type(box) is dict: # create instance from args
					box['id'] = b[0]
					
					if 'type' not in box:
						box['type'] = 'Box'
					box = Box.new(**box)
				if type(box) is str: # load this box
					box = self.load_box(box)
				page.add(box, panel = b[1])

	def load_box(self, key, args = None):
		
		objclass = IN.register.get_class(key, 'Box')
		if objclass is None:
			# use the default Box class
			objclass = Box
		
		if not issubclass(objclass, Box):
			return None
		
		if args is None:
			args = {}
		args['data'] = {'id' : key}
		# create Box instance
		box = objclass(**args)
		
		return box

	def process_lazy_box_request(self, context, lazy, **args):
		'''Process lazy_box_request

		'''
		obj = Object()

		for key, l in lazy.items():
			try:
				box = self.load_box(l['id'])
				obj.add(box)
			except Exception as e:
				IN.logger.debug()
		context.response = In.core.response.PartialResponse(output = obj)

#@IN.hook
#def __In_app_init__(app):
	### set the boxer
	#IN.boxer = BoxEngine()

@IN.hook
def box():
	return {
		'site_logo' : {												# box unique key

		},
		'site_promo' : {
			'box_class' : BoxFile,									# this class wil be initiated with the following args
			'arguments' : {
				'file' : 'files/public/boxes/site_promo.html',		# relative to app_path if not started with /
			},
			'default_panel' : 'promotion',
		},
	}
