import In.boxer


class BoxEntityComments(In.boxer.Box):
	
	def __init__(self, data = None, items = None, **args):

		self.level = 0
		self.parent_id = 0
		
		super().__init__(data, items, **args)

		container_id = self.container_id,
		parent_entity_type = self.parent_entity_type
		parent_entity_id = self.parent_entity_id

		#self.css.append('border-w2')

@IN.register('BoxEntityComments', type = 'Themer')
class BoxEntityCommentsThemer(In.boxer.BoxThemer):
	#ReactCommentBox

	def theme_items(self, obj, format, view_mode, args):

		data = {
			'level' : obj.level,
			'parent_id' : obj.parent_id,
			'container_id' : obj.container_id,
			'parent_entity_type' : obj.parent_entity_type,
			'parent_entity_id' : obj.parent_entity_id,
			'lazy_args' : {
				'load_args' : {
					'data' : {
						'container_id' : obj.container_id,
						'parent_entity_type' : obj.parent_entity_type,
						'parent_entity_id' : obj.parent_entity_id,
						'level' : obj.level,
						'parent_id' : obj.parent_id,
					},
				}
			},
		}
		
		v = obj.add('CommentListLazy', data)
		
		super().theme_items(obj, format, view_mode, args)

	def theme_process_variables(self, obj, format, view_mode, args):

		super().theme_process_variables(obj, format, view_mode, args)

		args['level'] = obj.level
		args['parent_id'] = obj.parent_id
		args['container_id'] = obj.container_id
		args['parent_entity_type'] = obj.parent_entity_type
		args['parent_entity_id'] = obj.parent_entity_id


class BoxEntityCommentAddForm(In.boxer.BoxLazy):
	
	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)

		container_id = self.container_id,
		parent_entity_type = self.parent_entity_type
		parent_entity_id = self.parent_entity_id
		commenter = IN.commenter
		
		# always set new id
		self.id = '_'.join(('BoxEntityCommentAddForm', parent_entity_type, str(parent_entity_id)))
		if IN.context.request.ajax:
		
			entity = IN.entitier.load_single(parent_entity_type, parent_entity_id)
			if entity:
				
				entity_bundle = entity.type
			
				try:
					
					comment_bundle = commenter.config_comments_enabled[parent_entity_type][entity_bundle]['comment_bundle']
					if IN.entitier.access('add', 'Comment', comment_bundle):
						add_form = commenter.get_comment_add_form(entity)
						if add_form:
							self.add(add_form)
							
				except:
					IN.logger.debug()
					pass

@IN.register('BoxEntityCommentAddForm', type = 'Themer')
class BoxEntityCommentAddFormThemer(In.boxer.BoxLazyThemer):
	''''''
