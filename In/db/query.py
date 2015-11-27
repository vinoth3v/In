from In.core.object_meta import ObjectMetaBase


class QueryMeta(ObjectMetaBase):

	__class_type_base_name__ = 'QueryBase'
	__class_type_name__ = 'Query'


class QueryBase(dict, metaclass = QueryMeta):
	'''Base class of all IN Query.

	'''
	__allowed_children__ = None
	__default_child__ = None
	

	def __bool__(self):
		'''always True for if obj'''
		return True

@IN.register('Query', type = 'Query')
class Query(QueryBase):
	'''Base class of all IN Query.

	'''

#class Table(Query):

	#def __init__(self, json, **args):

		#self.columns = json.get('columns', None)
		#self.name = json.get('name', None)
		#self.keys 	= json.get('keys', None)
		#self.indexes 	= json.get('indexes', None)
		#self.like 	= json.get('like', None)

		#self.values = {}

	#def sql_create(self):

		#self.values = {}

		#q = ['CREATE TABLE IF NOT EXISTS ']

		##TODO: add prefix
		#q.append(self.name)
		#if self.like:
			#q.append(' LIKE ')
			#q.append(self.like)

		#if self.columns:

			#qcols = []
			#for col, col_def in self.columns.items():
				#qcol = [col]
				#qcol.append(col_def['type'])
				#if 'length' in col_def:
					#qcol.append(''.join(('(', col_def['length'], ')')))
				#if 'default' in col_def:
					#qcol.append('DEFAULT')
					#vkey = '_' + str(len(self.values))
					#qcol.append(''.join(('%(', vkey, ')s')))
					#self.values[vkey] = col_def[default]

				#qcols.append(' '.join(qcol))


		#if self.keys:

			#qkeys = []

			#for keyname, key_def in self.keys.items():
				#qkey = []
				#qkey.append('CONSTRAINT ')
				#qkey.append('_'.join((self.name, keyname)))
				#qkey.append(key_def['type'])
				#if 'columns' in key_def:
					#qkey.append('(')
					#qkey.append(','.join(key_def['columns']))
					#qkey.append(')')

				#qkeys.append(' '.join(qkey))



		#q.append(' ( \n')
		#q.append(')\n')
		#return ''.join(q)

