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
	
	def __init__(self, json, **args):

		self.columns = json.get('columns', [])
		
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

	def sql(self):
		'''returns json as select sql'''
		
		where_values = {}
		join_values = {}
		
		q = ['SELECT ']

		q_append = q.append
		
		# COLUMNS
		
		self_columns = self.columns
		type_self_columns = type(self_columns)
		
		if not self_columns:
			q_append('*')
		elif type_self_columns is str:
			q_append(self_columns)
		else:

			if type_self_columns is list:

				# ['col1', 'col2']
				q_append(', '.join(col for col in self_columns))

			elif type_self_columns is dict:
				# {'tbl' : ['col', 'col']},
				# {'tbl' : [{'col': 'alias'}, {'col': 'alias'}]},
				# {'col' : 'alias'},
				for key, value in self_columns.items():
					type_value = type(value)
					if type_value is str:
						# {'key' : 'alias'},
						q_append(' as '.join((key, value)))
					elif type_value is list:
						# {'tbl' : [{'col': 'alias'}, {'col': 'alias'}]},
						for col_value in value:
							type_col_value = type(col_value)
							if type_col_value is list:
								# {'tbl' : ['col', 'col']},
								q_append(', '.join('.'.join((key, c)) for c in col_value))
							elif type_col_value is dict:
								q_append(''.join((key, '.', c, ' as ', a)) for c, a in col_value.items())


		q_append(' FROM ')

		# FROM TABLES
		
		self_tables = self.tables
		
		if type(self_tables) is str:
			q_append(self_tables)
		else:
			tables = []
			for tbl in self_tables:
				if type(tbl) is str:
					tables.append(tbl)
				else:
					tables.append(' '.join(tbl))
			q_append(', '.join(tables))
		
		# JOIN
		self_join = self.join
		
		if self_join:
			join_values = {}
			for join in self_join:
				q_append(' '.join((' ', join[0], join[1], join[2])))
				
				q_append(' ON ')
				
				where = join[3]
				where, join_vals = JoinCondition(where).sql(join_values)
				
				#join_values.update(join_vals)
				q_append(where)
		
		# WHERE
		
		self_where = self.where
		
		if self_where:
			q_append(' WHERE ')
			where, where_values = Condition(self_where).sql()
			q_append(where)
			
		# GROUP BY
		
		self_group = self.group
		type_self_group = type(self_group)
		
		if self_group:
			q_append(' GROUP BY ')

			if type_self_group is str:
				q_append(self_group)
			else:

				if type_self_group is list:

					# ['col1', 'col2']
					q_append(', '.join(col for col in self_group))

				elif type_self_group is dict:
					# {'tbl' : ['col', 'col']},
					for key, value in self_group.items():
						for col_value in value:
							q_append(', '.join('.'.join((key, c)) for c in col_value))

		# ORDER BY
		
		self_order = self.order
		type_self_order = type(self_order)
		
		if self_order:
			q_append(' ORDER BY ')

			if type_self_order is str:
				q_append(self_order)
			else:
				
				if type_self_order is list:
					# ['col1', 'col2']
					q_append(', '.join(col for col in self_order))

				elif type_self_order is dict:
					# {'tbl' : ['col', 'col']},
					# {'tbl' : [{'col': 'ASC'}, {'col': 'DESC'}]},
					# {'col' : 'ASC'},
					for key, value in self_order.items():
						if type(value) is str:
							# {'key' : 'ASC'},
							q_append(' '.join((key, value)))
						if type(value) is list:
							# {'tbl' : [{'col': 'ASC'}, {'col': 'ASC'}]},
							for col_value in value:
								if type(value) is list:
									# {'tbl' : ['col', 'col']},
									q_append(', '.join('.'.join((key, c)) for c in col_value))
								if type(col_value) is dict:
									q_append(''.join((key, '.', c, ' ', a)) for c, a in col_value.items())

		# LIMIT
		
		self_limit = self.limit
		if self_limit:
			q_append(' LIMIT ')
			if type(self_limit) is list:
				q_append(str(self_limit.pop()))
				if self_limit:
					q_append(' OFFSET ')
					q_append(str(self_limit.pop()))
				#q.append(','.join(str(i) for i in self.limit))
			else:
				q_append(str(self_limit))
				
		if join_values is None:
			join_values = {}
		if where_values is None:
			where_values = {}
		
		if join_values:
			where_values.update(join_values)
		
		return ''.join(q), where_values

	def count_sql(self):
		'''returns count query sql'''
		
		where_values = {}
		join_values = {}
		
		q = ['SELECT ']
		
		q_append = q.append
		
		if self.count_column:
			q_append(self.count_column.join((' count(', ') ')))
		else:
			q_append(' count(*) ')

		q_append(' FROM ')

		# FROM TABLES
		
		self_tables = self.tables
		
		if type(self_tables) is str:
			q_append(self_tables)
		else:
			tables = []
			for tbl in self_tables:
				if type(tbl) is str:
					tables.append(tbl)
				else:
					tables.append(' '.join(tbl))
			q_append(', '.join(tables))
			
		
		# JOIN
		self_join = self.join
		
		if self_join:
			join_values = {}
			for join in self_join:
				q_append(' '.join((' ', join[0], join[1], join[2])))
				
				q_append(' ON ')
				
				where = join[3]
				where, join_vals = JoinCondition(where).sql(join_values)
				
				#join_values.update(join_vals)
				q_append(where)
		
		
		# WHERE
		
		self_where = self.where
		
		if self_where:
			q_append(' WHERE ')
			where, where_values = Condition(self_where).sql()
			q_append(where)
			

		# GROUP BY
		
		self_group = self.group
		type_self_group = type(self_group)
		
		if self_group:
			q_append(' GROUP BY ')

			if type_self_group is str:
				q_append(self_group)
			else:

				if type_self_group is list:

					# ['col1', 'col2']
					q_append(', '.join(col for col in self_group))

				elif type_self_group is dict:
					# {'tbl' : ['col', 'col']},
					for key, value in self_group.items():
						for col_value in value:
							q_append(', '.join('.'.join((key, c)) for c in col_value))

		if join_values is None:
			join_values = {}
		if where_values is None:
			where_values = {}
		
		if join_values:
			where_values.update(join_values)
		
		return ''.join(q), where_values


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
		
		q_append = q.append
		self_columns = self.columns
		
		q_append(self.table)

		q_append(', '.join(col for col in self_columns).join((' (', ') ')))

		q_append(' VALUES ')

		vstr = ', '.join('%s' for col in range(len(self_columns))).join(('(', ')'))
		vstr = ', '.join(vstr for i in range(len(values)))
		
		q_append(vstr)
		
		if self.returning:
			q_append(' returning ')
			q_append(self.returning)

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

		q = ['INSERT INTO ']
		q_append = q.append
		self_columns = self.columns
		
		q_append(self.table)
		q_append(', '.join(col for col in self_columns).join(' (', ') '))
		q_append(' VALUES ')
		q_append(', '.join(col.join('%(', ')s') for col in self_columns).join(' (', ') '))
		if self.returning:
			q_append(' returning ')
			q_append(self.returning)

		return ''.join(q)

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
		q_append = q.append
		
		q_append(self.table)
		
		where_values = []
		if self.where:
			q_append(' WHERE ')
			where, where_values = Condition(self.where).sql()
			q_append(where)
			
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
		q_append = q.append
		
		q_append(self.table)
		
		values = {}

		if self.values:
			q_append(' SET ')
			set, set_values = ValueSet(self.set).sql()
			q_append(set)
			values.update(set_values)
			
		if self.where:
			q_append(' WHERE ')
			where, where_values = Condition(self.where).sql()
			q_append(where)
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
			where_0 = where[0]
			
			if type(where_0) is str:				
				where_0_lower = where_0.lower()
				
				if where_0_lower == 'or':
					return self.__class__(where[1]).sql(where_values, ' OR ')
				elif where_0_lower == 'and':
					return self.__class__(where[1]).sql(where_values, ' AND ')
				else:
					# ['status', 0]
					_len = len(where_values) + 1
					param_key = self.param_prefix + str(_len)
					where_values[param_key] = where[1]
					return ''.join((where_0, ' = ', '%(', param_key, ')s')), where_values

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
		q_append = q.append
		for where in self.where:
			subq, where_values = self.__class__(where).sql(where_values, andor)
			q_append(subq.join(('(', ')')))
		
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
		cols_append = cols.append
		
		for col_val in self.set:
			_len = len(set_values) + 1
			param_key = self.param_prefix + str(_len) # __, it should not be conflit with where values
			set_values[param_key] = col_val[1]
			cols_append(''.join((col_val[0], ' = ', '%(', param_key, ')s')))

		return ', '.join(cols), set_values
