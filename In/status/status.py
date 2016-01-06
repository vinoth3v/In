
#import In.entity

class Status(In.entity.Entity):
	'''Status Entity class.
	'''
	
	def __init__(self, data = None, items = None, **args):

		# default
		
		self.featured = False
		
		# includes comments and add form
		self.__include_comment_boxes__ = False
		
		super().__init__(data, items, **args)


@IN.register('Status', type = 'Entitier')
class StatusEntitier(In.entity.EntityEntitier):
	'''Base Status Entitier'''

	# Status needs entity insert/update/delete hooks
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
					'href' : '/'.join(('/status', str(entity.id), 'edit')),
					'weight' : 0,
					'attributes' : {
						'data-ajax_type' : 'POST',
					}
				})
				output[edit.id] = edit

			if entitier.access('delete', entity):
				delete = Object.new(type = 'Link', data = {
					'id' : 'delete-link-' + id_suffix,
					'css' : ['no-ajax ajax-modal i-button i-button-small i-float-right'], # no-ajax needed here or it bind twice
					'value' : s('delete'),
					'href' : '/'.join(('/status', str(entity.id), 'delete', 'confirm')),
					'weight' : 1,
					'attributes' : {
						'data-ajax_type' : 'POST',
					}
				})
				output[delete.id] = delete

			
		return output
	
	def entity_title(self, entity):

		title_field_name = 'field_status_body'
		
		if title_field_name in entity:
			try:
				title = entity[title_field_name].value[''][0]['value']				
				return texter.format(title, 'tinyteaser')				
			except Exception as e:
				IN.logger.debug()
		
		return ': '.join((entity.__type__, str(entity.id)))
		
@IN.register('Status', type = 'Model')
class StatusModel(In.entity.EntityModel):
	'''Status Model'''


@IN.hook
def entity_model():
	return {
		'Status' : {						# entity name
			'table' : {				# table
				'name' : 'status',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'to_entity_type' : {},
					'to_entity_id' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('Status', type = 'Themer')
class StatusThemer(In.entity.EntityThemer):
	'''Status themer'''


	def theme(self, obj, format, view_mode, args):
		super().theme(obj, format, view_mode, args)
		
		obj.css.append(obj.__type__)
		obj.css.append('i-margin-bottom')
		

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		
		entitier = IN.entitier
		
		nabar = entitier.load('Nabar', obj.nabar_id)
		
		args['nabar_name'] = nabar.name
		args['nabar_id'] = nabar.id
		args['nabar_picture'] = IN.nabar.nabar_profile_picture_themed(nabar)

		args['box_comments'] = ''
		args['box_comments_form'] = ''
		
		#if obj.__include_comment_boxes__:
		# add comment box and add form
		
		container_id = IN.commenter.get_container_id(obj)
		entity_type = 'Status'
		entity = obj
		
		args['to_entity'] = '' 
		
		if obj.to_entity_type == 'Nabar' and obj.to_entity_id != obj.nabar_id:
			to_nabar = entitier.load('Nabar', obj.to_entity_id)
			args['to_entity'] = ''.join(('<i class="i-icon-angle-double-right"></i> <a href="/nabar/', str(to_nabar.id), '">', to_nabar.name, '</a>'))
			
		if container_id:
			
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

			comments_box = Object.new('BoxEntityComments', data)

			data['weight'] = 11
			comments_form = Object.new('BoxEntityCommentAddForm', data)
			
			args['box_comments'] = IN.themer.theme(comments_box)
			args['box_comments_form'] = IN.themer.theme(comments_form) 

		
