import html
import copy
from In.themer.object_themer import ObjectThemer


@IN.register('HTMLObject', type = 'Themer')
class HTMLObjectThemer(ObjectThemer):
	''''''

builtins.HTMLObjectThemer = HTMLObjectThemer

@IN.register('Tag', type = 'Themer')
class TagThemer(ObjectThemer):

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		args['tag'] = obj.__tag__

@IN.register('Text', type = 'Themer')
class TextThemer(TagThemer):
	''''''

@IN.register('TextDiv', type = 'Themer')
class TextDivThemer(TagThemer):
	''''''

@IN.register('HTMLField', type = 'Themer')
class HTMLFieldThemer(ObjectThemer):

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		if obj.has_errors:
			excls = IN.APP.config.css['extra']
			if 'form_input_error_message' in excls:
				cls = excls['form_input_error_message']
			else:
				cls = ''

			if obj.error_message:
				args['error_message'] = ''.join(('<div class="', cls, '">', obj.error_message, '</div>'))
			else:
				args['error_message'] = ''
		else:
			args['error_message'] = ''

		args['title'] = obj.title or ''
		args['info'] = obj.info or ''


	def theme_css(self, obj, item_index=0, ref=2):
		if obj.has_errors:
			excls = IN.APP.config.css['extra']
			if 'form_input_error' in excls:
				obj.css.append(excls['form_input_error'])
			else:
				obj.css.append('has-error')
		return super().theme_css(obj)

@IN.register('InputField', type = 'Themer')
class InputFieldThemer(HTMLFieldThemer):
	''''''


@IN.register('TextBox', type = 'Themer')
class TextBoxThemer(InputFieldThemer):
	''''''

	def theme_value(self, obj, format, view_mode, args):
		value = super().theme_value(obj, format, view_mode, args)
		# always convert to str, # number field
		value = str(value)
		value = html.escape(value, quote = True)
		return value


@IN.register('TextArea', type = 'Themer')
class TextAreaThemer(InputFieldThemer):
	''''''

#@IN.register('Password', type = 'Themer')
#class PasswordThemer(TextBoxThemer):

	#def theme_process_variables(self, obj, args):
		#super().theme_process_variables(obj, args)
		#args['type'] = obj.__input_type__

@IN.register('Submit', type = 'Themer')
class SubmitThemer(InputFieldThemer):

	pass

@IN.register('Button', type = 'Themer')
class ButtonThemer(InputFieldThemer):

	pass

@IN.register('FieldSet', type = 'Themer')
class FieldSetThemer(TagThemer):

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		args['title'] = obj.title


@IN.register('CheckBox', type = 'Themer')
class CheckBoxThemer(InputFieldThemer):

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		args['title'] = obj.title
		args['label'] = obj.label

@IN.register('Link', type = 'Themer')
class LinkThemer(InputFieldThemer):

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		args['value'] = obj.value or obj.def_value



@IN.register('HeadLink', type = 'Themer')
class HeadLinkThemer(ObjectThemer):

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		args['href'] = obj.href
		args['media'] = obj.media
		args['rel'] = obj.rel
		args['link_type'] = obj.link_type



@IN.register('RadioBoxes', type = 'Themer')
class RadioBoxesThemer(HTMLFieldThemer):

	def theme_prepare(self, obj, format, view_mode, args):
		'''only add options here, so modules can change options.'''

		super().theme_prepare(obj, format, view_mode,  args)
		name = obj.name
		obj_value = obj.value

		weight = 0
		for value, label in obj.options.items():
			checked = value == obj_value
			
			if type(label) is dict:
				c_label = label['label']
				c_info = label.get('info', '')
			else:
				c_label = label
				c_info = ''
				
			data = {
				'name' : name,
				'value' : value,
				'label' : c_label,
				'weight' : weight,
				'checked' : checked,
				'info' : c_info,
			}

			if obj.child_additional_data:
				additional_data = copy.deepcopy(obj.child_additional_data)
				data.update(additional_data)
				

			o = obj.add('RadioBox', data)
			weight += 1



