

#-----------------------------------------------------------------------
#					Comment
#-----------------------------------------------------------------------

class Comment(In.entity.Entity):
	'''Comment Entity class.
	'''
	
	def __init__(self, data = None, items = None, **args):

		# default
		self.nabar_id = 0
		self.parent_id = 0
		self.container_id = 0
		self.level = 0
		self.parent_entity_type = ''
		self.parent_entity_id = 0
		
		super().__init__(data, items, **args)

		# TODO: move this logic to entitier
		
		if not self.parent_entity_type:
			
			container = IN.entitier.load_single('CommentContainer', self.container_id)
			
			if container:
				
				self.parent_entity_type = container.parent_entity_type
				self.parent_entity_id = container.parent_entity_id
		
#-----------------------------------------------------------------------
#					Comment Entitier
#-----------------------------------------------------------------------

@IN.register('Comment', type = 'Entitier')
class CommentEntitier(In.entity.EntityEntitier):
	'''Base Comment Entitier'''

	# Comment insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = False

	def entity_context_links(self, entity, context_type, format, view_mode):

		entitier = IN.entitier
		
		# no view access
		if not entitier.access('view', entity):
			return

		id_suffix = '-'.join((entity.__type__, str(entity.id)))
		
		output = super().entity_context_links(entity, context_type, format, view_mode)
		
		if context_type == 'links':
			
			if entitier.access('edit', entity):
				
				edit = Object.new(type = 'Link', data = {
					'id' : 'edit-link-' + id_suffix,
					'css' : ['i-button i-button-small'],
					'value' : s('edit'),
					'href' : '/'.join(('/comment', str(entity.id), 'edit')),
					'weight' : 0,
					'attributes' : {
						'data-ajax_type' : 'POST',
					}
				})
				output[edit.id] = edit

			if entitier.access('delete', entity):
				delete = Object.new(type = 'Link', data = {
					'id' : 'delete-link-' + id_suffix,
					'css' : ['no-ajax ajax-modal i-button i-button-small'], # no-ajax needed here or it bind twice
					'value' : s('delete'),
					'href' : '/'.join(('/comment', str(entity.id), 'delete', 'confirm')),
					'weight' : 1,
					'attributes' : {
						'data-ajax_type' : 'POST',
					}
				})
				output[delete.id] = delete

			if entitier.access('reply', entity):

				#db = IN.db

				#container = IN.entitier.load_single('CommentContainer', entity.container_id)
				
				#cursor = db.select({
					#'table' : 'entity.comment_container',
					#'where' : [['id', entity.container_id]]
				#}).execute()

				#if cursor.rowcount == 0:
					#return
				#row = cursor.fetchone()
				
				parent_entity_type = entity.parent_entity_type
				parent_entity_id = entity.parent_entity_id


				# allow reply only if level
				entity_bundle = IN.entitier.load_single(parent_entity_type, parent_entity_id).type
				config = IN.commenter.config_comments_enabled
				config = config.get(parent_entity_type, {}).get(entity_bundle, {})
				comment_level = config.get('data', {}).get('comment_level', 0)

				if entity.level < comment_level:
					edit = Object.new(type = 'TextDiv', data = {
						'id' : 'repli-link-' + id_suffix,
						'css' : ['ajax i-button i-button-small'],
						'value' : s('reply'),
						#'href' : '/comment/reply/!' + '/'.join((parent_entity_type, str(parent_entity_id), str(entity.id), str(entity.container_id))),
						'weight' : 3,
						'attributes' : {
							'data-ajax_type' : 'POST',
							'data-href' : '/comment/reply/!' + '/'.join((parent_entity_type, str(parent_entity_id), str(entity.id), str(entity.container_id))),
						},
					})
					output[edit.id] = edit

			#if entitier.access('delete', entity):
				
				#edit = Object.new(type = 'Link', data = {
					#'id' : 'delete-link-' + id_suffix,
					#'css' : ['ajax i-button'],
					#'value' : s('delete'),
					##'href' : s('#'),
					#'weight' : 1,
				#})
				#output[edit.id] = edit

		return output


	#def delete(self, entity, commit = True):
		#'''Recursively delete coments and its sub coments'''
		
		##result = entity.Model.delete(entity, commit)
		
		## Instead of delete and its all sub comments
		## just disable this comment only

		#try:
			
			#entity.Model.delete(entity, commit)
			
			## clear the cache
			#self.cacher.remove(entity.id)
			#if self.entity_load_all:
				#self.cacher.remove('all')

			## hook invoke
			#if self.invoke_entity_hook:
				#IN.hook_invoke('_'.join(('entity_delete', entity.__type__, entity.type)), entity)
				#IN.hook_invoke('entity_delete_' + entity.__type__, entity)

			## heavy. dont implement
			#IN.hook_invoke('__entity_delete__', entity)
			
			#return True
			
		#except Exception as e:
			#IN.logger.debug()
			#return False
	
	
