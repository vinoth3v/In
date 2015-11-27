
import datetime

class FlagButtonForm(Form):
	'''FlagButtonForm'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		flagger = IN.flagger
		entitier = IN.entitier
		nabar = IN.context.nabar
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		entity_id = args['entity_id']
		
		entity = entitier.load_single(entity_type, entity_id)
		
		self.entity = entity
		
		try:
			flag_types = flagger.enabled_flag_type[entity_type][entity_bundle]
		except KeyError as e:
			return # no flag enabled for this entity
		
		for flag_type_entity in flag_types:
			
			flag_entity = flagger.flag(flag_type_entity.type, entity, nabar)
			
			flag_status = flag_type_entity.data.get('flag_status', [])
			if not flag_status:
				continue
			
			current_status = None
			if flag_entity:
				current_status = flag_entity.flag_status
			
			
			key, text = flagger.get_next_flag_key_title(flag_status, current_status)
			
			if not key:
				continue
			
			# TODO: access check
			if not flagger.access(entity, nabar, flag_type_entity, key):
				continue
				
			count_by_statuses = flag_type_entity.data.get('count_by_statuses')
			if count_by_statuses:
				count = flagger.flag_count(flag_type_entity.type, entity, count_by_statuses)
			else:
				count = 0
			if not count:
				count = ''
			text = s(text, {'count': str(count)})
			
			
			button_id = '-'.join(('flag_button', entity_type, str(entity_id), flag_type_entity.type, str(flag_type_entity.id)))
			self.add('Button', {
				'id' : button_id,
				'name' : '-'.join((flag_type_entity.type, str(flag_type_entity.id))),
				'value' : text,
				'css' : [
					'ajax',
					'i-button i-button-small',
					'flag-button flag-type-' + flag_type_entity.type,
					'-'.join(('flag', flag_type_entity.type, key))
				],
				'attributes' : {'data-ajax_partial' : 1},
			})
			
			self.ajax_elements.append(button_id)
			
		# all ajax
		self.css.append('i-float-left')

@IN.register('FlagButtonForm', type = 'Former')
class FlagButtonFormFormer(FormFormer):
	'''FlagButtonForm Former'''
	
	#def validate(self, form, post):
		
		#if form.has_errors:
			#return
	
	def submit_prepare_partial(self, form, post):
		
		super().submit_prepare_partial(form, post)
		
		if form.has_errors:
			return
		
		element_id = post['element_id']
		
		element_id = element_id.split('-')
		if len(element_id) == 5:
			flag_type = element_id[3]
			flag_type_entity_id = element_id[4]
			
			if not flag_type_entity_id.isnumeric():
				
				return
		else:
			
			return
		
		flag_type_entity_id = int(flag_type_entity_id)
		
		flagger = IN.flagger
		entitier = IN.entitier
		nabar = IN.context.nabar
		
		args = form.args
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		
		entity = form.entity		
		entity_id = entity.id
		
		try:
			# get flag types
			flag_types = flagger.enabled_flag_type[entity_type][entity_bundle]
		except KeyError as e:
			# no flag enabled for this entity
			context.response = In.core.response.EmptyResponse()
			return
		
		for flag_type_entity in flag_types:
			
			# not this flag type
			
			if flag_type != flag_type_entity.type or flag_type_entity_id != flag_type_entity.id:
				continue
			
			flag_entity = flagger.flag(flag_type_entity.type, entity, nabar)
			
			flag_status = flag_type_entity.data.get('flag_status', [])
			if not flag_status:
				
				break
			
			current_status = None
			if flag_entity:
				current_status = flag_entity.flag_status
			
			new_status, new_status_text = flagger.get_next_flag_key_title(flag_status, current_status)
			
			# invalid
			if not new_status:
				
				break
			
			if not flagger.access(entity, nabar, flag_type_entity, new_status):
				
				break
			
			try:
				
				# get flag entity
				flag_entity = flagger.flag(flag_type_entity.type, entity, nabar)
				
				new_status, new_status_text = flagger.get_next_flag_key_title(flag_status, current_status)
				
				if flag_entity is None:
					# create
					data = {
						'type' : flag_type,
						'status' : 1,
						'flag_status' : new_status,
						'nabar_id' : nabar.nabar_id,
						'actor_entity_type' : nabar.__type__,
						'actor_entity_id' : nabar.id,
						'target_entity_type' : entity_type,
						'target_entity_id' : entity.id,
					}
				
					flag_entity = Entity.new('Flag', data)
				
				else:
					# update new status
					flag_entity.flag_status = new_status
					
				form.processed_data['flag_entity'] = flag_entity
				form.processed_data['flag_type_entity'] = flag_type_entity
				form.processed_data['new_status'] = new_status
				form.processed_data['new_status_text'] = new_status_text
				form.processed_data['flag_type_entity_id'] = flag_type_entity_id
				
				return
				
			except:
				IN.logger.debug()
		
		
		form.has_errors = True
		form.error_message = 'unknown error'
		
	def submit_partial(self, form, post):
		
		super().submit_partial(form, post)
		
		if form.has_errors:
			return
		
		flagger = IN.flagger
		
		args = form.args
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		
		entity = form.entity		
		entity_id = entity.id
		
		flag_entity = form.processed_data['flag_entity']
		flag_type_entity = form.processed_data['flag_type_entity']
		new_status = form.processed_data['new_status']
		new_status_text = form.processed_data['new_status_text']
		flag_type_entity_id = form.processed_data['flag_type_entity_id']
		
		
		# get new status and output
		# id flag_link-Comment-comment_page-like

		try:
			
			flag_entity.changed =  datetime.datetime.now()
			flag_entity.save()
			
			key, text = flagger.get_next_flag_key_title(flag_type_entity.data['flag_status'], new_status)
			
			button_id = '-'.join(('flag_button', entity_type, str(entity_id), flag_type_entity.type, str(flag_type_entity.id)))
			
			button_id = '-'.join(('flag_button', entity_type, str(entity_id), flag_type_entity.type, str(flag_type_entity.id)))
			
			count_by_statuses = flag_type_entity.data.get('count_by_statuses')
			if count_by_statuses:
				count = flagger.flag_count(flag_type_entity.type, entity, count_by_statuses)
			else:
				count = 0
				
			if not count:
				count = ''
			text = s(text, {'count': str(count)})
			# re add the button
			form.add('Button', {
				'id' : button_id,
				'name' : '-'.join((flag_type_entity.type, str(flag_type_entity_id))),
				'value' : text,
				'css' : [
					'ajax',
					'i-button i-button-small',
					'flag-button flag-' + flag_type_entity.type,
					'-'.join(('flag', flag_type_entity.type, key))
				],
				'attributes' : {'data-ajax_partial' : 1},
			})
			
			return
			
		except:
			IN.logger.debug()
		

@IN.register('FlagButtonForm', type = 'Themer')
class FlagButtonFormThemer(FormThemer):

	def theme(self, obj, format, view_mode, args):
		super().theme(obj, format, view_mode, args)

		obj.css.remove('i-panel i-panel-box')