class Select(Query):
	'''Select Query

	q = Select({
			'columns': {'a' : ['id', 'status']},
			'columns': {'a' : [{'id': 'alias'}, {'status': 'alias'}]},
			'columns': {'id' : 'alias'},
			'columns': ['id', 'status'],
			'tables' : [['account', 'a']],
			'join' : [
				['inner join', 'table', alias, [['a.id = b.id']]],
				['inner join', 'table', alias, condition]
			],
			'where' : [
				['id', 5],
				['status', '!=', 0],
				['or', [
					[],
					[],
				]],
			],			
			'group': {'a' : ['id', 'status']},
			'group': ['id', 'status'],
			'order' : [{'id': 'asc'}, 'status']
		})
	'''

	def sql(self):
		'''returns json as select sql'''
		
		where_values = {}
		join_values = {}
		
		q = ['SELECT ']

		# COLUMNS
		if type(self.columns) is str:
			q.append(self.columns)
		else:

			if type(self.columns) is list:

				# ['col1', 'col2']
				q.append(', '.join(col for col in self.columns))

			elif type(self.columns) is dict:
				# {'tbl' : ['col', 'col']},
				# {'tbl' : [{'col': 'alias'}, {'col': 'alias'}]},
				# {'col' : 'alias'},
				for key, value in self.columns.items():
					if type(value) is str:
						# {'key' : 'alias'},
						q.append(' as '.join((key, value)))
					if type(value) is list:
						# {'tbl' : [{'col': 'alias'}, {'col': 'alias'}]},
						for col_value in value:
							if type(value) is list:
								# {'tbl' : ['col', 'col']},
								q.append(', '.join('.'.join((key, c)) for c in col_value))
							if type(col_value) is dict:
								q.append(''.join((key, '.', c, ' as ', a)) for c, a in col_value.items())


		q.append(' FROM ')

		# FROM TABLES
		if type(self.tables) is str:
			q.append(self.tables)
		else:
			tables = []
			for tbl in self.tables:
				if type(tbl) is str:
					tables.append(tbl)
				else:
					tables.append(' '.join(tbl))
			q.append(', '.join(tables))
		
		# JOIN
		if self.join:
			join_values = {}
			for join in self.join:
				q.append(' '.join((' ', join[0], join[1], join[2])))
				
				q.append(' ON ')
				
				where = join[3]
				where, join_vals = JoinCondition(where).sql(join_values)
				
				#join_values.update(join_vals)
				q.append(where)
		
		# WHERE
		if self.where:
			q.append(' WHERE ')
			where, where_values = Condition(self.where).sql()
			q.append(where)
			
		# GROUP BY
		if self.group:
			q.append(' GROUP BY ')

			if type(self.group) is str:
				q.append(self.group)
			else:

				if type(self.group) is list:

					# ['col1', 'col2']
					q.append(', '.join(col for col in self.group))

				elif type(self.group) is dict:
					# {'tbl' : ['col', 'col']},
					for key, value in self.group.items():
						for col_value in value:
							q.append(', '.join('.'.join((key, c)) for c in col_value))

		# ORDER BY
		if self.order:
			q.append(' ORDER BY ')

			if type(self.order) is str:
				q.append(self.order)
			else:

				if type(self.order) is list:
					# ['col1', 'col2']
					q.append(', '.join(col for col in self.order))

				elif type(self.order) is dict:
					# {'tbl' : ['col', 'col']},
					# {'tbl' : [{'col': 'ASC'}, {'col': 'DESC'}]},
					# {'col' : 'ASC'},
					for key, value in self.order.items():
						if type(value) is str:
							# {'key' : 'ASC'},
							q.append(' '.join((key, value)))
						if type(value) is list:
							# {'tbl' : [{'col': 'ASC'}, {'col': 'ASC'}]},
							for col_value in value:
								if type(value) is list:
									# {'tbl' : ['col', 'col']},
									q.append(', '.join('.'.join((key, c)) for c in col_value))
								if type(col_value) is dict:
									q.append(''.join((key, '.', c, ' ', a)) for c, a in col_value.items())


		if self.limit:
			q.append(' LIMIT ')
			if type(self.limit) is list:
				q.append(str(self.limit.pop()))
				if self.limit:
					q.append(' OFFSET ')
					q.append(str(self.limit.pop()))
				#q.append(','.join(str(i) for i in self.limit))
			else:
				q.append(str(self.limit))
		if join_values is None:
			join_values = {}
		if where_values is None:
			where_values = {}
		
		where_values.update(join_values)
		
		return ''.join(q), where_values

	def count_sql(self):
		'''returns count query sql'''
		
		where_values = {}
		join_values = {}
		
		q = ['SELECT ']
		
		if self.count_column:
			q.append(self.count_column.join((' count(', ') ')))
		else:
			q.append(' count(*) ')

		q.append(' FROM ')

		# FROM TABLES
		if type(self.tables) is str:
			q.append(self.tables)
		else:
			tables = []
			for tbl in self.tables:
				if type(tbl) is str:
					tables.append(tbl)
				else:
					tables.append(' '.join(tbl))
			q.append(', '.join(tables))
		
		# JOIN
		if self.join:
			join_values = {}
			for join in self.join:
				q.append(' '.join((' ', join[0], join[1], join[2])))
				
				q.append(' ON ')
				
				where = join[3]
				
				where, join_vals = JoinCondition(where).sql(join_values)
				
				#join_values.update(join_vals)
				q.append(where)
		
		# WHERE
		if self.where:
			q.append(' WHERE ')
			where, where_values = Condition(self.where).sql()
			q.append(where)


		# GROUP BY
		if self.group:
			q.append(' GROUP BY ')

			if type(self.group) is str:
				q.append(self.group)
			else:

				if type(self.group) is list:

					# ['col1', 'col2']
					q.append(', '.join(col for col in self.group))

				elif type(self.group) is dict:
					# {'tbl' : ['col', 'col']},
					for key, value in self.group.items():
						for col_value in value:
							q.append(', '.join('.'.join((key, c)) for c in col_value))

		#if self.limit:
			#q.append(' LIMIT ')
			#if type(self.limit) is list:
				#q.append(str(self.limit.pop()))
				#if self.limit:
					#q.append(' OFFSET ')
					#q.append(str(self.limit.pop()))
				##q.append(','.join(str(i) for i in self.limit))
			#else:
				#q.append(str(self.limit))
		if join_values is None:
			join_values = {}
		if where_values is None:
			where_values = {}
		
		where_values.update(join_values)
		
		return ''.join(q), where_values

	def __init__(self, json, **args):

		self.columns = json.get('columns', ['*'])

		self.tables = json.get('tables', None)

		if self.tables is None:
			self.tables = []
			
		table = json.get('table', None)
		if table is not None:
			self.tables.append(table)
		
		self.where 	= json.get('where', None)
		self.join 	= json.get('join', None)
		self.order 	= json.get('order', None)
		self.group 	= json.get('group', None)
		self.limit 	= json.get('limit', None)
		self.having	= json.get('having', None)
		
		self.count_column = json.get('count_column', None)

		# values from where condtions will be added here
		self.values = {}

	def execute(self):
		'''shotcut method'''
		q, where_values = self.sql()
		
		return IN.db.execute(q, where_values)

	def execute_count(self):
		'''shotcut method'''
		q, where_values = self.count_sql()
		
		return IN.db.execute(q, where_values)