#-----------------------------------------------------------------------
#					Comment Model
#-----------------------------------------------------------------------

@IN.register('Comment', type = 'Model')
class CommentModel(In.entity.EntityModel):
	'''Comment Model'''
	
	not_updatable_columns = ['id', 'type', 'created', 'container_id', 'parent_id', 'level']
	set_deleted_status = True
	
	#def delete(self, entity, commit = True):
		#'''Recursively delete coments and its sub coments'''
		
		##result = entity.Model.delete(entity, commit)
		
		## Instead of delete and its all sub comments
		## just disable this comment only
		
		## TODO: sub comment delete
		#connection = IN.db.connection

		#try:
			
			#table_info = self.model['table']
			#table = table_info['name']
			#columns = table_info['columns']
			
			#cursor = IN.db.update({
				#'table' : table,
				#'set' : [['status', self.status_deleted]],
				#'where' : ['id', int(entity.id)]
			#}).execute()
			
			#if commit: # if caller will not handle the commit
				#connection.commit()

		#except Exception as e:
			#if commit:
				#connection.rollback()
			#IN.logger.debug()
			#raise e # re raise
			
		#return True
	
#-----------------------------------------------------------------------
#					CommentContainer
#-----------------------------------------------------------------------

class CommentContainer(In.entity.Entity):
	'''CommentContainer Entity class.
	'''
	
	total_comments = 0
	

@IN.register('CommentContainer', type = 'Entitier')
class CommentContainerEntitier(In.entity.EntityEntitier):
	'''Base CommentContainer Entitier'''

@IN.register('CommentContainer', type = 'Model')
class CommentContainerModel(In.entity.EntityModel):
	'''CommentContainer Model'''


