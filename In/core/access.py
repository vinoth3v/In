


class Access:
	'''base IN Access controller'''

	def __init__(self):
		
		self.admin_role_id = IN.APP.config.admin_role_id

		self.build_role_access()
		
	def build_role_access(self):
		
		# reset
		self.roles = {}
		self.role_access = {}

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
				try:
					self.role_access[role_id].append(key)
				except KeyError:
					self.role_access[role_id] = [key]
			
	def __call__(self, key, account):
		'''return true if account has access key

		if IN.access('view_content', account):
			do something
		
		TODO: cache?		
		'''
		
		try:

			roles = account.roles
			
			if self.admin_role_id in roles:
				# unconditional admin access
				return True

			role_access = self.role_access
			for role_id in roles: # always reverse sorted by weight ?
				if role_id in role_access and key in role_access[role_id]:
					return True
					
			return False
			
		except Exception as e:
			IN.logger.debug()

		return False
		
