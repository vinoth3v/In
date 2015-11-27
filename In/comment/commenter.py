
class Commenter:
	'''Comment controller'''

	def __init__(self):
		
		self.config_comments_enabled = RDict()

		self.build_config_comments_enabled()
		
	def build_config_comments_enabled(self):
		'''Build the comment configs'''
		
		cursor = IN.db.select({
			'table' : 'config.config_entity_bundle_comment',
		}).execute()

		if cursor.rowcount == 0:
			return
			
		enabled = self.config_comments_enabled
		
		for row in cursor:
			entity_type = row['entity_type']
			entity_bundle = row['entity_bundle']
			comment_bundle = row['comment_bundle']
			data = row['data']

			try:
				enabled[entity_type][entity_bundle] = {
					'comment_bundle' : comment_bundle,
					'data' : data,
				}
			except Exception as e:
				if entity_type not in enabled:
					enabled[entity_type] = {}
				enabled[entity_type][entity_bundle] = {
					'comment_bundle' : comment_bundle,
					'data' : data,
				}

		
	def get_container_id(self, entity):
		'''Returns container id for this Content/Parent entity'''
		
		# TODO: cache it
		
		db = IN.db
		connection = db.connection

		cursor = db.select({
			'table' : 'entity.comment_container',
			'columns' : ['id', 'type'],
			'where' : [
				['parent_entity_type', entity.__type__],
				['parent_entity_id', entity.id],
			],
			'order' : {'total_comments' : 'DESC'} # if having duplicates?
		}).execute()

		if cursor.rowcount == 0:
			container_id = self.create_comment_container(entity)			
			return container_id
			
		return cursor.fetchone()['id']
		
	def create_comment_container(self, entity):

		if not entity.id:
			return
		
		entity_type = entity.__type__

		if entity_type in {'Comment', 'CommentContainer'}: # 	recursive
			return

		entity_bundle = entity.type

		# only if comment enabled
		try:
			comment_bundle = self.config_comments_enabled[entity_type][entity_bundle]['comment_bundle']
		except:
			return # not enabled
		
		try:

			db = IN.db
			connection = db.connection
			#type = enabled_bundle[entity_bundle]

			values = ['comment', entity_type, entity.id]

			cursor = db.insert({
				'table' : 'entity.comment_container',
				'columns' : ['type', 'parent_entity_type', 'parent_entity_id'],
				'returning' : 'id',
			}).execute([values])

			new_id = cursor.fetchone()[0]

			connection.commit()
			
			return new_id
			
		except Exception as e:
			connection.rollback()
			IN.logger.debug()
			
	def entity_view(self, entity):

		entity_type = entity.__type__
		
		if entity_type in {'Comment', 'CommentContainer'}: # 	recursive
			return
		
		# TODO: add comments only if comments enabled
		container_id = self.get_container_id(entity)
		
		if not container_id:
			return
		data = {
			'lazy_args' : {
				'base_type' : 'Box',
				'load_args' : {
					'data' : {
						'container_id' : container_id,
						'parent_entity_type' : entity_type,
						'parent_entity_id' : entity.id,
					},
				},
			},
			'container_id' : container_id,
			'parent_entity_type' : entity_type,
			'parent_entity_id' : entity.id,
			'weight' : 10,
		}

		output = IN.context.response.output
		output.add('BoxEntityComments', data)
		
		entity_bundle = entity.type
			
		try:
			
			comment_bundle = self.config_comments_enabled[entity_type][entity_bundle]['comment_bundle']
			
			if IN.entitier.access('add', 'Comment', comment_bundle):
				
				data['weight'] = 11
				output.add('BoxEntityCommentAddForm', data)

		except:
			IN.logger.debug()
			pass
		
		#entity = IN.entitier.load_single(entity_type, entity.id)
		#print(555555555555, entity)
		#if entity:
			#add_form = self.get_comment_add_form(entity)
			#print(8888888888888, add_form)
			#if add_form:
				#IN.context.response.output.add(add_form)

		# load comments by container_id, make it ajax

		# TODO: add only if
		#	comments enabled
		#	comments display enabled in this view mode
		#	comments display enabled in this format

	def get_comment_add_form(self, entity, parent_id = 0):

		entity_type = entity.__type__
		entity_bundle = entity.type
		container_id = self.get_container_id(entity)
		if not container_id:
			return
			
		try:
			comment_bundle = self.config_comments_enabled[entity_type][entity_bundle]['comment_bundle']
		except:
			return
		
		args = {
			'parent_entity_type' : entity_type,
			'parent_entity_id' : entity.id,
			'parent_entity_bundle' : entity_bundle,
			'comment_bundle' : comment_bundle,
			'container_id' : container_id,
			'parent_id' : parent_id,
		}
		
		form = IN.entitier.get_entity_add_form('Comment', comment_bundle, args)
		
		return form

	def get_comment_delete_form(self, comment):
		
		form = IN.entitier.get_entity_delete_form(comment)
		
		return form
		
	def get_comment_edit_form(self, comment):
		
		form = IN.entitier.get_entity_edit_form(comment.__type__, comment.id)
		
		return form
