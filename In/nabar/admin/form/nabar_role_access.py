from collections import OrderedDict

class FormNabarRoleAccessAdmin(Form):

	def __init__(self, data = None, items = None, post = None, **args):

		if data is None: data = {}
		if post is None: post = {}

		if 'id' not in data:
			data['id'] = 'FormNabarRoleAccessAdmin'

		super().__init__(data, items, **args)
		
		group = args['group']

		self.group = group

		roleset = self.add('FieldSet', {
			'id' : 'roleset',
			'title' : s('Role Accesss'),
			'css' : ['i-form-row i-margin-large']
		})

		roles = IN.nabar.roles
		access_keys = IN.nabar.access_keys
		access_roles = IN.nabar.access_roles
		
		if group not in access_keys:
			roleset.add('TextDiv', {
				'id' : 'terms',
				'value' : s('''Access keys for the group {group} not found!''', {'group' : group}),
				'css' : ['i-text-primary']
			})
			return

		access_keys = access_keys[group]

		#set.add('TextDiv', {
			#'value' : s('Access keys'),
			#'css' : ['i-width-3-10']
		#})

		role_options = OrderedDict()
		
		for rid, role in roles.items():

			# admin always has access
			if rid == IN.nabar.admin_role_id:
				continue
			
			name = role['name']
			role_options[str(rid)] = name
			#set.add('TextDiv', {
				#'id' : 'role_' + str(rid),
				#'value' : name,
				#'css' : ['']
			#})

		#set.add('TextDiv', {
			#'value' : '<hr class="i-grid-divider">',
		#})

		post_access = post.get('access', {})

		flags = {
			'danger' : s('danger').join((' <span class="i-badge i-badge-danger">', '</span>')),
			'warning' : s('warning').join((' <span class="i-badge i-badge-warning">', '</span>'))
		}

		for key, data in access_keys.items():
			keyset = roleset.add('FieldSet', {
				'id' : 'set_' + key,
				'css' : ['i-form-row i-margin-large i-grid i-grid-divider']
			})

			title = data.get('title', '')
			info = data.get('info', '')
			flag = data.get('flag', '')
			flag = flags.get(flag, '')
			
			div = keyset.add('TextDiv', {
				'id' : 'access_text_' + key,
				'css' : ['i-width-1-1 i-margin-bottom']
			})
			div.add('H3', {
				'value' : title + flag,
				'weight' : 0,
			})
			div.add('TextDiv', {
				'value' : ''.join((s('Access key'), ': ', '<em>', key, '</em>')),
				'weight' : 1,
			})
			div.add('TextDiv', {
				'value' : info,
				'weight' : 2,
			})

			#keyset.add('TextDiv', {
				#'value' : '<hr class="i-grid-divider">',
			#})

			
			value = [str(r) for r in access_roles.get(key, [])]

			keyset.add('CheckBoxes', {
				'id' : '-'.join(('access', str(rid), key)),
				'name' : ''.join(('access[', key, ']')),
				'value' : value,
				'options' : role_options,
				'css' : ['i-grid'],
			})
			
			#for rid, role in roles.items():
				#set.add('CheckBox', {
					#'id' : '-'.join(('access', str(rid), key)),
					#'name' : ''.join(('access[', str(rid), '][', key, ']')),
					#'value' : post.get('name'),
					#'css' : ['']
				#})

			roleset.add('TextDiv', {
				'value' : '<div class="i-grid-divider"></div>',
			})
		
		#set.add('TextDiv', {
			#'id' : 'terms',
			#'value' : s('''By registering to our site you are accepting our {term_link}.''', term_link = tlink),
			#'css' : ['i-text-primary']
		#})

		roleset.add('Submit', {
			'id' : 'submit',
			'value' : s('Save Access'),
			'css' : ['i-button i-button-primary i-button-large']
		})

		self.css.append('i-panel i-panel-box i-margin-large')

@IN.register('FormNabarRoleAccessAdmin', type = 'Former')
class FormNabarRoleAccessAdminFormer(FormFormer):

	#def validate(self, form, post):
		#pprint(post)
		#if form.has_errors: # fields may have errors
			#return

	def submit(self, form, post):

		if form.has_errors:
			return

		access_keys = IN.nabar.access_keys[form.group]
		
		post_access = post.get('access', {})

		connection = IN.db.connection
		
		try:

			# delete old keys
			cursor = IN.db.delete({
				'table' : 'account.access',
				'where' : ['access', 'IN', access_keys],
			}).execute()

			if post_access:
					
				values = []
				for key, role_ids in post_access.items():
					for role_id in role_ids:
						values.append([role_id, key])
				
				cursor = IN.db.insert({
					'table' : 'account.access',
					'columns' : ['role_id', 'access'],
					'values' : values,
				}).execute()
			
			# commit
			connection.commit()

			# rebuild access
			# TODO: NOT USEFULL. server runs on multiple instances
			IN.nabar.build_access_roles()
			
		except Exception as e:
			connection.rollback()
			IN.logger.debug()
			form.error_message = s('Unknown error occurred! Please try again later!')
			form.has_errors = True
			return False

		#form.redirect = '/admin/nabar/role'

