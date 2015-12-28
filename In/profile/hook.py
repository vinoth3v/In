import os
import datetime

@IN.hook
def page_menu_tab_nabar___edit_anything_after(context):
	
	tab = context.page_menu_tab
	request = context.request
	path_parts = context.request.path_parts
	
	if path_parts[1].isnumeric():

		last = path_parts[3]
		entity_id = path_parts[1]
		
		li = tab.add('Li', {
			'css' : ['i-active' if last == 'profile' else '']
		}).add('Link', {
			'href' : ''.join(('/nabar/', entity_id, '/edit/profile/!general')),
			'value' : s('Profile'),
		})
		
@IN.hook
def entity_insert_Profile_general(entity):
	update_nabar_info(entity)

@IN.hook
def entity_update_Profile_general(entity):
	update_nabar_info(entity)


def update_nabar_info(entity):
	
	try:
		
		nabar = IN.entitier.load_single('Nabar', entity.nabar_id)
		
		if not nabar:
			return
		
		changed = False
		
		name = None
		
		# use nic if available
		try:
			name = entity['field_nickname'].value[''][0]['value'].strip()
		except Exception as e1:
			IN.logger.debug()
		
		# use name 
		try:
			if not name:
				name = entity['field_name'].value[''][0]['value'].strip()
		except Exception as e1:
			IN.logger.debug()
			
		if name:
			texter = IN.texter
			
			name_plain = texter.format(name, 'nochange')
			
			if name_plain and name_plain != nabar.name:
				nabar.name = name_plain
			
			changed = True
			
		try:
			dob = entity['field_dob'].value[''][0]['value']
			if dob != nabar.dob:
				nabar.dob = dob
				
				changed = True
		except Exception as e2:
			IN.logger.debug()
			
		try:
			gender = entity['field_gender'].value[''][0]['value']
			if gender != nabar.gender:
				nabar.gender = gender
				
				changed = True
		except Exception as e3:
			IN.logger.debug()
			
		if changed:
			nabar.save()
		
	except Exception as e:
		IN.logger.debug()
	
	
@IN.hook
def entity_load_Nabar(nabar):
	
	config = IN.APP.config.nabar_default_profile_picture_path
	
	field = 'field_avator'
	profile_bundle = 'image'
	
	try:
		
		profiles = In.profile.nabar_profile(nabar.id, profile_bundle)
		
		if profiles:
			profile = next(iter(profiles.values()))
			
			file_id = profile[field].value[''][0]['value']
			
			if file_id:
				
				file = IN.entitier.load_single('File', file_id)
				
				if file and os.path.exists('/'.join((IN.APP.config.public_file_dir, file.path))):
					nabar.picture = file.path
					
					return
					
	except Exception as e:
		IN.logger.debug()
	
	nabar.picture = config[nabar.gender]


	
@IN.hook
def entity_insert_Profile_image(entity):
	
	cacher = IN.cacher.cachers['entity_Nabar']
	cacher.remove(entity.nabar_id)

@IN.hook
def entity_update_Profile_image(entity):
	
	cacher = IN.cacher.cachers['entity_Nabar']
	cacher.remove(entity.nabar_id)


@IN.hook
def nabar_registration_verified(nabar_id):
	'''Create a general Profile for this verified account'''
	
	try:
		
		# return if profile already exists, Incase
		
		cursor = IN.db.select({
			'table' : 'entity.profile',
			'columns' : ['id'],
			'where' : [
				['nabar_id', nabar_id],
				['type', 'general']
			]
		}).execute()
		
		if cursor.rowcount > 0:
			return
			
		# check nabar exists
		cursor = IN.db.select({
			'table' : 'account.nabar',
			'columns' : ['name', 'dob', 'gender'],
			'where' : [
				['nabar_id', nabar_id]
			]
		}).execute()
		
		if cursor.rowcount == 0:
			return
			
		row = cursor.fetchone()
		
		profile = Entity.new('Profile', {
			'id' : None,
			'nabar_id' : nabar_id,
			'type' : 'general',
			'created' : datetime.datetime.now(),
			'status' : 1
		})
		
		profile['field_name'].value = {
			'' : {
				0 : {
					'value' : row['name'],
				}
			}
		}
		profile['field_nickname'].value = {
			'' : {
				0 : {
					'value' : row['name'],
				}
			}
		}
		profile['field_dob'].value = {
			'' : {
				0 : {
					'value' : row['dob'],
				}
			}
		}
		profile['field_gender'].value = {
			'' : {
				0 : {
					'value' : row['gender'],
				}
			}
		}
		
		profile.insert()
		
	except Exception as e:
		IN.logger.debug()
	
	