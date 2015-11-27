
@IN.hook
def form_load_form(form, post, args):

	field_name = get_form_bot_field(form.__type__)

	# TODO: do this as early as possible
	# bot check
	if post: # process if post is not empty
		if post.get(field_name, None): # if not empty it is bot
			return IN.context.bad_request() # or not found?

	# add the bot field
	form.add('InputField', {
		'id' : field_name, 
		'name' : field_name, 
		'css' : ['i-hidden', 'form-field-tob'],
		'item_wrapper' : None,
		'weight' : 100,
	})
	

def get_form_bot_field(type = 'default'):
	form_bot_fields = IN.APP.config.form_bot_fields
	if type in form_bot_fields: # mostly no
		return form_bot_fields[type]
	else:
		try:
			return form_bot_fields['default']
		except Exception:
			return 'field_e-mail-address'