@IN.register('CheckBoxes', type = 'Themer')
class CheckBoxesThemer(HTMLFieldThemer):

	def theme_prepare(self, obj, format, view_mode, args):
		'''only add options here, so modules can change options.'''

		super().theme_prepare(obj, format, view_mode,  args)
		name = obj.name
		obj_value = obj.value
		
		weight = 0

		for value, label in obj.options.items():
			if obj.multiple:
				checked = value in obj_value
			else:
				checked = value == obj_value
			
			if type(label) is dict:
				c_label = label['label']
				c_info = label.get('info', '')
			else:
				c_label = label
				c_info = ''
				
			data = {
				'name' : name,
				'value' : value,
				'label' : c_label,
				'weight' : weight,
				'checked' : checked,
				'info' : c_info,
			}

			if obj.child_additional_data:
				data.update(copy.deepcopy(obj.child_additional_data))

			obj.add('CheckBox', data)
			weight += 1

@IN.register('HTMLSelect', type = 'Themer')
class HTMLSelectThemer(HTMLFieldThemer):

	def theme_process_variables(self, obj, format, view_mode, args):
		'''only add options here, so modules can change options.

		speed: Creating many option object and theme each of them are very heavy!
		'''

		super().theme_process_variables(obj, format, view_mode,  args)
		name = obj.name
		select_options = obj.value

		if obj.multiple:
			selected = lambda v: 'selected' if v in select_options else ''
		else:
			selected = lambda v: 'selected' if v == select_options else ''

		if isinstance(obj.options, dict):
			options = [''.join(['<option value="', str(value), '" ', selected(value), ' >', str(label), '</option>']) for value, label in obj.options.items()]
		elif isinstance(obj.options, enumerate):
			options = [''.join(['<option value="', str(value+1), '" ', selected(value+1), ' >', str(label), '</option>']) for value, label in obj.options]
		else:
			options = [''.join(['<option value="', str(value), '" ', selected(value), ' >', str(value), '</option>']) for value in obj.options]

		# add empty
		if not obj.required:
			options.insert(0, '<option value=""></option>')
		options = ''.join(options)
		args['options'] = options

@IN.register('DateSelect', type = 'Themer')
class DateSelectThemer(HTMLFieldThemer):

	def theme_prepare(self, obj, format, view_mode, args):
		'''add select.'''

		super().theme_prepare(obj, format, view_mode,  args)
		name = obj.name

		weight = 0
		value = obj.value
		if not value:
			class emptydate:
				day = 0
				month = 0
				year = 0
			value = emptydate()

		set = obj.add('TextDiv', {
			'css' : ['i-grid']
		})
		set.add('HTMLSelect', {
			'id' : obj.id + '-day',
			'name' : obj.name + '[day]',
			'title' : s('Day'),
			'options' : obj.day,
			'value' : value.day,
			'required' : obj.required,
			'multiple' : False,
		})
		set.add('HTMLSelect', {
			'id' : obj.id + '-month',
			'name' : obj.name + '[month]',
			'title' : s('Month'),
			'options' : obj.month,
			'value' : value.month,
			'required' : obj.required,
			'multiple' : False,
		})
		set.add('HTMLSelect', {
			'id' : obj.id + '-year',
			'name' : obj.name + '[year]',
			'title' : s('Year'),
			'options' : obj.year,
			'value' : value.year,
			'required' : obj.required,
			'multiple' : False,
		})
		#obj.css.append('')


@IN.register('SiteFooter', type = 'Themer')
class SiteFooterThemer(TagThemer):

	pass

@IN.register('HTMLModalPopup', type = 'Themer')
class HTMLModalPopupThemer(TextDivThemer):

	def theme_process_variables(self, obj, format, view_mode, args):

		args['title'] = obj.title
		super().theme_process_variables(obj, format, view_mode, args)
