@IN.hook
def actions():
	actns = {}

	actns['admin/structure/entity/{entity_type}/map'] = {
		'title' : 'Entity to comment map',
		'handler' : action_admin_entity_comment_map,
	}

	return actns

def action_admin_entity_comment_map(context, action, **args):
	# TODO: ADMIN ACCESS

	#IN.context.access('admin_nabar_role_access', deny = True)
	
	frm = IN.former.load('FormEntityCommentMapAdmin')

	page = context.response.output

	context.asset.add_js('/files/libraries/uikit-2.22.0/dist/js/components/accordion.min.js', 'accordion')
	
	page.add(frm)

