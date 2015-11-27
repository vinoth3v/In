import re
from In.core.object_meta import ObjectMetaBase


class ValuatorContainer(dict):

	def __missing__(self, key):
		vcls = IN.register.get_class(key, 'Valuator')
		obj = vcls()
		self[key] = obj
		return obj

class ValuatorEngine:
	'''Valuator class that valuate values based on validation rules.

	Instance available as IN.valuator
	'''

	# dict of all Valuator instances
	valuators = ValuatorContainer()

	def validate(self, value, rule): # rule is ['type', args] or [[], [], []]
		'''
			#TODO: allow per false error message
			rule = [
				'And', [
					['Length', '>', 6, 'The value length should be greater than 6.'],
					['Not', [['Num']],
					['Or', [
						['Email', 'Invalid email address.'],
						['Domain'],
						['Url', 'Invalid Url.'],
					]],
				]],
			]
		'''
		if not rule: # empty list

			return [True]

		try:
			firstitem = rule[0]
			item_type = type(firstitem)
			if item_type is str: # ['type', args]
				args = rule[1:]
				result = self.valuators[firstitem].validate(value, *args)
				if not result[0]:
					#return [False, args[-1]] # last item is error message
					return result
			elif item_type is list: # [[], [], []]
				for subrule in rule:
					result = self.validate(value, subrule) # recursive
					if not result[0]:
						return result
		except Exception as e:
			IN.logger.debug()
			return [False, str(e)]

		return [True]

	def __getattr__(self, key):
		self.key = self.valuators[key]
		return self.key

class ValuatorMeta(ObjectMetaBase):

	__class_type_base_name__ = 'ValuatorBase'
	__class_type_name__ = 'Valuator'


class ValuatorBase(dict, metaclass = ValuatorMeta):
	'''Base class of all IN ValuatorBase.

	'''
	__allowed_children__ = None
	__default_child__ = None

	ops = {
		'=' : lambda l, al, ml: l == al,
		'==' : lambda l, al, ml: l == al,
		'!=' : lambda l, al, ml: l != al,
		'>' : lambda l, al, ml: l > al,
		'<' : lambda l, al, ml: l < al,
		'>=' : lambda l, al, ml: l >= al,
		'<=' : lambda l, al, ml: l <= al,
		'<>' : lambda l, al, ml: al < l > ml,
		'><' : lambda l, al, ml: al > l < ml,
	}

	def validate(self, value):
		'''return value should be a list like [False, 'Error message.'] or [True]
		'''
		return [True]

@IN.register('Valuator', type = 'Valuator')
class Valuator(ValuatorBase):
	'''Base class of all IN ValuatorBase.

	'''
	pass

class And(Valuator):
	pass

class Or(Valuator):
	pass

class Not(Valuator):
	
	def validate(self, value, rule, message = ''):
		'''not validator'''
		result = IN.valuator.validate(value, rule[0])
		not_result = not result[0]
		
		return [not_result, message]

class Empty(Valuator):
	
	def validate(self, value, message = ''):
		# returning value itself makes it evaluates again
		return [False, message] if value else [True]

class Length(Valuator):

	def validate(self, value, length = 0, op = '=', mlength = 0, message = ''):
		try:
			# does multiple ifs are good?
			result = self.ops[op](len(value), length, mlength)
			result = [result or False, message]
			return result
		except KeyError:
			IN.logger.debug()
			return [False, message] # always false

class Equal(Valuator):

	def validate(self, value, tvalue, op = '=', mvalue = 0, message = ''):
		try:
			# does multiple ifs are good?
			result = self.ops[op](value, tvalue, mvalue)
			result = [result or False, message]
			return result
		except KeyError:
			IN.logger.debug()
			return [False, message] # always false


class Regx(Valuator):
	'''Valuator rule class that using regex'''

	re_compiled = {} # we dont want to compile again

	def get_regx(self, regx):
		try:
			return self.re_compiled[regx]
		except KeyError:
			self.re_compiled[regx] = re.compile(regx)
		return self.re_compiled[regx]

	def validate(self, value, regx, message = ''):
		result = self.get_regx(regx).match(value)
		return [result, message]

