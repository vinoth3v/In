from .page import *

@IN.hook
def actions():
	actns = {}

	actns['comment/more/{entity_type}/{entity_id}/{last_id}/{parent_id}'] = {
		'title' : 'load more comments',
		'handler' : action_comment_load_more,
	}

	actns['comment/reply/{entity_type}/{entity_id}/{parent_id}/{container_id}'] = {
		'title' : 'comment reply',
		'handler' : action_comment_reply_form,
	}

	actns['comment/{comment_id}/delete/confirm'] = {
		'title' : 'comment delete confirm',
		'handler' : action_comment_delete_form,
	}
	actns['comment/{comment_id}/edit'] = {
		'title' : 'comment edit',
		'handler' : action_comment_edit_form,
	}
	
	return actns

