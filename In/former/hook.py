


@IN.register
def register():
	'''
	instance :
		class - class type if assigned directly
		instance - instance will be created and assigned, all object will use the same member instance
	'''
	return {
		# all Form should have __form_handler__ member of type which is registered as __form_handler__ for Form type
		'class_members' : {								# register for
			'Form' : {									# type of object - arg to class members
				'Former' : {					# key
					'name' : 'Former',		# member name
					'instance' : 'instance',			# type of instance
				},
			},
		},
	}


@IN.hook
def __context_early_action__(context):
	'''entry point: handle the submitted form

	'''

	if IN.former.is_form_submit(context.request):
		form = IN.former.load_form_from_submit()

		if form is None:
			return

		args = {
			'handler' : IN.former.process,
			'handler_arguments' : {
				'form' : form,
				'post' : context.request.args['post'],
			},
			'pass_next' : True  # pass to default page loading
		}

		action_object = In.core.action.ActionObject(**args)

		return action_object