class Domain(Regx):

	regex_host = r'(?:(?:[a-zA-Z0-9][a-zA-Z0-9\-]*)?[a-zA-Z0-9])'

	def validate(self, domain, message = ''):
		false_message = [False, message]
		dlen = len(domain)
		if dlen < 4 or dlen > 255 or domain.endswith('.') or '.' not in domain:
			return false_message
		try:
			domain = domain.encode('idna').decode('ascii')
		except Exception:
			return false_message
		try:
			domain.encode('ascii').decode('idna')
		except Exception:
			return false_message

		reg = self.regex_host + r'(?:\.' + self.regex_host + r')*'
		m = re.match(reg + "$", domain)
		if not m:
			return false_message

		return [True]

class Email(Regx):

	regex = re.compile(r'^[A-Za-z0-9\.\+_-]')

	atext = r'a-zA-Z0-9_\.\-' # !#\$%&\'\*\+/=\?\^`\{\|\}~
	atext_utf8 = atext + r"\u0080-\U0010FFFF"

	regex_local = re.compile(''.join(('[', atext, ']+(?:\\.[', atext, ']+)*$')))
	regex_local_utf8 = re.compile(''.join(('[', atext_utf8, ']+(?:\\.[', atext_utf8, ']+)*$')))


	def validate(self, value, message = ''):
		parts = value.split('@')
		if len(parts) != 2:
			return [False, message]

		local = self.validate_local(parts[0])
		if not local:
			return [False, message]
		# check domain part
		domain_result = IN.valuator.validate(parts[1], ['Domain', message])
		if not domain_result[0]:
			return domain_result

		return [True] # valid

	def validate_local(self, local):
		# check nabar name part
		if not local or len(local) > 64 or '..' in local:
			return False

		m = re.match(self.regex_local, local) # ASCII
		if m: # True
			return True
		else:
			# unicode
			m = re.match(self.regex_local_utf8, local)
			if m:
				return True
			else:
				return False

class Url(Regx):
	def validate(self, value, message = ''):
		return True

class Alpha(Valuator):
	def validate(self, value, message = ''):
		return [str.isalpha(value), message]

class AlphaNum(Valuator):
	def validate(self, value, message = ''):
		return [str.isalnum(value), message]

class Digit(Valuator):
	def validate(self, value, message = ''):
		return [str.isdigit(value), message]

class Decimal(Valuator):
	def validate(self, value, message = ''):
		return [str.isdecimal(value), message]

class Lower(Valuator):
	def validate(self, value, message = ''):
		return [str.islower(value), message]

class Upper(Valuator):
	def validate(self, value, message = ''):
		return [str.isupper(value), message]

class Numeric(Valuator):
	def validate(self, value, message = ''):
		return [str.isnumeric(value), message]

class Space(Valuator):
	'''Is value has only non printable chars'''
	def validate(self, value, message = ''):
		return [str.isspace(value), message]

class Startswith(Valuator):
	def validate(self, value, start, message = ''):
		return [str(value).startswith(start), message]

class Endswith(Valuator):
	def validate(self, value, start, message = ''):
		return [str(value).endswith(start), message]

class In(Valuator):
	def validate(self, value, itr, message = ''):
		return [value in itr, message]


class INPath(Valuator):
	'''Check whether this string is a valid IN route.'''
	def validate(self, value, message = ''):
		return True

class NabarRole(Valuator):
	'''Check whether nabar has this role.'''
	def validate(self, value, message = ''):
		return True

class NabarAccess(Valuator):
	'''Check whether nabar has this access permissions.'''
	def validate(self, value):
		return True

class Callback(Valuator):
	'''call the Callback to valuate.'''
	def validate(self, value, message = ''):
		return True

#@IN.hook
#def __In_app_init__(app):
	### set the valuator
	#IN.valuator = ValuatorEngine()
