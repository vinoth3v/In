from In.boxer.box import Box, BoxThemer

class BoxAdminNabarRoleAccessGroup(Box):

	pass


@IN.register('BoxAdminNabarRoleAccessGroup', type = 'Themer')
class BoxAdminNabarRoleAccessGroupThemer(BoxThemer):


	def theme(self, obj, format, view_mode, args):
		super().theme(obj, format, view_mode, args)

	def theme_value(self, obj, format, view_mode, args):

		values = []

		access_keys = IN.nabar.access_keys
		
		for group in access_keys:
			values.append(''.join(('<li><a data-ajax_panel="content" href="/admin/nabar/role/access/!', group, '">', group, '</a></li>')))
		
		box = ''.join(values).join(('''<div class="i-panel i-panel-box">

			<ul class="i-nav i-nav-side">
				''', '''
			</ul>

		</div>'''))

		return box
