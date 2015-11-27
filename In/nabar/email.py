from In.mailer.email import EMail, EMailThemer

class WelcomeEmailVerification(EMail):
	
	mail_verify_token = None
	
@IN.register('WelcomeEmailVerification', type = 'Themer')
class WelcomeEmailVerificationThemer(EMailThemer):
	'''WelcomeEmailVerification themer'''
	
	def theme_process_variables(self, obj, format, view_mode, args):
		
		super().theme_process_variables(obj, format, view_mode, args)
		
		# token/verify/!register/!mail_verify_token
		args['mail_verify_token'] = obj.mail_verify_token or ''
		

class AccountRecoveryEmail(EMail):
	
	mail_verify_token = None
	

@IN.register('AccountRecoveryEmail', type = 'Themer')
class AccountRecoveryEmailThemer(EMailThemer):
	'''AccountRecoveryEmail themer'''
	
	def theme_process_variables(self, obj, format, view_mode, args):
		
		super().theme_process_variables(obj, format, view_mode, args)
		
		# token/verify/!register/!mail_verify_token
		args['mail_verify_token'] = obj.mail_verify_token or ''
		
