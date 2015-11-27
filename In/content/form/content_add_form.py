@IN.register('Content', type = 'EntityAddForm')
class ContentAddForm(In.entity.EntityAddForm):
	'''Content Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		set = self.add('FieldSet', {
			'id' : 'adminset',
			'css' : ['i-form-row i-text-primary'],
			'weight' : 100,
		})
		
		# admin
		if IN.entitier.access('admin', self.entity_type, self.entity_bundle):
			
			# nabar 
			
			field_options = {}
			field_value = None
			if 'nabar' in post:
				nabar_id = post['nabar']
				if nabar_id.isnumeric():
					nabar = IN.entitier.load_single('Nabar', int(nabar_id))
					if nabar:
						field_value = nabar.id
						field_options[field_value] = nabar.name
			
			set.add('HTMLSelect', { # TextBox
				'id' : 'nabar',
				'name' : 'nabar',
				'value' : field_value,
				'options' : field_options,
				'css' : ['autocomplete i-width-1-1'],
				'multiple' : False,
				'attributes' : {
					'data-autocomplete_max_items' : 1,
					'data-autocomplete_create' : '0',
					'data-autocomplete_url' : '/nabar/autocomplete',
					#'data-autocomplete_options' : init_options,
				},
				'weight' : 0,
			})
			
			# published
			set.add('CheckBox', {
				'label' : 'Published',
				'id' : 'published',
				'value' : 1,	# returned value if checked
				'checked' : post.get('published', 0) == '1',
				'weight' : 1,
			})
			
			# featured
			set.add('CheckBox', {
				'label' : 'Featured content?',
				'id' : 'featured',
				'value' : 1,	# returned value if checked
				'checked' : post.get('featured', 0) == '1',
				'weight' : 2,
			})
			
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary'],
			'weight' : 101, # last
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Save'),
			'css' : ['i-button i-button-primary i-button-large']
		})
		
		self.css.append('ajax i-panel i-panel-box i-margin-large')
		self.css.append('ContentEditForm-bundle-' + self.entity_bundle)

@IN.register('ContentAddForm', type = 'Former')
class ContentAddFormFormer(In.entity.EntityAddFormFormer):
	'''Content Form Former'''

	def validate(self, form, post):
		
		#if form.has_errors:
			#return
		
		if IN.entitier.access('admin', form.entity_type, form.entity_bundle):
			nabar_id = form['adminset']['nabar'].value
			
			if nabar_id is not None:
				nabar = IN.entitier.load_single('Nabar', nabar_id)
				
				if not nabar:
					form.has_errors = True
					form['adminset']['nabar'].error_message = s('Invalid Nabar!')
				
		
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
			
		# create entity object from form post
		entity_type = form.entity_type
		entity_bundle = form.entity_bundle

		entity = form.processed_data['entity']
		
		if IN.entitier.access('admin', entity_type, entity_bundle):
			entity.featured = post.get('featured', 0) == '1'
			if post.get('published', 0) == '1':
				entity.status = 1 # change only if set
			
			# set nabar
			nabar_id = form['adminset']['nabar'].value
			if type(nabar_id) is int:
				entity.nabar_id = int(nabar_id)
			
		else:
			# make featured in bundle config
			entity.featured = False # default
			
