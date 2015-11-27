import json
import datetime

import base64
import hashlib
from functools import *
from collections import defaultdict, OrderedDict

class AccountAuth:
	
	
	hasher = In.core.util.DrupalHash()
	
	NABAR_STATUS_ACTIVE = 1
	NABAR_STATUS_BLOCKED = -10
	NABAR_STATUS_REGISTERED = -5
	
	def __init__(self):
		'''init nabar controller'''
		
		config = IN.APP.config
		self.admin_role_id = config.admin_role_id
		self.anonymous_role_id = config.anonymous_role_id
		self.not_confirmed_role_id = config.not_confirmed_role_id
		self.confirmed_role_id = config.confirmed_role_id
		
		# moved to core.access
		#self.build_access_roles()
		
		#self.cached_method = lru_cache(maxsize=16)(self.cached_method)
		
	def build_access_roles(self):
		
		# reset
		self.roles = OrderedDict()
		self.access_keys = RDict()
		self.access_roles = defaultdict(set)

		keys = IN.hook_invoke('access_keys')
		for key in keys:
			if key:
				self.access_keys.update(key)
		# access_keys_alter
		IN.hook_invoke('access_keys_alter', self.access_keys)

		self.access_keys = OrderedDict(sorted(self.access_keys.items(), key = lambda o:o[0]))
		
		# role
		cursor = IN.db.execute('''SELECT * 
				FROM account.role
				ORDER BY weight''')

		if cursor.rowcount > 0:
			for row in cursor:
				self.roles[row['id']] = {
					'id' : row['id'],
					'name' : row['name'],
					'weight' : int(row['weight']),
					'info' : row['info']
				}

		# access
		# can we use pgsql AGGREGATE here?
		'''
		CREATE AGGREGATE array_accum (anyelement)
		(
			sfunc = array_append,
			stype = anyarray,
			initcond = '{}'
		);

		SELECT col1, array_accum(col2)
		 GROUP BY  col1

		'''
		
		cursor = IN.db.execute('''SELECT * FROM account.access''')
		if cursor.rowcount > 0:
			for row in cursor:
				role_id = row['role_id']
				key = row['access']
				self.access_roles[key].add(role_id) # default dict


	def access(self, key, account):
		'''return true if account has access key


		if IN.nabar.access('view_content', account):
			do something
		
		TODO: cache?		
		'''
		
		try:

			roles = account.roles
			
			if not roles:
				roles = {self.anonymous_role_id} # anonymous # set
			
			if self.admin_role_id in roles:
				# unconditional admin access
				return True

			if key not in self.access_roles:
				return False
			
			access_roles = self.access_roles[key]
			
			if roles & access_roles: # & common in both
				return True

			return False
			
		except Exception as e:
			IN.logger.debug()

		return False
	
	def match_password(self, nabar_id, password):
		try:
			
			# password auth
			hashes = IN.entitier.select('NabarHash', [['nabar_id', nabar_id]])

			if not hashes: # None or empty
				return None
			
			# multiple passwords
			for hid, hash in hashes.items():
				old_hash = hash.hash
				new_hash = self.hasher.password_crypt('sha512', password, old_hash)
				if old_hash == new_hash:
					return hash
			
			return None
			
		except Exception as e:
			IN.logger.debug()
			
		return None
		
	#def auth_loginname_password(self, loginname, password):
		#try:
			
			## nabar name auth // and a.status >= 1
			#cursor = IN.db.execute('''select l.nabar_id
				#FROM account.login l
				#JOIN account.nabar n ON l.nabar_id = n.id
				#where l.status = 1 AND
				#l.value = %(loginname)s
				#LIMIT 1''', {
				#'loginname' : loginname
			#})
			
			#if cursor.rowcount != 1:
				#return False
			#data = cursor.fetchone()

			## password auth
			#hashes = IN.entitier.select('NabarHash', [['nabar_id', data['nabar_id']], ['status', 1]])

			#if not hashes: # None or empty
				#return False

			#for hid, hash in hashes.items():
				#old_hash = hash.hash
				#new_hash = self.hasher.password_crypt('sha512', password, old_hash)
				#if old_hash == new_hash: # success
					#return data['nabar_id']
		#except Exception as e:
			#IN.logger.debug()

		#return False

	def auth_cookie(self, context):

		cookie = context.request.cookie

		# get cookie uid
		uid = cookie.get('UID')

		if not uid:
			return False

		# get cookie hash
		ohash = cookie.get('HASH')

		if not ohash:
			return False

		rhash = ''
		orhash = cookie.get('RHASH', None)

		agent = context.environ['HTTP_USER_AGENT']

		# REMOTE_ADDR will be changed

		newhash = self.__simple_hash__(self.__get_cookie__key(uid, context))

		if orhash is not None:
			newrhash = self.__simple_hash__(ohash)
			if ohash == newhash and orhash == newrhash:
				return int(uid)
		else:
			if ohash == newhash: # valid nabar is logged in
				return int(uid)
		
		# not valid
		context.cookie.clear('UID')
		context.cookie.clear('HASH')
		context.cookie.clear('RHASH')

		return False

	def login(self, nabar_id, rememberme = False):

		context = IN.context
		
		#nabars = IN.entitier.select('Nabar', [['id', nabar_id], ['status', 1]])

		## TODO: additional validations

		#if not nabars: # None or empty
			#return False

		#nabar = next(iter(nabars.values()))
		
		nabar = IN.entitier.load_single('Nabar', nabar_id)
		
		if not nabar:
			return False
		
		nabar_id = str(nabar.id)
		
		hash = self.__simple_hash__(self.__get_cookie__key(nabar_id, context))

		# todo: set cookie
		if not rememberme:
			context.cookie.set('HASH', hash)
			context.cookie.set('UID', nabar_id)
		else:
			remdays = IN.APP.config.cookie_remember_me_days

			context.cookie.set('HASH', hash, expires_days = remdays)
			context.cookie.set('UID', nabar_id, expires_days = remdays)

			remhash = self.__simple_hash__(hash)
			# set rem cookie
			context.cookie.set('RHASH', remhash, expires_days = remdays)

	def logout(self, context, action = None, **args):

		clear = context.cookie.clear
		clear('UID')
		clear('HASH')
		clear('RHASH')

		context.nabar = self.anonymous()

		context.redirect(IN.APP.config.logout_path)

	def __simple_hash__(self, key):
		h = 5
		for i in key:
			h ^= ord(i)
			h ^= h >> 16;
			h *= 0x85ebca6b; h ^= h >> 13;
			h *= 0xc2b2ae35; h ^= h >> 16;

		h = str(h).encode('utf-8')
		return hashlib.sha512(h).hexdigest()

	def __get_cookie__key(self, nabar_id, context):
		# REMOTE_ADDR will be changed

		agent = context.environ['HTTP_USER_AGENT']

		return '|'.join(('N', str(nabar_id), agent, IN.APP.config.cookie_secret))
	
	def get_active_nabar_id_by_email(self, email):
		
		try:
			cursor = IN.db.execute('''select l.nabar_id
				FROM account.login l
				JOIN account.nabar a ON l.nabar_id = a.id
				where a.status = 1  AND
				l.type = %(type)s and l.status = 1 AND
				l.value = %(email)s
				LIMIT 1''', {
				'type' : 'email',
				'email' : email,
			})

			if cursor.rowcount == 0:
				return
				
			nabar_id = cursor.fetchone()['nabar_id']
				
			return nabar_id
				
		except Exception as e:
			IN.logger.debug()
		
					
	def register(self, email, password, name, gender, dob, roles = None):

		if not name or not email or not gender or not password or not dob:
			# raise error
			return False
		
		if not roles: # default to not confirmed
			roles = [self.not_confirmed_role_id]
		

		# email already exists?
		try:
			
			nabar_id = self.get_active_nabar_id_by_email(email)
			
			if nabar_id:
				return False
			
			# transactions are per connection based
			# with: not useful as it ignores some errors

			connection = IN.db.connection

			now = datetime.datetime.now()

			if type(gender) is str:
				gender = {'female' : 0,  'male' : 1, 'shemale' : 2}[gender] # throw error

			# insert nabar and get nabar id
			nabar_id = In.nabar.Nabar({
				'id' : None,		# new nabar
				'name' : name,		# display name
				'gender' : gender,
				'dob' : dob,
				'created' : now,
				'status' : IN.nabar.NABAR_STATUS_REGISTERED, 		# disabled by default
				'roles' : roles,
				'data' : {
					'primary_email' : email
				},
			}).insert(False)


			if not nabar_id:
				raise In.nabar.AccountCreateException('Cannot insert into account')
			
			nabar = IN.entitier.load_single('Nabar', nabar_id)
			
			# update the nabar_id and nabar cache
			nabar.nabar_id = nabar_id
			nabar.save()
			
			# update nabar_id to nabar
			#IN.db.update({
				#'table' : 'account.nabar',
				#'set' : [['nabar_id', nabar_id]],
				#'where' : [['id', nabar_id]]
			#}).execute()
			
			# create nabar login
			login_id = In.nabar.NabarLogin({
				'id' : None,				# new login
				'nabar_id' : nabar_id,
				'value' : email,
				'type' : 'email',
				'created' : now,
				'status' : IN.nabar.NABAR_STATUS_REGISTERED, 				# disabled by default
			}).insert(False)

			# create password hash
			hash_id = In.nabar.NabarHash({
				'id' : None,				# new password
				'nabar_id' : nabar_id,
				'hash' : self.hasher.hash(password),
				'hint' : ''.join((password[0], '|', password[-1:])),
				'type' : '$S$',
				'created' : now,
				'status' : IN.nabar.NABAR_STATUS_REGISTERED, 				# disabled by default
			}).insert(False)

			# create nabar profile
			# no thing

			# create email token
			#agent = IN.context.environ['HTTP_USER_AGENT']

			token = In.core.token_verification.create_random_token()
			
			# token data
			data = {
				'nabar_id' : nabar_id,
				'email' : email,
			}

			data = json.dumps(data, skipkeys = True, ensure_ascii = False)

			cursor = IN.db.execute('''INSERT INTO log.token
					(token, type, created, expire, data)
			VALUES  (%(token)s, %(type)s, %(created)s, %(expire)s, %(data)s)''', {
				'token' : token,
				'type' : 'register',
				'created' : now,
				'expire' : now + datetime.timedelta(days = 30), # nabar register token, 1 month
				'data' : data,
			})
			# nabar created
			# commit the changes
			connection.commit()

			# send mail
			
			EMail.new('WelcomeEmailVerification', {
				'title' : s('Verify your email!'),
				'to_name' : name,
				'to_address' : email,
				'mail_verify_token' : token,
			}).send()
			
			return nabar_id

		except Exception as e:
			connection.rollback()
			# PG INCREASES SERIALS EVEN ON ROLLBACK
			IN.logger.debug()
			raise e # re raise
			
	def send_recovery_email(self, nabar_id, email = None):
		
		nabar = IN.entitier.load_single('Nabar', nabar_id)
		if not nabar:
			raise In.nabar.AccountException(s('Invalid Nabar!'))
		
		if nabar.status == self.NABAR_STATUS_BLOCKED:
			raise In.nabar.AccountException(s('This nabar is Blocked!'))
		
		if email is None:
			email = nabar.email_address
		
		try:
			token = In.core.token_verification.create_random_token()
			
			now = datetime.datetime.now()
			
			# token data
			data = {
				'nabar_id' : nabar_id,
				'email' : email,
			}

			data = json.dumps(data, skipkeys = True, ensure_ascii = False)

			cursor = IN.db.execute('''INSERT INTO log.token
					(token, type, created, expire, data)
			VALUES  (%(token)s, %(type)s, %(created)s, %(expire)s, %(data)s)''', {
				'token' : token,
				'type' : 'recovery',
				'created' : now,
				'expire' : now + datetime.timedelta(days = 30), # nabar register token, 1 month
				'data' : data,
			})
			# nabar created
			# commit the changes
			IN.db.connection.commit()

			# send mail
			
			EMail.new('AccountRecoveryEmail', {
				'title' : s('Account Recovery e-mail!'),
				'to_name' : nabar.name,
				'to_address' : email,
				'mail_verify_token' : token,
			}).send()
			
		except Exception as e:
			IN.logger.debug()
			raise e
	
	
	def nabar_recovery_token_verification(self, context, data):
		'''Recovery'''
		
		nabar_id = data['nabar_id']
		email = data['email']

		db = IN.db
		
		if not nabar_id or not email:
			context.bad_request()

		try:

			# check email should be active
			cursor = db.execute('''select l.nabar_id
				FROM account.login l
				JOIN account.nabar a ON l.nabar_id = a.id
				where l.value = %(email)s AND
					l.type = %(type)s AND
					l.status >= 1 AND 
					a.status >= 1 AND
					a.nabar_id = %(nabar_id)s''', {
				'email' : email,
				'type' : 'email',
				'nabar_id' : nabar_id,
			})
			if cursor.rowcount == 0:
				context.bad_request()
			
			# activate nabar, set role to confirmed
			nabar = IN.entitier.load_single('Nabar', nabar_id)
			
			if not nabar:
				context.bad_request()
			
			# nabar is not active yet
			if nabar.status == IN.nabar.NABAR_STATUS_REGISTERED:
				context.bad_request()
			
			# nabar blocked
			if nabar.status == IN.nabar.NABAR_STATUS_BLOCKED:
				context.bad_request()
			
			# add recover change password form
			
			email_token = context.request.path_parts[3]
			email_token = email_token[1:]
			
			form = IN.former.load('RecoverChangePassword', args = {
				'data' : {'id' : '-'.join(('RecoverChangePassword', str(nabar.id)))},
				'nabar_id' : nabar.id,
				'email' : email,
				'email_token' : email_token,
			})
			
			context.response.output.add(form)
			
			return True
		except Exception as e:
			IN.logger.debug()
			

	def nabar_register_token_verification(self, context, data):
		
		nabar_id = data['nabar_id']
		email = data['email']

		db = IN.db
		
		if not nabar_id or not email:
			context.bad_request()

		try:

			# check email not activated before 
			# it may be active with another nabar_id
			cursor = db.execute('''select l.nabar_id
				FROM account.login l
				JOIN account.nabar a ON l.nabar_id = a.id
				where l.value = %(email)s AND
					l.type = %(type)s AND
					l.status >= 1 and a.status >= 1''', {
				'email' : email,
				'type' : 'email'
			})
			if cursor.rowcount > 0:
				context.bad_request()

			# activate nabar, set role to confirmed
			nabar = IN.entitier.load_single('Nabar', nabar_id)
			
			if not nabar:
				context.bad_request()
			
			if nabar.status != IN.nabar.NABAR_STATUS_REGISTERED:
				context.bad_request()
				
			nabar.status = 1
			
			# set role
			nabar.roles.remove(self.not_confirmed_role_id)
			nabar.roles.add(self.confirmed_role_id)
			
			nabar.save()
			
			# activate nabar login
			logins = IN.entitier.select('NabarLogin', [
				['nabar_id', nabar_id],
				['status', IN.nabar.NABAR_STATUS_REGISTERED]
			])
			
			if not logins:
				context.bad_request()
			
			for login_id, login in logins.items():
				login.status = 1
				login.save()
			
			# activate nahar hash
			hashes = IN.entitier.select('NabarHash', [
				['nabar_id', nabar_id],
				['status', IN.nabar.NABAR_STATUS_REGISTERED]
			])
				
			if not hashes:
				context.bad_request()
			
			for hash_id, hash in hashes.items():
				hash.status = 1
				hash.save()
			
			
			db.connection.commit()
			
			# hook invoke
			IN.hook_invoke('nabar_registration_verified', nabar_id)

			# show message
			# redirect
			context.response.output.add('TextDiv', {'value' : IN.APP.config.nabar_verified_message})

			return True
		except Exception as e:
			IN.logger.debug()
			db.connection.rollback()

	
	def anonymous(self):
		'''returns anonymous nabar'''
		nabar = In.nabar.nabar.Nabar()
		nabar.id = 0
		nabar.name = 'guest'
		nabar.gender = 0
		nabar.dob = datetime.datetime.now()
		nabar.roles = {self.anonymous_role_id}
		return nabar


	def nabar_profile_picture(self, nabar, profile_bundle = 'image', field = 'field_avator'):
		'''returns the public uri of nabar picture'''
		# TODO: Cache it
		config = IN.APP.config.nabar_default_profile_picture_path
		
		try:
			
			profiles = In.profile.nabar_profile(nabar.id, profile_bundle)
			
			if profiles:
				profile = next(iter(profiles.values()))
				
				file_id = profile[field].value[''][0]['value']
			
				if file_id:
				
					file = IN.entitier.load_single('File', file_id)
					
					if file:
						return file.path
						
		except Exception as e:
			IN.logger.debug()
			
		return config[nabar.gender]
		
		
	def nabar_profile_picture_uri(self, nabar, profile_bundle = 'image', field = 'field_avator', style = 'xsmall'):
		'''returns the public uri of nabar picture'''
		# TODO: Cache it
		
		path = self.nabar_profile_picture(nabar, profile_bundle, field)
		if path:
			return ''.join(('/files/public/style/', style, '/', path))
		else:
			return ''
		
	def nabar_profile_picture_themed(self, nabar, style = 'xsmall'):
		
		pic_obj = Object.new('NabarPicture', {
			'nabar' : nabar, 
			'style' : style,
			'css' : ['nabar-picture i-float-left i-width i-margin-small-right']
		})
		
		pic_themed = IN.themer.theme(pic_obj)
		
		return pic_themed
	
