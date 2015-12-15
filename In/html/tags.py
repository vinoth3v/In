import calendar
import html
import datetime

class HTMLObject(Object):

	__always_add_id_attribute__ = True

	def get_attributes(self):
		super().get_attributes()
		if self.__always_add_id_attribute__:
			self.attributes['id'] = self.id

		return self.attributes

builtins.HTMLObject = HTMLObject

class Tag(HTMLObject):
	__tag__ = 'div'


class Body(Tag):
	__tag__ = 'body'

class Head(Tag):
	__tag__ = 'head'

class Text(Tag):
	__tag__ = 'div'

class TextDiv(Text):
	__tag__ = 'div'

class TextP(TextDiv):
	__tag__ = 'p'

class TextSpan(TextDiv):
	__tag__ = 'span'

class Header(Tag):
	__tag__ = 'header'

class Footer(Header):
	__tag__ = 'footer'

class H1(Tag):
	__tag__ = 'h1'

class H2(Tag):
	__tag__ = 'h2'

class H3(Tag):
	__tag__ = 'h3'

class H4(Tag):
	__tag__ = 'h4'

class H5(Tag):
	__tag__ = 'h5'

class H6(Tag):
	__tag__ = 'h6'


class SiteHeader(Header):
	pass
class SiteFooter(Footer):
	pass

class Section(Tag):
	__tag__ = 'section'

class Aside(Tag):
	__tag__ = 'aside'

class Article(Tag):
	__tag__ = 'article'

class Nav(Tag):
	__tag__ = 'nav'

class Hr(Tag):
	__tag__ = 'hr'


class List(HTMLObject):

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		self.tag = args.get('tag','ul')

	def add(self, itm=None, **args):
		if not 'item_wrapper' in args:
			args['item_wrapper'] = 'li'
		return super().add(self, itm, **args)

class Ul(Tag):
	__tag__ = 'ul'

class Ol(Tag):
	__tag__ = 'ol'
	
class Li(Tag):
	__tag__ = 'li'



class Image(HTMLObject):

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		self.src = args.get('src', '')

	def get_attributes(self):
		attrs = super().get_attributes()
		if self.src:
			attrs['src'] = self.src
		return self.attributes


class Link(HTMLObject):

	def __init__(self, data = None, items = None, **args):

		self.href = '#'
		self.name = None

		super().__init__(data, items, **args)
		

	def get_attributes(self):
		super().get_attributes()
		if self.href is not None:
			self.attributes['href'] = self.href
		else:
			self.attributes['href'] = '/#'
		self.attributes['name'] = self.name
		return self.attributes


class HTMLField(HTMLObject):

	def __init__(self, data = None, items = None, **args):
		
		if data is None:
			data = {}

		data['required'] = data.get('required', False)
		data['error_message'] = data.get('error_message', None)
		data['has_errors'] = data.get('has_errors', None)
		data['placeholder'] = data.get('placeholder', None)
		
		# wrap all input fields in div
		if 'item_wrapper' not in data:
			data['item_wrapper'] = Object.new('TextDiv')

		super().__init__(data, items, **args)
		
		
			
	def get_value(self):
		return self.value
	def set_value(self, value):
		self.value = value
		self.validate()

	def get_def_value(self):
		return self.def_value
	def set_def_value(self, value):
		self.def_value = value

	def get_attributes(self):
		super().get_attributes()
		self.attributes['name'] = self.name
		self.attributes['title'] = self.title

		return self.attributes

	@staticmethod
	def def_required_mark():
		return '*'

class InputField(HTMLField):
	__input_type__ = 'text' # default to text

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)

	def get_attributes(self):
		super().get_attributes()

		self.attributes['value'] = self.value or self.def_value
		self.attributes['type'] = self.__input_type__
		if self.placeholder:
			self.attributes['placeholder'] = self.placeholder
		return self.attributes

	def validate():
		self.validators

class Submit(InputField):

	__tag__ = 'button'
	__input_type__ = 'submit'
	
	def __init__(self, data = None, items = None, **args):
		data['item_wrapper'] = data.get('item_wrapper', None)
		super().__init__(data, items, **args)
		

	def get_attributes(self):
		super().get_attributes()

		self.attributes['type'] = 'submit'

		return self.attributes

class Button(InputField):

	__tag__ = 'button'
	
	def __init__(self, data = None, items = None, **args):
		data['item_wrapper'] = data.get('item_wrapper', None)
		super().__init__(data, items, **args)
		
	def get_attributes(self):
		super().get_attributes()
		self.attributes['value'] = 'value'

		return self.attributes

class FieldSet(Tag):

	__tag__ = 'fieldset'


class TextBox(InputField):

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		self.size = args.get('size', 15)

	def get_attributes(self):
		super().get_attributes()

		if self.required:
			self.attributes['required'] = None # no value
		self.attributes['size'] = self.size
		
		self.attributes['value'] = html.escape(self.attributes['value'])

		return self.attributes


class TextBoxEmail(TextBox):
	__input_type__ = 'email'

class Password(TextBox):
	__input_type__ = 'password'


