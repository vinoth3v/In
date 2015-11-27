
@IN.hook
def action_handler_stringer_update_to_db(context, action, **args):
	'''not here. updates duplicates'''

	connection = IN.db.connection

	try:
		
		for lang, lang_lc in IN.stringer.strings.items():
			for lc, strings in lang_lc.items():
				for string, conf in strings.items():
					if conf['new']:
						values = []
						try:
							tstring = conf['string']
							values.append([tstring, lc, tstring, lang, 0])
							conf['new'] = False # next update ignore this

							cursor = IN.db.insert({
								'table' : 'config.config_string',
								'columns' : ['string', 'context', 'tstring', 'language', 'translated'],
								'values' : values,
							}).execute()
							connection.commit()
						except Exception as e:
							IN.logger.debug()

		#cursor = IN.db.insert({
			#'table' : 'config.config_string',
			#'columns' : ['string', 'context', 'tstring', 'language', 'translated'],
			#'values' : values,
		#}).execute()

		## commit
		#connection.commit()
	
	except Exception as e:
		connection.rollback()
		IN.logger.debug()
	