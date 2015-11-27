@IN.register('Comment', type = 'EntityAddForm')
class CommentAddForm(In.entity.EntityAddForm):
	'''Comment Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)

		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary'],
			'weight' : 50, # last
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Save'),
			'css' : ['i-button'] #  i-button-primary
		})

		self.css.append('ajax i-panel i-panel-box')

@IN.register('CommentAddForm', type = 'Former')
class CommentAddFormFormer(In.entity.EntityAddFormFormer):
	'''Comment Form Former'''
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		parent_id = int(form.args['parent_id'])
		
		if parent_id > 0:
			# set the increased level from parent comment level
			parent_comment = IN.entitier.load_single('Comment', parent_id)
			if parent_comment:
				form.processed_data['entity'].level = parent_comment.level + 1
				
	def submit(self, form, post):

		super().submit(form, post)
		
		if form.has_errors:
			return
		
		form.redirect = None
		
		# set result commands
		if form.entity_id is not None:
			comment = IN.entitier.load('Comment', form.entity_id)
			if comment is not None:
				output = IN.themer.theme(comment)
				element_id = '_'.join(('CommentListLazy', form.args['parent_entity_type'], str(form.args['parent_entity_id']), str(form.args['parent_id'])))
				form.result_commands = [{
					'method' : 'append',
					'args' : ['#' + element_id, output]
				}]

				# clear the body field
				for field in form['field_comment_body'].values():
					# TODO: reset to default
					field.value = ''


@IN.register('CommentAddForm', type = 'Themer')
class CommentAddFormThemer(FormThemer):
	'''CommentAddForm themer'''

	def theme(self, obj, format, view_mode, args):
		
		# chanage row size
		# TODO: move to admin field configuation
		if 'field_comment_body' in obj:
			for k, field in obj['field_comment_body'].items():
				if isinstance(field, In.html.tags.TextArea):
					field.rows = 1
		super().theme(obj, format, view_mode, args)

	def theme_process_variables(self, obj, format = 'html', view_mode = 'default', args = None):
		super().theme_process_variables(obj, format, view_mode, args)

		nabar = args['context'].nabar
		
		args['nabar_name'] = nabar.name
		args['nabar_id'] = nabar.id
		args['nabar_picture'] = IN.nabar.nabar_profile_picture_themed(nabar)
