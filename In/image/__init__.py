import os
from .imager import *
from .field_image import *
from .entity_bundle_file_image import *
from .field_image_field_formatter import *

from .admin import *

@IN.hook
def file_generator(ext, path, base_path, path_type):
	
	if not (path_type == 'public' or path_type == 'private'): # for now, public,private only
		return
		
	if not path.startswith('style'):
		return
	
	style = path.split('/')[1]
	
	nostyle_path = path.replace(style.join(('style/', '/')), '', 1)
	nostyle_full_path = os.path.join(base_path, nostyle_path)
	full_path = os.path.join(base_path, path)
	
	
	# generate the image
	try:
		# TODO: token, dir to allowed styles mapping
		
		IN.imager.generate(nostyle_full_path, style, full_path)
		
		# return generated image path
		return full_path
	except Exception as e:
		IN.logger.debug()
		

'''

[[{
	"fid":"30231",
	"view_mode":"default",
	"fields":{
		"format":"default",
		"field_file_image_alt_text[und][0][value]":"Tamil Script",
		"field_file_image_title_text[und][0][value]":""},
		"type":"media",
		"attributes":{
			"alt":"Tamil Script",
			"class":"media-element file-default"
		}
	}
]]

[[#include args = {
	"type" : 'File',
	"id" : "30231",
	"view_mode" : "default",
	"data" : {},
}]]

'''