class Insert(Query):
	'''Multiple Insert Query

	q = Insert({
			'table' : 'account',
			'columns': [],
			'values': [[], [], ...],
		})
	'''

	def __init__(self, json):

		self.columns = json.get('columns', [])
		self.table 	= json.get('table', None)
		self.values = json.get('values', [])
		self.returning = json.get('returning', None)

	def sql(self, values):
		'''returns json as insert sql'''
		q = ['INSERT INTO ']
		q.append(self.table)

		q.append(', '.join(col for col in self.columns).join((' (', ') ')))

		q.append(' VALUES ')

		vstr = ', '.join('%s' for col in range(len(self.columns))).join(('(', ')'))
		vstr = ', '.join(vstr for i in range(len(values)))
		
		q.append(vstr)
		
		if self.returning:
			q.append(' returning ')
			q.append(self.returning)

		return ''.join(q)

	def execute(self, values = None):
		'''shotcut method'''
		if values is None:
			values = self.values
		sql = self.sql(values)

		# merge values or multiple rows
		pass_values = []
		for row in values:
			pass_values.extend(row)
		
		return IN.db.execute(sql, pass_values)


class InsertDict(Query):
	'''Insert Query

	q = InsertDict({
			'table' : 'account',
			'columns': [],
			'values': {},
		})
	'''

	def __init__(self, json):

		self.columns = json.get('columns', [])
		self.table 	= json.get('table', None)
		self.values = json.get('values', {})
		self.returning = json.get('returning', None)

	def sql(self):
		'''returns json as insert sql'''

		sql = ['INSERT INTO ']
		sql.append(self.table)
		sql.append(', '.join(col for col in self.columns).join(' (', ') '))
		sql.append(' VALUES ')
		sql.append(', '.join(col.join('%(', ')s') for col in self.columns).join(' (', ') '))
		if self.returning:
			sql.append(' returning ')
			sql.append(self.returning)

		return ''.join(sql)

	def execute(self, values = None):
		'''shotcut method'''
		if values is None:
			values = self.values
		return IN.db.execute(self.sql(), values)


