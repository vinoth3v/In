from collections import defaultdict
import datetime


class Flagger:
	'''Flag manager'''
	
	def __init__(self):
		''''''
		
		self.enabled_flag_type = {}
		self.flag_types = {}
		
		self.build_enabled_flag_type()
		
	def build_enabled_flag_type(self):
		
		entitier = IN.entitier
		
		types = IN.entitier.load_all('FlagType')
		
		self.flag_types = types
		
		if types is None:
			return
		
		for id, flag_type in types.items():
			data = flag_type.data
			entity_bundle = data.get('entity_bundle', {})
			
			for entity_type, entity_bundles in entity_bundle.items():
				if entity_type not in self.enabled_flag_type:
					self.enabled_flag_type[entity_type] = defaultdict(list)
				
				if '*' in entity_bundles:
					# add all
					if entity_type not in entitier.entity_bundle:
						del self.enabled_flag_type[entity_type]
						break
					for bundle in entitier.entity_bundle[entity_type].keys():
						self.enabled_flag_type[entity_type][bundle].append(flag_type)
				else:
					for bundle in entity_bundles:
						self.enabled_flag_type[entity_type][bundle].append(flag_type)
					
		
	def flag(self, flag_type, entity, actor, flag_status = None):
		'''Get/Create/Update flag'''
		
		if isinstance(flag_type, Object):
			flag_type = flag_type.type
			
		try:
			
			# Existing flag check
			flags = IN.entitier.select('Flag', [
				['type', flag_type],
				#['nabar_id', actor.nabar_id], 			# no need for nabar.id
				['target_entity_type', entity.__type__],
				['target_entity_id', entity.id],
				['actor_entity_type', actor.__type__],
				['actor_entity_id', actor.id],			
			])
			
			if flags:
				flag_entity = next(iter(flags.values()))
			else:
				flag_entity = None
			
			if flag_status is None:
				# get request
				return flag_entity
			
			# create or update
			
			if flag_entity is None:
				# create
				data = {
					'type' : flag_type,
					'status' : 1,
					'flag_status' : flag_status,
					'nabar_id' : actor.nabar_id,
					'actor_entity_type' : actor.__type__,
					'actor_entity_id' : actor.id,
					'target_entity_type' : entity.__type__,
					'target_entity_id' : entity.id,
					'changed' : datetime.datetime.now()
				}
			
				flag_entity = Entity.new('Flag', data)
			
			else:
				# update
				flag_entity.flag_status = flag_status
				flag_entity.changed =  datetime.datetime.now()
				
			flag_entity.save()
			
			return flag_entity
			
		except Exception as e:
			IN.logger.debug()
		
	def access(self, entity, nabar, flag_type = None, status = None):
		
		# admin all access
		if IN.nabar.access('flag', nabar):
			return True
		
		key = '_'.join(('flag', entity.__type__))
		# flag_entity_type		
		if IN.nabar.access(key, nabar):
			return True
		
		key = '_'.join((key, entity.type))
		# flag_entity_type_bundle
		if IN.nabar.access(key, nabar):
			return True
		
		
		if flag_type is None:
			return
			
		key = '_'.join((key, flag_type.type))
		# flag_entity_type_bundle_flag_type
		if IN.nabar.access(key, nabar):
			return True
		
		if status is None:
			return
		key = '_'.join((key, status))
		# flag_entity_type_bundle_flag_type_status
		if IN.nabar.access(key, nabar):
			return True
	
	def get_next_flag_key_title(self, flag_statuses, current_status = None):
		'''returns status from flag statuses depends on current status'''
		
		if not current_status:
			# show first status
			status_list = flag_statuses[0]
			
			return (status_list[0], status_list[1])
			
		
		# show next flag status
		
		nextkey = False
		for status_list in flag_statuses:
			key = status_list[0]
			if nextkey:
				text = status_list[1]
				
				return (key, text)
				
			if key == current_status:
				nextkey = True
				
		
		# use first key
		status_list = flag_statuses[0]
		
		return (status_list[0], status_list[1])
	
	def __entity_context_links__(self, entity, context_type, output, format, view_mode):
		
		entity_type = entity.__type__
		entity_bundle = entity.type
		
		try:
			flag_types = self.enabled_flag_type[entity_type][entity_bundle]
		except KeyError as e:
			# no flag enabled for this entity
			return
		
		form = IN.former.load('FlagButtonForm', args = {
			'entity_type' : entity_type,
			'entity_bundle' : entity_bundle,
			'entity_id' : entity.id,
		})
	
		o = HTMLObject({
			'css' : ['flag-buttons'],
			'weight' : -1,
		}).add(form)
		
		output[o.id] = o
	
	#def __entity_context_links__(self, entity, context_type, output, format, view_mode):
		
		#entitier = IN.entitier
		#nabar = IN.context.nabar
		#entity_type = entity.__type__
		#entity_bundle = entity.type
		
		#try:
			#flag_types = self.enabled_flag_type[entity_type][entity_bundle]
		#except KeyError as e:
			## no flag enabled for this entity
			
			#return
			
		
		#if context_type == 'links':
			
			#for flag_type_entity in flag_types:
				#enabled = False
				
				#flag_entity = self.flag(flag_type_entity.type, entity, nabar)
				
				#flag_status = flag_type_entity.data.get('flag_status', [])
				#if not flag_status:
					#continue
				
				#current_status = None
				#if flag_entity:
					#current_status = flag_entity.flag_status
				
				#key, text = self.get_next_flag_key_title(flag_status, current_status)
				
				#if not key:
					#continue
				
				## TODO: access check
				#if not self.access(entity, nabar, flag_type_entity, key):
					
					#continue
				
				#count_by_statuses = flag_type_entity.data.get('count_by_statuses', False)
				#if count_by_statuses:
					#count = self.flag_count(flag_type_entity.type, entity, count_by_statuses)
				#else:
					#count = 0
				#if not count:
					#count = ''
				#text = s(text, {'count': str(count)})
				
				#button_id = '-'.join(('flag_button', entity_type, str(entity.id), flag_type_entity.type, str(flag_type_entity.id)))
				#flag_link = Object.new(type = 'Link', data = {
					#'id' : button_id,
					#'css' : [
						#'ajax i-button i-button-small',
						#'flag-link flag-' + flag_type_entity.type,
						#'-'.join(('flag', flag_type_entity.type, key))
					#],
					#'value' : text,
					#'href' : ''.join(('/flag/flag/!', entity_type, '/', str(entity.id), '/!', flag_type_entity.type, '/!', key)),
					#'weight' : -1,
				#})
				
				#output[flag_link.id] = flag_link
				
	def flag_count(self, flag_type, entity, flag_status = None):
		'''returns total # of flags'''
	
	
		where = [
			['type', flag_type],
			['status', 1],
			['target_entity_type', entity.__type__],
			['target_entity_id', entity.id],
		]
		if flag_status:
			if type(flag_status) is str:
				where.append(['flag_status', flag_status])
			else: # list
				where.append(['flag_status', 'IN', flag_status])
			
		cursor = IN.db.select({
			'tables' : 'entity.flag',
			'columns' : ['count(*)'],
			'where' : where,
		}).execute()

		if cursor.rowcount != 1:
			return 0

		data = cursor.fetchone()
		return data[0]
		
