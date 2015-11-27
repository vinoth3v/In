
class FormSearch(Form):

	def __init__(self, data = None, items = None, post = None, **args):
		
		super().__init__(data, items, **args)
		
		self.method = 'GET'
		
		query = post.get('q', None) or IN.context.request.args['query'].get('q', '')
		
		wrapper = Object.new('TextDiv', {
			'css' : ['i-width-5-6'],
		})
		self.add('TextBox', {
			'id' : 'q',
			'value' : query,
			'placeholder' : s('search disabled'),
			'css' : ['i-form-large i-width-1-1'],
			'weight' : 1,
			'item_wrapper' : wrapper,
			'attributes' : {'disabled' : None}
		})
		
		wrapper = Object.new('TextDiv', {
			'css' : ['i-width-1-6'],
		})
		self.add('Submit', {
			'value' : '<i class="i-icon-search"></i>',
			'css' : ['i-button i-width-1-1 i-button-large i-button-success'],
			'weight' : 2,
			'item_wrapper' : wrapper
		})
		
		self.css.append('ajax i-grid i-width-1-1 i-form i-displai-inline-block i-grid-collapse')
		
@IN.register('FormSearch', type = 'Former')
class FormSearchFormer(FormFormer):
	'''FormSearch Former'''
	
	#def load_arguments(self, form_id, post, args):
		#if 'entity_type' in post:
			#args['entity_type'] = post['entity_type']
		#if 'entity_bundle' in post:
			#args['entity_bundle'] = post['entity_bundle']


	#def validate(self, form, post):

		#if form.has_errors: # fields may have errors
			#return

		#field_type = form['addset']['field_type'].value
		#field_name = form['addset']['field_name'].value

		#if not field_type or not field_name:
			#form.has_errors = True
			#form.error_message = s('Field name cannot be empty!')


	def submit(self, form, post):
		
		if form.has_errors:
			return
		
		query = post.get('q', None) or IN.context.request.args['query'].get('q', '')
		
		if query:
			form.redirect = 'search?q=' + query
		
		#entity_type = form.entity_type
		#entity_bundle = form.entity_bundle
		#addset = form['addset']
		
		#field_type = addset['field_type'].value

		#field_type = field_type[0]
		
		#field_name = addset['field_name'].value
		## always start with field_
		#if not field_name.startswith('field_'):
			#field_name = 'field_' + field_name
		
		#title = addset['title'].value

		#weight = 0
		#status = 1
		
		#data = {
			#'title' : title,
		#}
		
		#fielder = IN.fielder
		#try:
			#created = fielder.__create_new_field__(entity_type, entity_bundle, field_type, field_name, status, weight, data)
			
			#if not created:
				## unknown error
				#form.has_errors = True
				#form.error_message = s('Unknown error occurred while creating new field!')
				#return
			
			#form.redirect = ''.join(('admin/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/field/!', field_name, '/edit'))
			
		#except Exception as e:
			#IN.logger.debug()
			#form.has_errors = True
			#form.error_message = ' '.join((s('Error while creating new field!'), str(e)))

		
@IN.register('FormSearch', type = 'Themer')
class FormSearchThemer(FormThemer):

	def theme(self, obj, format, view_mode, args):
		super().theme(obj, format, view_mode, args)

		obj.css.remove('i-panel i-panel-box')
