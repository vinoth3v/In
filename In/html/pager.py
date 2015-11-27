import json

class Pager(HTMLObject):
	
	# default load more text
	url = ''
	
	# current page index starting from 1
	current_page = 1
	
	# total number of pages
	total_page = 0
	
	link_ajax_args = None
	
	def __init__(self, data = None, items = None, **args):
		
		super().__init__(data, items, **args)
		
		self.css.append('i-pagination i-text-center')
	

@IN.register('Pager', type = 'Themer')
class PagerThemer(HTMLObjectThemer):
	''''''
	
class PagerLoadMore(Pager):

	def __init__(self, data = None, items = None, **args):
		
		self.page_title = 'Page {current_page}'
		
		super().__init__(data, items, **args)
		
		if not self.value:
			self.value = s('load more')# + str(self.current_page)
		

@IN.register('PagerLoadMore', type = 'Themer')
class PagerLoadMoreThemer(PagerThemer):
	
	def theme_items(self, obj, format, view_mode, args):
		
		next_page = obj.current_page + 1

		url = ''.join(('/', obj.url, '?page=', str(next_page)))
		
		o = obj.add('Link', {
			'href' : url,
			'value' : obj.value,
			'css' : ['no-scroll'],
			'attributes' : {
				'data-ajax_type' : 'POST',
			}
		})
		
		if obj.link_ajax_args:
			ajax_args = json.dumps(obj.link_ajax_args, skipkeys = True, ensure_ascii = False)
			o.attributes['data-ajax_args'] = ajax_args
		
		obj.value = ''
		
		super().theme_items(obj, format, view_mode, args)
		


class PagerPrevNext(Pager):
	
	def __init__(self, data = None, items = None, **args):
		
		self.prev = 'previous'
		self.next = 'next'
		
		super().__init__(data, items, **args)
		
@IN.register('PagerPrevNext', type = 'Themer')
class PagerPrevNextThemer(PagerThemer):
	
	merge_children = False
	
	def theme_items(self, obj, format, view_mode, args):
		
		if obj.current_page > 1:
			prev_index = obj.current_page - 1
			
			if prev_index > 1:
				url = ''.join(('/', obj.url, '?page=', str(prev_index)))
			else:
				url = '/' + obj.url
			
			v = obj.add('Link', {
				'id' : 'previous',
				'href' : url,
				'value' : '<i class="i-icon-angle-double-left"></i> ' + s(obj.prev),
			})
			if obj.link_ajax_args:
				ajax_args = json.dumps(obj.link_ajax_args, skipkeys = True, ensure_ascii = False)
				v.attributes['data-ajax_args'] = ajax_args
		
		next_index = obj.current_page + 1

		url = ''.join(('/', obj.url, '?page=', str(next_index)))
		
		v = obj.add('Link', {
			'id' : 'next',
			'href' : url,
			'value' : '<i class="i-icon-angle-double-right"></i> ' + s(obj.next),
		})
		if obj.link_ajax_args:
			ajax_args = json.dumps(obj.link_ajax_args, skipkeys = True, ensure_ascii = False)
			v.attributes['data-ajax_args'] = ajax_args
		
		obj.value = ''
		
		super().theme_items(obj, format, view_mode, args)
		
	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		
		if 'previous' in obj:
			args['previous'] = args['children']['previous']['content']
		else:
			args['previous'] = ''
		args['next'] = args['children']['next']['content']



class PagerNumberList(Pager):
	
	def __init__(self, data = None, items = None, **args):
		
		super().__init__(data, items, **args)
		
@IN.register('PagerNumberList', type = 'Themer')
class PagerNumberListThemer(PagerThemer):
	
	def theme_items(self, obj, format, view_mode, args):
		
		url = '/' + obj.url
		current_page = obj.current_page
		total_pages = obj.total_pages
		
		ajax_args = ''
		if obj.link_ajax_args:
			ajax_args = json.dumps(obj.link_ajax_args, skipkeys = True, ensure_ascii = False)
				
		# add current
		c = obj.add('Li', {
			'value' : str(current_page).join(('<span>', '</span>')),
			'css' : ['i-active'],
			'weight' : current_page
		})
		
		# add prev
		prev = current_page - 1
		if prev > 0:
			o = obj.add('Li', {
				'weight' : prev,
			})
			l = o.add('Link', {
				'href' : ''.join((url, '?page=', str(prev))),
				'value' : str(prev),
			})
			if obj.link_ajax_args:
				l.attributes['data-ajax_args'] = ajax_args
		
		
		# add next
		next = current_page + 1
		if next <= total_pages:
			o = obj.add('Li', {
				'weight' : next,
			})
			l = o.add('Link', {
				'href' : ''.join((url, '?page=', str(next))),
				'value' : str(next),
			})
			if obj.link_ajax_args:
				l.attributes['data-ajax_args'] = ajax_args
		
		# add first
		if prev > 1:
			obj.add('Li', {
				'weight': 1,
			}).add('Link', {
				'href' : url,
				'value' : '1',
			})
		
		# add first	next
		if prev > 2:
			o = obj.add('Li', {
				'weight': 2,
			})
			l = o.add('Link', {
				'href' : ''.join(('/', obj.url, '?page=', str(2))),
				'value' : '2',
			})
			if obj.link_ajax_args:
				l.attributes['data-ajax_args'] = ajax_args
		
		
		# add eclipse
		if 3 < prev:
			o = obj.add('Li', {
				'value' : '<span>...</span>',
				'weight' : 3
			})
			
		
		# add last
		if total_pages > next:
			o = obj.add('Li', {
				'weight': total_pages,
			})
			l = o.add('Link', {
				'href' : ''.join(('/', obj.url, '?page=', str(total_pages))),
				'value' : str(total_pages),
			})
			if obj.link_ajax_args:
				l.attributes['data-ajax_args'] = ajax_args
		
		
		# add last prev
		lastprev = total_pages - 1
		if lastprev > next:
			o = obj.add('Li', {
				'weight': lastprev,
			})
			l = o.add('Link', {
				'href' : ''.join(('/', obj.url, '?page=', str(lastprev))),
				'value' : str(lastprev),
			})
			if obj.link_ajax_args:
				l.attributes['data-ajax_args'] = ajax_args
		
		
		# add eclipse
		if lastprev -1 > next:
			o = obj.add('Li', {
				'value' : '<span>...</span>',
				'weight' : lastprev -1
			})
			
		
		super().theme_items(obj, format, view_mode, args)
		

