import sys, string
import time, datetime, calendar
import email.utils
import numbers, random, string
import re, io, hashlib, base64

from functools import *

class OutputCatcher:
	'''Catch all print output.'''

	def __enter__(self):
		self.old_stdout = sys.stdout
		self.new_stdout = io.StringIO()
		self.output_result = ''
		sys.stdout = self.new_stdout
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.output_result = self.new_stdout.getvalue()#
		self.new_stdout.close()
		sys.stdout = self.old_stdout

	def output(self):
		return self.output_result


def ignore_error(func):
	'''Decorator. ignore the errors.'''

	@wraps(func)
	def hook(*args, **kwds):
		try:
			return func(*args, **kwds)
		except Exception:
			IN.logger.debug()
		return

	return hook

def format_timestamp(ts):
	"""Formats a timestamp in the format used by HTTP.

	The argument may be a numeric timestamp as returned by `time.time`,
	a time tuple as returned by `time.gmtime`, or a `datetime.datetime`
	object.

	>>> format_timestamp(1359312200)
	'Sun, 27 Jan 2013 18:43:20 GMT'
	"""
	if isinstance(ts, numbers.Real):
		''''''
	elif isinstance(ts, (tuple, time.struct_time)):
		ts = calendar.timegm(ts)
	elif isinstance(ts, datetime.datetime):
		ts = calendar.timegm(ts.utctimetuple())
	else:
		raise TypeError("unknown timestamp type: %r" % ts)
	return email.utils.formatdate(ts, usegmt=True)


def raw_eval(source, g=globals(), l=globals(), err='IN.logger'):
	ret = ''
	#ret = eval(source, g, l)
	try:
		ret = eval(source, g, l)
	except Exception as e:
		IN.logger.debug()

	return ret


def raw_exec(source, g=globals(), l=globals(), err='IN.logger'):
	try:
		exec(source, g, l)

	except Exception as e:
		IN.logger.debug()

__to_seconds__ = {
	'year' : lambda value: 3.15569e7 * value,
	'month' : lambda value: 2.62974e6 * value,
	'week' : lambda value: 604800.0 * value,
	'day' : lambda value: 86400.0 * value,
	'hour' : lambda value: 3600.0 * value,
	'minute' : lambda value: 60.0 * value,
	'second' : lambda value: float(value),
}

def to_seconds(type, value):
	'''Convert value to seconds.'''
	try:
		return __to_seconds__[type](value)
	except:
		return 0

def format_datetime_friendly(date_time_arg):
	
	now = datetime.datetime.now()
	
	diff = now - date_time_arg
	second_diff = diff.seconds
	
	day_diff = diff.days

	if now.day == date_time_arg.day:
		return date_time_arg.strftime("%I:%M %p")
	
	if day_diff < 28:
		return date_time_arg.strftime("%a %d") # Tue 12
	
	if day_diff < 365:
		return date_time_arg.strftime("%b, %a %d") #Aug Tue 12
	
	return date_time_arg.strftime("%b, %a %d, %Y")
	
	#Tue, Tuesday, August 04 , 2015 10:18 AM
	#%a,  %A,		%B 	   %d , %Y 	 %I:%M %p
	
# Calculate a Drupal 7 compatible password hash.

class DrupalHash:
	'''Allows to login using drupal generated password.'''

	bytes_decode_type = 'replace'

	def __init__(self):
		self.itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
		self.min_log = 7
		self.max_log = 30
		self.default_log = 15
		self.hash_length = 55

	def password_get_count_log2(self, setting):
		return self.itoa64.index(setting[3])

	def password_crypt(self, algo, password, setting):
		setting = setting[0:12]
		if setting[0] != '$' or setting[2] != '$':
			return False

		count_log2 = self.password_get_count_log2(setting)
		salt = setting[4:12]
		if len(salt) < 8:
			return False
		count = 1 << count_log2

		if algo == 'md5':
			hash_func = hashlib.md5
		elif algo == 'sha512':
			hash_func = hashlib.sha512
		else:
			return False

		pwd = salt + password
		pwd = pwd.encode('utf-8')
		passencode = password.encode('utf-8')

		pwd = hash_func(pwd).digest()

		for c in range(count):
			pwd = pwd + passencode
			pwd = hash_func(pwd).digest()

		output = setting + self.custom64(pwd.decode('ISO-8859-1', self.bytes_decode_type)) #

		return output[0:self.hash_length]

	def custom64(self, string, count = 0):
		if count == 0:
			count = len(string)

		output = []

		i = 0
		itoa64 = self.itoa64
		while 1:
			value = ord(string[i])

			i += 1
			output.append(itoa64[value & 0x3f])
			if i < count:
				value |= ord(string[i]) << 8

			output.append(itoa64[(value >> 6) & 0x3f])
			if i >= count:
				break
			i += 1
			if i < count:
				value |= ord(string[i]) << 16
			output.append(itoa64[(value >> 12) & 0x3f])
			if i >= count:
				break
			i += 1
			output.append(itoa64[(value >> 18) & 0x3f])
			if i >= count:
			   break
		return ''.join(output)

	def rehash(self, stored_hash, password):
		# Drupal 6 compatibility
		if len(stored_hash) == 32 and stored_hash.find('$') == -1:
			return hashlib.md5(password).hexdigest()
		# Drupal 7
		if stored_hash[0:2] == 'U$':
			stored_hash = stored_hash[1:]
			password = hashlib.md5(password).hexdigest()
		hash_type = stored_hash[0:3]
		if hash_type == '$S$':
			hash_str = self.password_crypt('sha512', password, stored_hash)
		elif hash_type == '$H$' or hash_type == '$P$':
			hash_str = self.password_crypt('md5', password, stored_hash)
		else:
			hash_str = False
		return hash_str

	def password_generate_salt(self, count_log2):
		output = '$S$'
		count_log2 = self._password_enforce_log2_boundaries(count_log2)
		output += self.itoa64[count_log2]
		output += self.custom64(self._random_string(6), 6)
		return output

	def hash(self, password, count_log2 = 0):
		if count_log2 == 0:
			count_log2 = self.default_log
		return self.password_crypt('sha512', password, self.password_generate_salt(count_log2))

	def _password_enforce_log2_boundaries(self, count_log2):
		if count_log2 < self.min_log:
			return self.min_log
		if count_log2 > self.max_log:
			return self.max_log
		return count_log2

	def _random_string(self, length):
		r = random.SystemRandom()
		chars = string.ascii_letters + string.digits
		return ''.join(r.choice(chars) for _ in range(length))

class RDict(dict):
	'''Recursive Dict to deep merge'''
	
	def update(self, source, **extra):
		self.__update__(source)
		if extra:
			self.__update__(extra)
		
	def __update__(self, source):
		for key, value in source.items():
			if key in self and isinstance(value, dict):
				self[key] = RDict(self[key])
				self[key].update(value)
			else:
				self[key] = value

builtins.RDict = RDict
