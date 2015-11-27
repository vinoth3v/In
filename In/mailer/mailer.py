import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid


class Mailer:
	'''Mailer class for sending E-mail messages.

	TODO: async
	mail templates
	'''
	
	def __init__(self):
		self.connections = {}
		
	def smtp(self, server = 'default'):
		'''returns a new smtp connection'''
		
		mail_config = IN.APP.config.mail
		smtp_config = mail_config['smtp']
		if not server in smtp_config:
			server = 'default'
			
		smtp = self.connections.get(server, None)
		if smtp:
			try:
				status = smtp.noop()[0]
			except: # smtplib.SMTPServerDisconnected
				status = -1
			
			if status == 250:
				return smtp # reuse
		
		
		smtp = smtplib.SMTP(*smtp_config[server])
		
		if 'login' in mail_config:
			logins = mail_config['login']
			smtp.login(logins[0], logins[1])
		
		self.connections[server] = smtp
		
		return smtp
		
	def send(self, emailobj):
		'''Send mails

		'''

		config = IN.APP.config.mail

		if not emailobj.from_address:
			emailobj.from_address = config['from']
		if not emailobj.from_name:
			emailobj.from_name = config['from_name']
		if not emailobj.reply_to:
			emailobj.reply_to = config['reply_to']
		
		
		#print(emailobj.to_address)
		#if type(emailobj.to_address) is str: # mail address
			#emailobj.to_address = Address(emailobj.to_address)
		#else:
			#emailobj.to_address = Address(*emailobj.to_address)
		
		#message = EmailMessage()
		message = MIMEMultipart('alternative')

		#message['From'] = Address(emailobj.from_name, emailobj.from_address)
		message['From'] = emailobj.from_address
		message['To'] 	= emailobj.to_address
		message['Subject'] 	= emailobj.title

		# body_text
		
		themer = IN.themer
		
		# theme the mail obj and set body
		body_text = themer.theme(emailobj, view_mode = 'text')
		#message.set_content(body_text)
		
		text_part = MIMEText(body_text, 'plain')
		
		
		# default view mode is html
		body_html = themer.theme(emailobj)
		#message.add_alternative(body_html)
		
		html_part = MIMEText(body_html, 'html')
		
		
		message.attach(text_part)
		message.attach(html_part)

		try:
			
			# use default smtp for now
			# TODO: re use smtp connections
			mail_server = self.smtp()
			
			#mail_server.starttls()
			#mail_server.login(smtp_user_name, smtp_password)
			
			# send it
			#mail_server.send_message(message)
			
			# send it
			mail_server.sendmail(emailobj.from_address, emailobj.to_address, message.as_string())
			
		except Exception as e:
			IN.logger.debug()
			# retry

		#mail_server.quit()

'''

# Add the html version.  This converts the message into a multipart/alternative
# container, with the original text message as the first part and the new html
# message as the second part.

asparagus_cid = make_msgid()
msg.add_alternative("""\
    <img src="cid:{asparagus_cid}" \>
""".format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')

# note that we needed to peel the <> off the msgid for use in the html.

# Now add the related image to the html part.
with open("roasted-asparagus.jpg", 'rb') as img:
    msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg',
                                     cid=asparagus_cid)

'''