class CommentListLazy(In.core.lazy.HTMLObjectLazy):
	'''list of comments'''

	def __init__(self, data = None, items = None, **args):

		
		self.level = 0
		self.parent_id = 0
		
		super().__init__(data, items, **args)

		container_id = self.container_id
		parent_entity_type = self.parent_entity_type
		parent_entity_id = self.parent_entity_id
		level = self.level
		parent_id = self.parent_id

		# add react comment box
		#IN.context.asset.add_js('/files/assets/js/react.comment.js', 'react.comment')
		
		# always set new id
		self.id = '_'.join(('CommentListLazy', parent_entity_type, str(parent_entity_id), str(parent_id)))
		
		if IN.context.request.ajax_lazy:
			
			entity = IN.entitier.load_single(parent_entity_type, parent_entity_id)
			
			if entity:

				db = IN.db
				connection = db.connection

				# TODO: paging
				# get total
				total = 0
				limit = 5
				cursor = db.select({
					'table' : 'entity.comment',
					'columns' : ['count(id)'],
					'where' : [
						['container_id', container_id],
						['parent_id', parent_id],
						['status', 1],
					],
				}).execute()
				if cursor.rowcount >= 0:
					total = int(cursor.fetchone()[0])
				
				if total > 0:
					cursor = db.select({
						'table' : 'entity.comment',
						'columns' : ['id'],
						'where' : [
							['container_id', container_id],
							['parent_id', parent_id],				# add main level comments only
							['status', 1],
						],
						'order' : {'created' : 'DESC'},
						'limit'	: limit,
					}).execute()

					ids = []
					last_id = 0
					if cursor.rowcount >= 0:
						for row in cursor:
							ids.append(row['id'])

						last_id = ids[-1] # last id

						comments = IN.entitier.load_multiple('Comment', ids)
						
						for id, comment in comments.items():
							comment.weight = id	# keep order
							self.add(comment)
		
					remaining = total - limit
					if remaining > 0 and  last_id > 0:
						self.add('TextDiv', {
							'id' : '_'.join(('more-commens', parent_entity_type, str(parent_entity_id), str(self.parent_id))),
							'value' : ' '.join((str(remaining), s('more comments'))),
							'css' : ['ajax i-text-center i-text-danger pointer'],
							'attributes' : {
								'data-href' : ''.join(('/comment/more/!Content/', str(parent_entity_id), '/', str(last_id), '/', str(self.parent_id)))
							},
							'weight' : -1
						})

		self.css.append('comment-list p2')
		
@IN.hook
def entity_model():
	# TODO: anonymous comments
	return {
		'Comment' : {						# entity name
			'table' : {						# table
				'name' : 'comment',
				'columns' : {				# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'parent_id' : {}, 		# nested comments
					'container_id' : {}, 	# comment container
					'level' : {},			# comment level
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
		'CommentContainer' : {				# entity name
			'table' : {						# table
				'name' : 'comment_container',
				'columns' : {				# table columns / entity attributes
					'id' : {},
					'type' : {},
					'parent_entity_type' : {},
					'parent_entity_id' : {},
					'total_comments' : {}
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('Comment', type = 'Themer')
class CommentThemer(In.entity.EntityThemer):
	'''Comment themer'''

	def theme(self, obj, format, view_mode, args):
		
		obj.css.append('i-margin-small')
		
		if args['context'].request.ajax:
			super().theme(obj, format, view_mode, args)


	def theme_process_variables(self, obj, format, view_mode, args):

		if args['context'].request.ajax:

			#container = IN.entitier.load_single('CommentContainer', obj.container_id)
			# add comment sub list
			data = {
				'level' : obj.level + 1,
				'parent_id' : obj.id,
				'container_id' : obj.container_id,
				'parent_entity_type' : obj.parent_entity_type,
				'parent_entity_id' : obj.parent_entity_id
			}
			# lazy args
			data['lazy_args'] = {
				'load_args' : {
					'data' : {
						'level' : obj.level + 1,
						'parent_id' : obj.id,
						'container_id' : obj.container_id,
						'parent_entity_type' : obj.parent_entity_type,
						'parent_entity_id' : obj.parent_entity_id
					}
				}
			}
			
			sub_comment_list = Object.new(type = 'CommentListLazy', data = data)
			
			args['sub_comment_list'] = IN.themer.theme(sub_comment_list)

		super().theme_process_variables(obj, format, view_mode, args)
		
		#nabar = args['context'].nabar
		
		nabar = IN.entitier.load('Nabar', obj.nabar_id)
		
		args['nabar_name'] = nabar.name
		args['nabar_id'] = nabar.id
		args['nabar_picture'] = IN.nabar.nabar_profile_picture_themed(nabar)


#@IN.register('CommentContainer', type = 'Themer')
#class CommentContainerThemer(In.themer.ObjectThemer):
	#'''CommentContainer themer'''

@IN.register('CommentListLazy', type = 'Themer')
class CommentListLazyThemer(In.core.lazy.HTMLObjectLazyThemer):
	'''lazy themer'''

