import sys

if sys.version < '3.4':
	raise RuntimeError('IN requires python version 3.4')

import asyncio
import greenlet

#import aioredis

# YES It is builtins


import pprint as cprint

printobj = cprint.PrettyPrinter(indent = 1)

def _pprint(*args):
	for o in args:
		printobj.pprint(o)

builtins.pprint = _pprint




def s(text, args = None, lc = '', language = 'ta'):
	'''
	This is the wrapper function for i18n strings.

	i18n module will replace this function.
	'''
	if args is None:
		args = {}

	#text = str(text)

	return text.format_map(args)


builtins.s = s #i18n will override



'''system_boot
'''
#sys.tracebacklimit = 5
import In.core.__In__

# In module namespace

builtins.In = In.core.__In__.__INModuleNamespace__()
builtins.In.__dict__ = __In_globals_dict__

# IN Object
builtins.IN = In.core.__In__.IN()

import In.core.logger as logger
In.logger = logger
IN.logger = logger.Logs()

import In.core.util as util
In.util = util

import In.core.object_meta
import In.core.object

import In.core.context
In.context = In.core.context

import In.themer

import In.core.http as http

In.http = http


import In.core.application

import In.html
import In.core.page
import In.core.action
import In.core.access

import In.db

import In.core.access

import In.core.lazy

import In.former

import In.entity
import In.field

import In.nabar


import In.stringer

import In.file
import In.image
import In.core.valuator
import In.core.cacher
import In.boxer
import In.core.token_verification

import In.texter
import In.tasker

import In.vakai

import In.content
import In.comment
import In.profile
import In.activity


import In.mailer

import In.flag

IN.register.process_registers()

In.application = In.core.application

In.page = In.core.page
In.action = In.core.action

import In.core.request
import In.core.response

import In.search
import In.status

#print('load_system_Addons start : ' , datetime.datetime.now(), '<br/>')

# load core modules
# APP level Addons will be loaded in APP init


In.access = In.core.access

IN.register.process_registers()

IN.hook_invoke('In_pre_system_init')

IN.hook_invoke('In_system_init')



