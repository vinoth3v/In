from collections import OrderedDict

@IN.register('FlagType', type = 'EntityAddForm')
class FlagTypeAddForm(In.entity.EntityAddForm):
	'''FlagType Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		# TODO: early validate: one flag type per flag bundle
		
		set = self.add('FieldSet', {
			'id' : 'configset',
			'css' : ['i-form-row'],
			'weight' : 0,
		})
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		
		set = self.add('FieldSet', {
			'id' : 'addedset',
			'css' : ['i-form-row i-panel i-panel-box i-margin-medium'],
			'weight' : 0,
			'title' : s('Enabled Entities & Bundles'),
		})
		
		entity_types = IN.entitier.entity_bundle.keys()
		
		flag_entity_types = post.get('enabled_entity_type', [])
		if type(flag_entity_types) is str:
			flag_entity_types = [flag_entity_types]
		
		si = sorted(flag_entity_types, key = lambda o: o)
		for flag_entity_type in si:
			
			html_field_name = 'enabled_entity_type' #flag_entity_type.join(('entity_type[', ']'))
			html_field_name_bundle = 'entity_type_' + flag_entity_type + '_bundle'
			
			# always add to addedset
			set = self['addedset']
			
			set = set.add('FieldSet', {
				'id' : flag_entity_type + '_set',
				'css' : ['i-form-row'],
				'weight' : 0,
				'title' : flag_entity_type,
			})
			
			o = set.add('Hidden', {
				'id' : 'entity_type_' + flag_entity_type,
				'name' : html_field_name,
				'value' : flag_entity_type,	
			})
			
			options = OrderedDict()
			options['*'] = s('Any bundle')
			
			flag_entity_bundles = post.get(html_field_name_bundle, ['*'])
			if type(flag_entity_bundles) is str:
				flag_entity_bundles = [flag_entity_bundles]
			
			if flag_entity_type is not None:
				# get bundles
				for bundle in IN.entitier.entity_bundle[flag_entity_type].keys():
					options[bundle] = bundle
			
			o = set.add('CheckBoxes', {
				'id' : html_field_name_bundle,
				'value' : flag_entity_bundles,
				#'title' : ' '.join((flag_entity_type, s('bundles'))),
				'options' : options,
				'required' : False,
				'css' : ['i-width-1-1 i-form-large'],
				#'info' : s('Allow only these bundles.'),
				'validation_rule' : [
					['Not', [['Empty', '']], s('Entity bundle is required!')]
				],
				'weight' : 6,
			})
			
		
		self.ajax_elements.append('addedset')
		
		set = self.add('FieldSet', {
			'id' : 'addset',
			'css' : ['i-form-row i-panel i-panel-box'],
			'weight' : 10,
			'title' : s('Select entity & bundles')
		})
		
		## allow only rest of them
		entity_types = [key for key in sorted(entity_types, key = lambda o: o) if key not in flag_entity_types]
		
		flag_entity_type = post.get('new_entity_type', None)
		
		# always display value to make sure bundle displays the correct values		
		if flag_entity_type is None and entity_types:
			flag_entity_type = list(entity_types)[0]
		
		set.add('HTMLSelect', {
			'id' : 'new_entity_type',
			'name' : 'new_entity_type',
			'value' : flag_entity_type,
			'title' : s('Entity type'),
			'options' : entity_types,
			'required' : True,
			'css' : ['ajax i-width-1-1 i-form-large'],
			'multiple' : False,
			'info' : s('The type of entity this field may reference to.'),
			'validation_rule' : [
				['Not', [['Empty', '']], s('Entity type is required!')]
			],
			'attributes' : {'data-ajax_partial' : 1},
			'weight' : 5,
		})
		
		options = OrderedDict()
		options['*'] = s('Any bundle')
		
		if flag_entity_type is not None:
			# get bundles
			for bundle in IN.entitier.entity_bundle[flag_entity_type].keys():
				options[bundle] = bundle
		
		bundle_element = set.add('CheckBoxes', {
			'id' : 'new_entity_bundle',
			'name' : 'new_entity_bundle',
			'value' : post.get('new_entity_bundle', None),
			'title' : s('Entity bundle'),
			'options' : options,
			'required' : False,
			'css' : ['i-width-1-1 i-form-large'],
			'info' : s('Allow only these bundles.'),
			'validation_rule' : [
				['Not', [['Empty', '']], s('Entity bundle is required!')]
			],
			'weight' : 6,
		})
		
		set = self.add('FieldSet', {
			'id' : 'configset',
			'css' : ['i-form-row'],
			'weight' : 11,
		})
		
		set.add('TextArea', {
			'id' : 'statuses',
			'title' : s('Flag statuses'),
			'value' : post.get('statuses', ''),
			'css' : ['i-width-1-1 i-form-large'],
			'weight' : 8,
			'info' : s('''Flag statuses key, notflagged, flagged values separated by :, one per line <br>
			example:  <br>
			like:Like <br>
			unlike:Liked'''),
		})
		
		
		set.add('TextArea', {
			'id' : 'count_by_statuses',
			'title' : s('Count by statuses'),
			'value' : post.get('count_by_statuses', ''),
			'css' : ['i-width-1-1 i-form-large'],
			'weight' : 8,
			'info' : s('''Use these statuses to count flags.'''),
		})
		
		self.ajax_elements.append('addset')
		
		set.add('Submit', {
			'id' : 'addanother',
			'value' : s('Add another entity'),
			'css' : ['ajax i-button i-button-primary'],
			'attributes' : {'data-ajax_partial' : 1},
			'weight' : 10,
		})

		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary'],
			'weight' : 50, # last
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Save'),
			'css' : ['i-button i-button-primary i-button-large']
		})

		self.css.append('ajax i-panel i-panel-box i-margin-large')

@IN.register('FlagTypeAddForm', type = 'Former')
class FlagTypeAddFormFormer(In.entity.EntityAddFormFormer):
	'''FlagType Form Former'''
	
	def validate(self, form, post):
		if form.has_errors:
			return
		
		statuses = post.get('statuses', '').split('\n')
		
		for status in statuses:
			status = status.split(':')
			key = status[0].strip()
			if len(status) != 2:
				form.has_errors = True
				form.error_message = s('Invalid flag statues text')
			
	def submit_partial(self, form, post):
		
		super().submit_partial(form, post)
		
		if post['element_id'] == 'addanother':
			
			set = form['addedset']
			
			if 'new_entity_type' not in post:
				return
				
			flag_entity_type = post['new_entity_type']
			
			# field may be empty
			if 'new_entity_bundle' in post:
				flag_entity_bundles = post['new_entity_bundle']
			else:
				flag_entity_bundles = ['*']
			
			html_field_name = 'enabled_entity_type' #flag_entity_type.join(('entity_type[', ']'))
			html_field_name_bundle = 'entity_type_' + flag_entity_type + '_bundle'

			set = set.add('FieldSet', {
				'id' : flag_entity_type + '_set',
				'css' : ['i-form-row'],
				'weight' : 0,
				'title' : flag_entity_type,
			})
			
			o = set.add('Hidden', {
				'id' : 'entity_type_' + flag_entity_type,
				'name' : html_field_name,
				'value' : flag_entity_type,	
			})
			
			options = OrderedDict()
			options['*'] = s('Any bundle')
			
			if flag_entity_type is not None:
				# get bundles
				for bundle in IN.entitier.entity_bundle[flag_entity_type].keys():
					options[bundle] = bundle
			
			o = set.add('CheckBoxes', {
				'id' : html_field_name_bundle,
				'value' : flag_entity_bundles,
				#'title' : ' '.join((flag_entity_type, s('bundles'))),
				'options' : options,
				'required' : False,
				'css' : ['i-width-1-1 i-form-large'],
				#'info' : s('Allow only these bundles.'),
				'validation_rule' : [
					['Not', [['Empty', '']], s('Entity bundle is required!')]
				],
				'weight' : 6,
			})
			
			form.ajax_elements.append('addedset')
		
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		entity_type = form.args['entity_type']
		
		flag_type_entity = form.processed_data['entity']
		
		entity_bundle = {}
		
		entity_types = post.get('enabled_entity_type', [])
		if type(entity_types) is str:
			entity_types = [entity_types]
		
		for entity_type in entity_types:
			
			bundle_name = 'entity_type_' + entity_type + '_bundle'
			
			bundles = post.get(bundle_name, ['*'])
			
			if type(bundles) is str:
				bundles = [bundles]
			
			entity_bundle[entity_type] = bundles
		
		flag_type_entity.data['entity_bundle'] = entity_bundle
		
		flag_status = [] # we need ordering
		statuses = post.get('statuses', '').split('\n')
		
		count_by_statuses = []
		for s in post.get('count_by_statuses', '').split(','):
			count_by_statuses.append(s.strip())
		
		flag_type_entity.data['count_by_statuses'] = count_by_statuses
		
		
		for status in statuses:
			status = status.split(':')
			
			flag_status.append([status[0].strip(), status[1].strip()])
		
		flag_type_entity.data['flag_status'] = flag_status
		
		form.redirect = entity_type.join(('admin/structure/entity/!', '/list'))
		
	def submit(self, form, post):
		
		super().submit(form, post)
		
		if form.has_errors:
			return
		
		form.redirect = 'admin/structure/entity/!FlagType/list'
		
