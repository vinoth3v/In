
class Vakai(In.entity.Entity):
	'''Vakai Entity class.'''
	
	def __init__(self, data = None, items = None, **args):
		
		self.weight = 0
		super().__init__(data, items, **args)

		self.css.append(self.__type__)


@IN.register('Vakai', type = 'Entitier')
class VakaiEntitier(In.entity.EntityEntitier):
	'''Base Vakai Entitier'''
	
	# Vakai needs entity insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = True
	
	parent_field_name = 'field_vakai_parent'
	title_field_name = 'field_vakai_title'
	
	def entity_context_links(self, entity, context_type):

		entitier = IN.entitier
		
		# no view access
		if not entitier.access('view', entity):
			return

		id_suffix = '-'.join((entity.__type__, str(entity.id)))

		output = super().entity_context_links(entity, context_type)
		
		if context_type == 'links':
			
			if entitier.access('edit', entity):
				
				edit = Object.new(type = 'Link', data = {
					'id' : 'edit-link-' + id_suffix,
					'css' : ['i-button i-button-small'],
					'value' : s('edit'),
					'href' : '/'.join(('/vakai', str(entity.id), 'edit')),
					'weight' : 0,
				})
				output[edit.id] = edit

			if entitier.access('delete', entity):
				delete = Object.new(type = 'Link', data = {
					'id' : 'delete-link-' + id_suffix,
					'css' : ['ajax-modal i-button i-button-small'],
					'value' : s('delete'),
					'href' : '/'.join(('/vakai', str(entity.id), 'delete', 'confirm')),
					'weight' : 1,
				})
				output[delete.id] = delete

			if entitier.access('add', entity):
				
				try:
					
					bundle = entity.type
					reply = Object.new(type = 'TextDiv', data = {
						'id' : 'add_sub-link-' + id_suffix,
						'css' : ['i-button i-button-small'],
						'value' : s('Add sub vakai'),
						'weight' : 3,
						'attributes' : {
							'data-ajax_type' : 'POST',
							'data-href' : '/vakai/add/sub/!' + '/'.join((bundle, str(entity.id))),
						},
					})
					output[reply.id] = reply
				except Exception:
					IN.logger.debug()

		return output


	def delete(self, entity, commit = True):
		'''Recursively delete coments and its sub coments'''
		
		#result = entity.Model.delete(entity, commit)
		
		# Instead of delete and its all sub vakais
		# just disable this vakai only

		try:
			db = IN.db
			connection = db.connection

			entity.Model.delete(entity, commit)
			
			cursor = db.execute('''SELECT 
				  field_vakai_parent.value
				FROM 
				  config.vakai,
				  field.field_vakai_parent				  
				WHERE
				  vakai.id = field_vakai_parent.entity_id AND
				  vakai.id = %(parent_id)s AND
				  vakai.status > 0 AND
				  field_vakai_parent.value > 0
				''', {
				'parent_id' : entity.id,
			})
			ids = []
			last_id = 0
			if cursor.rowcount >= 0:
				for row in cursor:
					# reverse reference
					ids.append(row['value'])
					
			sub_loaded = None
			if ids:
				sub_loaded = self.load_multiple(self, ids)
				
				for id, sub_entity in sub_loaded.items():
					# recursive delete
					sub_entity.Entitier.delete(sub_entity, commit)
			
			# hook invoke
			if self.invoke_entity_hook:
				IN.hook_invoke('_'.join(('entity_delete', entity.__type__, entity.type)), entity)
				IN.hook_invoke('entity_delete_' + entity.__type__, entity)

			# heavy. dont implement
			IN.hook_invoke('__entity_delete__', entity)
			
			# clear the cache
			cacher = self.cacher
			
			cacher.remove(entity.id)
			
			if self.entity_load_all:
				cacher.remove('all')
				
			if self.entity_load_all_by_bundle:
				self.cacher.remove(entity.type)
				
			return True
			
		except Exception as e:
			IN.logger.debug()
			return False
	

#-----------------------------------------------------------------------
#					Vakai Model
#-----------------------------------------------------------------------

@IN.register('Vakai', type = 'Model')
class VakaiModel(In.entity.EntityModel):
	'''Vakai Model'''
	
	not_updatable_columns = ['id', 'type', 'created']
	status_deleted = -1
	
	def delete(self, entity, commit = True):
		'''Recursively delete coments and its sub coments'''
		
		if not entity.id:
			return
		
		# Instead of delete and its all sub Vakai
		# just disable this Vakai only
		
		# TODO: sub vakai delete
		connection = IN.db.connection
		
		try:
			
			table_info = self.model['table']
			table = table_info['name']
			columns = table_info['columns']
			
			cursor = IN.db.update({
				'table' : table,
				'set' : [['status', self.status_deleted]],
				'where' : ['id', int(entity.id)]
			}).execute()
			
			if commit: # if caller will not handle the commit
				connection.commit()

		except Exception as e:
			if commit:
				connection.rollback()
			IN.logger.debug()
			raise e # re raise
			
		return True
	

@IN.hook
def entity_model():
	return {
		'Vakai' : {						# entity name
			'table' : {				# table
				'name' : 'vakai',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'weight' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('Vakai', type = 'Themer')
class VakaiThemer(In.entity.EntityThemer):
	'''Vakai themer'''

	def view_modes(self):
		modes = super().view_modes()
		modes.add('tag')
		return modes
		
	def theme(self, obj, format, view_mode, args):
		obj.css.append('vakai-' + str(obj.id))
		super().theme(obj, format, view_mode, args)

	def theme_process_variables(self, obj, format, view_mode, args):

		if args['context'].request.ajax:

			# add sub list
			data = {
				'lazy_args' : {
					'load_args' : {
						'data' : {
							'parent_entity_type' : obj.__type__, # always should be Vakai
							'parent_entity_bundle' : obj.type,
							'parent_entity_id' : obj.id, # parent
						},
					},
				},
				'parent_entity_type' : obj.__type__, # always should be Vakai
				'parent_entity_bundle' : obj.type,
				'parent_entity_id' : obj.id, # parent
			}
			
			sub_list = Object.new(type = 'VakaiListLazy', data = data)
			
			args['sub_list'] = IN.themer.theme(sub_list)

		super().theme_process_variables(obj, format, view_mode, args)
		
		##nabar = args['context'].nabar
		#if obj.nabar_id:
			#nabar = IN.entitier.load('Nabar', obj.nabar_id)
		
			#args['nabar_name'] = nabar.name
			#args['nabar_id'] = nabar.id
			#args['nabar_picture'] = IN.nabar.nabar_profile_picture_themed(nabar)


