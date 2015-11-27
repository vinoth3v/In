from .page import *

@IN.hook
def actions():
	actns = {}

	actns['vakai/more/{parent_entity_bundle}/{last_id}/{parent_entity_id}'] = {
		'title' : 'load more vakais',
		'handler' : action_vakai_load_more,
	}

	actns['vakai/add/sub/{parent_entity_bundle}/{parent_id}'] = {
		'title' : 'vakai add sub',
		'handler' : action_vakai_add_sub_form,
	}

	actns['vakai/{vakai_id}/delete/confirm'] = {
		'title' : 'vakai delete confirm',
		'handler' : action_vakai_delete_form,
	}
	actns['vakai/{vakai_id}/edit'] = {
		'title' : 'vakai edit',
		'handler' : action_vakai_edit_form,
	}
	
	actns['vakai/{vakai_bundle}/autocomplete/{query}'] = {
		'title' : 'vakai autocomplete',
		'handler' : action_vakai_autocomplete,
	}
	
	actns['vakai/{entity_type}/{field}/{vakai_id}'] = {
		'title' : 'vakai list',
		'handler' : action_handler_vakai_entity_list,
	}
	
	return actns




def action_vakai_add_sub_form(context, action, parent_entity_bundle, parent_id, **args):
	
	entity_type = 'Vakai'
	
	entity = IN.entitier.load_single(entity_type, int(parent_id))

	if not entity:
		return
		
	try:
		
		args = {
			'data' : {
				# ajax replace
				'id' : '_'.join(('VakaiAdminAddForm', entity_type, parent_entity_bundle)),
				'title' : s('Add sub vakai'),
			},
			'parent_entity_bundle' : parent_entity_bundle,
			'parent_entity_type' : entity_type,
			'parent_entity_id' : int(parent_id),
		}
		
		form = IN.entitier.get_entity_add_form(entity_type, parent_entity_bundle, args)
		
		element_id = str(parent_id).join(('#Vakai_', '-ajax-vakai-form'))
		reply_id = '#add_sub-link-Vakai-' + str(parent_id)
		
		output = [
			{'method' : 'html', 'args' : [element_id, IN.themer.theme(form)]},
			{'method' : 'remove', 'args' : [reply_id]},
			{'method' : 'focus', 'args' : [element_id + ' form input']},
		]
		context.response = In.core.response.CustomResponse(output = output)
	except:
		IN.logger.debug()


def action_vakai_delete_form(context, action, vakai_id, **args):
	
	entity = IN.entitier.load_single('Vakai', int(vakai_id))

	if not entity:
		context.not_found()
		
	try:
		
		form = IN.entitier.get_entity_delete_form(entity)
		
		if context.request.ajax_modal:
			
			element_id = 'i-ajax-modal'
			element_id = element_id + ' .modal-content'
			
			modal = Object.new(type="HTMLModalPopup", data = {
				'title' : s('Delete!'),
			})
			modal.add(form)
			
			output = {
				element_id : modal,			
			}
			context.response = In.core.response.PartialResponse(output = output)
		else:
			context.response.output.add(form)
			
	except:
		IN.logger.debug()

def action_vakai_edit_form(context, action, vakai_id, **args):
	
	entitier = IN.entitier
	
	entity = entitier.load_single('Vakai', int(vakai_id))

	if not entity:
		context.not_found()
		
	try:
		
		entitier.access('edit', entity, deny = True)
		
		form = IN.entitier.get_entity_edit_form(entity.__type__, entity.id)
		
		if context.request.ajax:
			element_id = '-'.join(('.vakai', str(entity.id))) # class
			
			output = [{
				'method' : 'html',
				'args' : [element_id, IN.themer.theme(form)]
			}]
			context.response = In.core.response.CustomResponse(output = output)
			
		else:
			context.response.output.add(form)
			
	except:
		IN.logger.debug()




	
