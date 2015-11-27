from .form import *

@IN.hook
def actions():
	actns = {}

	actns['search'] = {
		'title' : 'Search',
		'handler' : search_page,
	}

	actns['search/{query}'] = {
		'title' : 'Search',
		'handler' : search_page,
	}

	return actns

def search_page(context, action, query = '', **args):

	
	page = context.response.output
	
	#page.add(frm)


class ObjectSearch(Object):

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)

		self.form = self.add('Form')

		self.textbox = self.form.add(
			type = 'TextBox',
			title = 'Search',
			weight = 1,
			value = 'Type here...',
			#required = "true",
			trim = "true",
			width = 30,
			valuenow = 'Type here',
			id = 'search_box',
			#cssclass='float-left'
		)

		self.searchbutton = self.form.add(
			type = 'Submit',
			value = 'Go',
			weight = 2,
		)



def site_search():
	return ObjectSearch()

def site_search_configure(mode): #view | validate | save | reset
	pass
