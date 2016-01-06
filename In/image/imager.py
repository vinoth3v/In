import os

import PIL

from PIL import Image, ImageOps

class InvalidImageStyleException(Exception):
	'''InvalidImageStyleException'''

class Imager:
	'''IN imager'''
	
	def __init__(self):
		
		self.config_style_filters = IN.APP.config.image_style_filters
		
		self.filters = {
			'resize' : self.resize,
			'resize_crop' : self.resize_crop			
		}
	
	def generate(self, file_path, style, save_to):
		'''Generate image with new styles'''
		
		# no exception handled
		
		filters = self.style_filters(style)
		
		# no filters to apply
		if not filters:
			# make symlink
			os.makedirs(os.path.dirname(save_to), exist_ok = True)
			os.symlink(file_path, save_to)
			
			return
		
		img = PIL.Image.open(file_path)
		
		for filter in filters:
			img = self.filters[filter[0]](img, filter[1])
		
		os.makedirs(os.path.dirname(save_to), exist_ok = True)
		img.save(save_to, optimize = True, quality = IN.APP.config.image_style_quality)
	
	def resize(self, img, args):
		size = args['size']
		over_scale = args.get('over_scale', True)
		if over_scale:
			return img.resize(size, Image.ANTIALIAS)
		else:
			img.thumbnail(size, Image.ANTIALIAS)
			return img
		
	
	def resize_crop(self, img, args):
		size = args['size']
		return ImageOps.fit(img, size, Image.ANTIALIAS)
		
	def style_filters(self, style):
		try:
			return self.config_style_filters[style]
		except KeyError as e:
			raise InvalidImageStyleException(s('Invalid image style {style}!', {'style' : style}))
	
@IN.hook
def In_app_init(app):
	IN.imager = Imager()
	
	
#@IN.hook
#def image_style_filters(style):
	
	


'''
size = (128, 128)
for infile in sys.argv[1:]:
	outfile = os.path.splitext(infile)[0] + ".thumbnail"
	if infile != outfile:
		try:
			im = Image.open(infile)
			im.thumbnail(size)
			im.save(outfile, "JPEG")
		except IOError:
			print("cannot create thumbnail for", infile)


with Image.open(infile) as im:
			print(infile, im.format, "%dx%d" % im.size, im.mode)


box = (100, 100, 400, 400)
region = im.crop(box)

region = region.transpose(Image.ROTATE_180)
im.paste(region, box)

out = im.resize((128, 128))
out = im.rotate(45)

out = im.transpose(Image.FLIP_LEFT_RIGHT)
out = im.transpose(Image.FLIP_TOP_BOTTOM)
out = im.transpose(Image.ROTATE_90)
out = im.transpose(Image.ROTATE_180)
out = im.transpose(Image.ROTATE_270)




fp = open("lena.ppm", "rb")
im = Image.open(fp)

im = Image.open(StringIO.StringIO(buffer))

from PIL import TarIO

fp = TarIO.TarIO("Imaging.tar", "Imaging/test/lena.ppm")
im = Image.open(fp)




def resize_and_crop(img_path, modified_path, size, crop_type='middle'):
	"""
	Resize and crop an image to fit the specified size.

	args:
		img_path: path for the image to resize.
		modified_path: path to store the modified image.
		size: `(width, height)` tuple.
		crop_type: can be 'top', 'middle' or 'bottom', depending on this
			value, the image will cropped getting the 'top/left', 'midle' or
			'bottom/rigth' of the image to fit the size.
	raises:
		Exception: if can not open the file in img_path of there is problems
			to save the image.
		ValueError: if an invalid `crop_type` is provided.
	"""
	# If height is higher we resize vertically, if not we resize horizontally
	img = Image.open(img_path)
	# Get current and desired ratio for the images
	img_ratio = img.size[0] / float(img.size[1])
	ratio = size[0] / float(size[1])
	#The image is scaled/cropped vertically or horizontally depending on the ratio
	if ratio > img_ratio:
		img = img.resize((size[0], size[0] * img.size[1] / img.size[0]),
				Image.ANTIALIAS)
		# Crop in the top, middle or bottom
		if crop_type == 'top':
			box = (0, 0, img.size[0], size[1])
		elif crop_type == 'middle':
			box = (0, (img.size[1] - size[1]) / 2, img.size[0], (img.size[1] + size[1]) / 2)
		elif crop_type == 'bottom':
			box = (0, img.size[1] - size[1], img.size[0], img.size[1])
		else :
			raise ValueError('ERROR: invalid value for crop_type')
		img = img.crop(box)
	elif ratio < img_ratio:
		img = img.resize((size[1] * img.size[0] / img.size[1], size[1]),
				Image.ANTIALIAS)
		# Crop in the top, middle or bottom
		if crop_type == 'top':
			box = (0, 0, size[0], img.size[1])
		elif crop_type == 'middle':
			box = ((img.size[0] - size[0]) / 2, 0, (img.size[0] + size[0]) / 2, img.size[1])
		elif crop_type == 'bottom':
			box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
		else :
			raise ValueError('ERROR: invalid value for crop_type')
		img = img.crop(box)
	else :
		img = img.resize((size[0], size[1]),
				Image.ANTIALIAS)
		# If the scale is the same, we do not need to crop
	img.save(modified_path)


'''