class Delete(Query):
	'''Delete Query

	q = InsertDict({
			'table' : 'account',
			'where': [],
		})
	'''

	def __init__(self, json):

		self.table 	= json.get('table', None)
		self.where = json.get('where', [])
		
	def sql(self):
		'''returns json as insert sql'''

		q = ['DELETE FROM ']
		q.append(self.table)

		where_values = []
		if self.where:
			q.append(' WHERE ')
			where, where_values = Condition(self.where).sql()
			q.append(where)
			
		return ''.join(q), where_values

	def execute(self):
		'''shotcut method'''
		q, where_values = self.sql()
		return IN.db.execute(q, where_values)


class Update(Query):
	'''Update Query

	q = Update({
			'table' : 'account',
			'set' : [id, value]
			'where': [],
		})
	'''

	def __init__(self, json):

		self.table 	= json.get('table', None)
		self.set 	= json.get('set', [])
		self.where = json.get('where', [])
		
	def sql(self):
		'''returns json as insert sql'''

		q = ['UPDATE ']
		q.append(self.table)

		values = {}

		if self.values:
			q.append(' SET ')
			set, set_values = ValueSet(self.set).sql()
			q.append(set)
			values.update(set_values)
			
		if self.where:
			q.append(' WHERE ')
			where, where_values = Condition(self.where).sql()
			q.append(where)
			values.update(where_values)
			
		return ''.join(q), values

	def execute(self):
		'''shotcut method'''
		q, where_values = self.sql()
		
		return IN.db.execute(q, where_values)



class Condition:
	
	param_prefix = '_' # 1 _
	
	'''
		'where' : [
			['id', 5],
			['status', '!=', 0],
			[[], [], [], []],		# and
			['or', [				# or
				[],
				[],
			]],
		],
	'''

	in_any_all = ['IN', 'ALL', 'ANY']

	def __init__(self, json):
		self.where = json

	def sql(self, where_values = None, andor = ' AND '):

		if where_values is None:
			where_values = {}

		where = self.where

		length = len(where)

		if length == 1:
			if type(where[0]) is str:
				return where[0], where_values

		if length == 2:
			if type(where[0]) is str:
				if where[0].lower() == 'or':
					return self.__class__(self.where[1]).sql(where_values, ' OR ')
				elif where[0].lower() == 'and':
					return self.__class__(self.where[1]).sql(where_values, ' AND ')
				else:
					# ['status', 0]
					_len = len(where_values) + 1
					param_key = self.param_prefix + str(_len)
					where_values[param_key] = where[1]
					return ''.join((where[0], ' = ', '%(', param_key, ')s')), where_values

		if length == 3:
			col = where[0]
			if type(col) is str:
				# ['status', '!=', 0],
				op = where[1]
				val = where[2]
				# TODO: Allow sub query, select json
				if op in self.in_any_all and type(val) is not tuple: # array is tuple
					val = tuple(val)

				param_key = self.param_prefix + str(len(where_values) + 1)
				where_values[param_key] = val

				# add spaces, col IN ()
				op = op.join((' ', ' '))
				return op.join((col, ''.join(('%(', param_key, ')s')))), where_values

		q = []

		for where in self.where:
			subq, where_values = self.__class__(where).sql(where_values, andor)
			q.append(subq.join(('(', ')')))
		q = andor.join(q)
		return q, where_values

class JoinCondition(Condition):
	
	param_prefix = '___' # 3 _

class ValueSet:
	'''
		'set' : [
			['id', 5],
		],
	'''
	
	param_prefix = '__' # 2 _

	def __init__(self, json):
		self.set = json

	def sql(self):

		set_values = {}
		cols = []
		for col_val in self.set:
			_len = len(set_values) + 1
			param_key = self.param_prefix + str(_len) # __, it should not be conflit with where values
			set_values[param_key] = col_val[1]
			cols.append(''.join((col_val[0], ' = ', '%(', param_key, ')s')))

		return ', '.join(cols), set_values