class TextArea(TextBox):

	def __init__(self, data = None, items = None, **args):
		if data is None:
			data = {}
		self.rows = data.get('rows', 5)
		super().__init__(data, items, **args)

	def get_attributes(self):
		super().get_attributes()
		self.attributes['rows'] = self.rows
		
		# no value in attributes
		if 'value' in self.attributes:
			del self.attributes['value']
		return self.attributes

class FileUpload(TextBox):
	__input_type__ = 'file'


class Hidden(InputField):
	__input_type__ = 'hidden'


class CheckBox(InputField):

	__input_type__ = 'checkbox'

	def __init__(self, data = None, items = None, **args):
		if data is None:
			data = {}
		self.checked = data.get('checked', False)
		self.label = data.get('label', '')
		super().__init__(data, items, **args)

	def get_attributes(self):
		super().get_attributes()
		self.attributes['value'] = self.value or self.def_value

		if self.checked:
			self.attributes['checked'] = None

		return self.attributes

#@IN.register('html.select', type = 'Object')
class HTMLSelect(HTMLField):
	__tag__ = 'select'
	
	multiple = False
	
	def __init__(self, data = None, items = None, **args):
		if data is None:
			data = {}

		self.multiple = str(data.get('multiple', False))
		self.options = str(data.get('options', {}))

		super().__init__(data, items, **args)

		# if multipe it is list or autocomplete
		if self.multiple and type(self.value) is not list:
			self.value = [self.value]

	def get_attributes(self):
		super().get_attributes()
		if self.multiple:
			self.attributes['multiple'] = None
		return self.attributes


class Option(HTMLField):
	__tag__ = 'option'

	def __init__(self, **args):
		self.selected = args.get('selected', False)
		super().__init__(**args)

	def get_attributes(self):
		super().get_attributes()
		if self.selected:
			self.attributes['selected'] = None

		return self.attributes


class OptionGroup(HTMLField):

	pass


class Options(HTMLField):

	def __init__(self, **args):
		self.multiple = args.get('multiple', False)
		self.size = args.get('size', 1)

		##select, list, checkbox, radio
		self.view_mode = args.get('view_mode', 'select')
		super().__init__(**args)

	def get_attributes(self):
		super().get_attributes()
		self.attributes['multiple'] = self.multiple
		self.attributes['size'] = self.size

		return self.attributes


class RadioBox(CheckBox):
	__input_type__ = 'radio'


class RadioBoxes(HTMLObject):

	def __init__(self, data = None, items = None, **args):
		self.options = {}
		
		super().__init__(data, items, **args)

class CheckBoxes(HTMLObject):

	def __init__(self, data = None, items = None, **args):
		self.multiple = True		
		self.options = {}

		super().__init__(data, items, **args)
		
		# value in list not found because of str to int types
		# convert all to str as options dict keys are str
		if self.value:
			if self.multiple:
				if type(self.value) is list or type(self.value) is set or type(self.value) is enumerate:
					newvals = [str(v) for v in self.value]
				else:
					self.value = [str(self.value)]
			else:
				self.value = str(self.value)

class DateSelect(HTMLField):
	__tag__ = 'div'

	def __init__(self, data = None, items = None, **args):
		if data is None:
			data = {}

		# always use date object or None
		if 'value' in data:
			value = data['value']
			if type(value) is dict: # submitted post data
				data['value'] = datetime.date(int(value['year']), int(value['month']), int(value['day']))
			if type(value) is int:
				data['value'] = datetime.date.fromtimestamp(value)

		data['year'] = data.get('year', range(datetime.date.today().year, 1900, -1))
		data['month'] = data.get('month', enumerate(calendar.month_name[1:]))
		data['day'] = data.get('day', range(1, 31))

		super().__init__(data, items, **args)


class HeadLink(HTMLObject):

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		self.href = str(args.get('href', '#'))
		self.media = str(args.get('media', ''))
		self.rel = str(args.get('rel', ''))
		self.link_type = str(args.get('link_type', ''))

class HTMLModalPopup(TextDiv):
	__tag__ = 'div'



#-----------------------------------------------------------------------
#							TABLE
#-----------------------------------------------------------------------


class HTMLTableColumn(Tag):
	''''''
	__tag__ = 'td'

class HTMLTableHColumn(HTMLTableColumn):
	__tag__ = 'th'

class HTMLTableRow(Tag):
	__allowed_children__ = HTMLTableColumn
	__tag__ = 'tr'
	

class HTMLTableRowContainer(Tag):
	__allowed_children__ = HTMLTableRow


class HTMLTableHeader(HTMLTableRowContainer):
	__tag__ = 'thead'
	
class HTMLTableFooter(HTMLTableRowContainer):
	__tag__ = 'tfoot'
	
class HTMLTableBody(HTMLTableRowContainer):
	__tag__ = 'tbody'

class HTMLTable(Tag):
	__tag__ = 'table'
	
	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)

		self.add('HTMLTableHeader', {
			'id' : 'header', 
			'weight' : 1
		})
		self.add('HTMLTableBody', {
			'id' : 'body', 
			'weight' : 2
		})
		self.add('HTMLTableFooter', {
			'id' : 'footer', 
			'weight' : 3
		})
		
		self.css.append('i-table')
