import json
import re

from bs4 import BeautifulSoup

from In.core.object_meta import ObjectMetaBase



import textwrap


class TexterMeta(ObjectMeta):

	__class_type_base_name__ = 'TexterBase'
	__class_type_name__ = 'Texter'


class TexterBase(Object, metaclass = TexterMeta):
	'''Base class of all IN TexterBase.

	'''
	
	__allowed_children__ = None
	__default_child__ = None

	__info__ = s('base Texter')

	def format(self, text, config):
		'''format the text and return as text.'''
		return text


@IN.register('Texter', type = 'Texter')
class Texter(TexterBase):
	'''Base class of all IN Texter.

	'''
	__info__ = s('Texter')
	
	def format(self, text, config):
		'''format the text and return as text.'''
		return text

class NewLineToBRTexter(Texter):
	'''convert \n into <br />'''
	
	__info__ = s('NewLine to BR')
	
	def format(self, text, config):
		# TODO: disable if already a html text
		if '/>' not in text and '</' not in text:
			return text.replace('\n', '<br/>')
		else:
			return text

class PlainTextTexter(Texter):
	'''convert \n into <br />'''
	
	__info__ = s('NewLine to BR')
	
	def format(self, text, config):
		soup = BeautifulSoup(text, IN.texter.html_parser)
		return soup.get_text()

class RemoveScriptTexter(Texter):
	'''remove script tags'''
	
	__info__ = s('Remove Script tags')
	
	def format(self, text, config):
		soup = BeautifulSoup(text, IN.texter.html_parser)
		for elem in soup('script'):
			elem.extract()
		return str(soup) # we just need to correct


class RemoveOnEventAttributesTexter(Texter):
	'''remove onclick onload like atributes from tags'''
	
	__info__ = s('Remove on event attributes')
	
	def format(self, text, config):
		soup = BeautifulSoup(text, IN.texter.html_parser)
		for elem in soup.findAll(True):
			for attr in list(elem.attrs.keys()):
				if attr.startswith('on'):
					del elem.attrs[attr]
		return str(soup) # we just need to correct


class FixHTMLTexter(Texter):
	'''convert \n into <br />'''
	
	__info__ = s('Fix HTML')
	
	def format(self, text, config):
		soup = BeautifulSoup(text, IN.texter.html_parser)
		
		return str(soup) # we just need to correct

class URLToLinkTexter(Texter):
	'''convert \n into <br />'''
	
	__info__ = s('Url to Link')
	
	ignore_tags = {'a', 'script', 'style', 'code', 'pre', 'object', 'embed'}
	
	def _format_tag(self, child):
		
		if child.name is None: # string
			output = self._format(str(child))
			
			sub_soup = BeautifulSoup(output, IN.texter.html_parser)
			child.replace_with(sub_soup)

		elif child.name in self.ignore_tags:
			return
		else:
			# recursive format
			for sub_child in child.children:
				self._format_tag(sub_child)
		
	def format(self, text, config):
		# TODO: *speed* CACHE IT
		
		to_change = []
		
		try:
			
			soup = BeautifulSoup(text, IN.texter.html_parser)
			self._format_tag(soup)
			
		except:
			IN.logger.debug()
			
		return str(soup)
		
	
	def _format(self, text):
		_urlfinderregex = re.compile(r'http([^\.\s]+\.[^\.\s]*)+[^\.\s]{2,}')
		
		def replacewithlink(matchobj):
			url = matchobj.group(0)
			
			text_match = url
			
			if text_match.startswith('http://'):
				text_match = text_match.replace('http://', '', 1)
			elif text_match.startswith('https://'):
				text_match = text_match.replace('https://', '', 1)

			if text_match.startswith('www.'):
				text_match = text_match.replace('www.', '', 1)
			
			if text_match.split('/', 1)[0] != IN.APP.config.app_domain:
				return '<a target="_blank" href="' + url + '" >' + text_match + '</a>'
				
			return '<a href="' + url + '" >' + text_match + '</a>'

		if text:
			output = _urlfinderregex.sub(replacewithlink, text)
			return output
		else:
			return ''


class TrimTexter(Texter):
	'''trim text'''
	
	__info__ = s('Trim text')
	
	def format(self, text, config):
		length = config['length']
		
		# very slow
		#return textwrap.shorten(text, width = length, placeholder = " ...")
		
		# may cut at middle of words
		#return (text[:length] + ' ...') if len(text) > length else text
		
		# seems ok
		return ' '.join(text[:length+1].split(' ')[0:-1]) + ' ...' if len(text) > length else text


class IncludeEntityTexter(Texter):
	'''include any entity'''
	
	__info__ = s('Include any Entity')
	
	ignore_tags = {'a', 'script', 'style', 'code', 'pre', 'object', 'embed'}
	
	def _format_tag(self, child):
		
		if child.name is None: # string
			output = self._format(str(child))
			
			sub_soup = BeautifulSoup(output, IN.texter.html_parser)
			child.replace_with(sub_soup)

		elif child.name in self.ignore_tags:
			return
		else:
			# recursive format
			for sub_child in child.children:
				self._format_tag(sub_child)
		
	def format(self, text, config):
		# TODO: *speed* CACHE IT
		
		to_change = []
		
		try:
			
			soup = BeautifulSoup(text, IN.texter.html_parser)
			self._format_tag(soup)
			
		except:
			IN.logger.debug()
			
		return str(soup)
		
	
	def _format(self, text):
		_urlfinderregex = re.compile(r'\[\[(#include )[\s\S]+\]\]')
		
		def replacewith_entity(matchobj):
			sub_text = matchobj.group(0)
			
			# TODO: prevent recursive theming
			
			'''
			[[#include {
				"type" : 'File',
				"id" : "30231",
				"view_mode" : "default"
			}]]
			'''
			
			sub_text = sub_text[11:-2] #.replace('[[#include', '', 1)
			
			try:
				entity_args = json.loads(sub_text)
				
				# return if no type and id
				if 'entity_type' in entity_args and 'entity_id' in entity_args:
				
					entity_type = entity_args['entity_type']
					entity_id = int(entity_args['entity_id'])
					
					entity = IN.entitier.load_single(entity_type, entity_id)
					
					if not entity:
						return ''
						
					view_mode = 'default'
					if 'view_mode' in entity_args:
						view_mode = entity_args['view_mode']
						
					entity_themed = IN.themer.theme(entity, view_mode = view_mode)
					
					return entity_themed
					
				if 'type' in entity_args:
					
					base_type = 'Object'
					if 'base_type' in entity_args:
						base_type = entity_args['base_type']
			
					# get the type class
					objclass = IN.register.get_class(args['type'], base_type)
					if not objclass:
						return ''
						
					obj = objclass(**entity_args)
					
					obj_themed = IN.themer.theme(obj, view_mode = view_mode)
					
					return obj_themed
					
				return ''
				
			except Exception as e:
				IN.logger.debug()
				
			return ''

		if text:
			output = _urlfinderregex.sub(replacewith_entity, text)
			return output
		else:
			return ''


class RemoveIncludeEntityTexter(Texter):
	'''remove include entity tags'''
	
	__info__ = s('remove Include Entity scripts')
	
	ignore_tags = {'a', 'script', 'style', 'code', 'pre', 'object', 'embed'}
	
	def _format_tag(self, child):
		
		if child.name is None: # string
			output = self._format(str(child))
			
			sub_soup = BeautifulSoup(output, IN.texter.html_parser)
			child.replace_with(sub_soup)

		elif child.name in self.ignore_tags:
			return
		else:
			# recursive format
			for sub_child in child.children:
				self._format_tag(sub_child)
		
	def format(self, text, config):
		# TODO: *speed* CACHE IT
		
		to_change = []
		
		try:
			
			soup = BeautifulSoup(text, IN.texter.html_parser)
			self._format_tag(soup)
			
		except:
			IN.logger.debug()
			
		return str(soup)
		
	
	def _format(self, text):
		_urlfinderregex = re.compile(r'\[\[(#include )[\s\S]+\]\]')
		
		def replacewith_entity(matchobj):
			'''
			[[#include ]]
			'''
			
			return ''
			

		if text:
			output = _urlfinderregex.sub(replacewith_entity, text)
			return output
		else:
			return ''

'''

	$ignore_tags = 'a|script|style|code|pre';

  // Pass length to regexp callback.
  _filter_url_trim(NULL, $filter->settings['filter_url_length']);

  // Create an array which contains the regexps for each type of link.
  // The key to the regexp is the name of a function that is used as
  // callback function to process matches of the regexp. The callback function
  // is to return the replacement for the match. The array is used and
  // matching/replacement done below inside some loops.
  $tasks = array();

  // Prepare protocols pattern for absolute URLs.
  // check_url() will replace any bad protocols with HTTP, so we need to support
  // the identical list. While '//' is technically optional for MAILTO only,
  // we cannot cleanly differ between protocols here without hard-coding MAILTO,
  // so '//' is optional for all protocols.
  // @see filter_xss_bad_protocol()
  $protocols = variable_get('filter_allowed_protocols', array('ftp', 'http', 'https', 'irc', 'mailto', 'news', 'nntp', 'rtsp', 'sftp', 'ssh', 'tel', 'telnet', 'webcal'));
  $protocols = implode(':(?://)?|', $protocols) . ':(?://)?';

  // Prepare domain name pattern.
  // The ICANN seems to be on track towards accepting more diverse top level
  // domains, so this pattern has been "future-proofed" to allow for TLDs
  // of length 2-64.
  $domain = '(?:[A-Za-z0-9._+-]+\.)?[A-Za-z]{2,64}\b';
  $ip = '(?:[0-9]{1,3}\.){3}[0-9]{1,3}';
  $auth = '[a-zA-Z0-9:%_+*~#?&=.,/;-]+@';
  $trail = '[a-zA-Z0-9:%_+*~#&\[\]=/;?!\.,-]*[a-zA-Z0-9:%_+*~#&\[\]=/;-]';

  // Prepare pattern for optional trailing punctuation.
  // Even these characters could have a valid meaning for the URL, such usage is
  // rare compared to using a URL at the end of or within a sentence, so these
  // trailing characters are optionally excluded.
  $punctuation = '[\.,?!]*?';

  // Match absolute URLs.
  $url_pattern = "(?:$auth)?(?:$domain|$ip)/?(?:$trail)?";
  $pattern = "`((?:$protocols)(?:$url_pattern))($punctuation)`";
  $tasks['_filter_url_parse_full_links'] = $pattern;

  // Match e-mail addresses.
  $url_pattern = "[A-Za-z0-9._-]{1,254}@(?:$domain)";
  $pattern = "`($url_pattern)`";
  $tasks['_filter_url_parse_email_links'] = $pattern;

  // Match www domains.
  $url_pattern = "www\.(?:$domain)/?(?:$trail)?";
  $pattern = "`($url_pattern)($punctuation)`";
  $tasks['_filter_url_parse_partial_links'] = $pattern;

  // Each type of URL needs to be processed separately. The text is joined and
  // re-split after each task, since all injected HTML tags must be correctly
  // protected before the next task.
  foreach ($tasks as $task => $pattern) {
    // HTML comments need to be handled separately, as they may contain HTML
    // markup, especially a '>'. Therefore, remove all comment contents and add
    // them back later.
    _filter_url_escape_comments('', TRUE);
    $text = preg_replace_callback('`<!--(.*?)-->`s', '_filter_url_escape_comments', $text);

    // Split at all tags; ensures that no tags or attributes are processed.
    $chunks = preg_split('/(<.+?>)/is', $text, -1, PREG_SPLIT_DELIM_CAPTURE);
    // PHP ensures that the array consists of alternating delimiters and
    // literals, and begins and ends with a literal (inserting NULL as
    // required). Therefore, the first chunk is always text:
    $chunk_type = 'text';
    // If a tag of $ignore_tags is found, it is stored in $open_tag and only
    // removed when the closing tag is found. Until the closing tag is found,
    // no replacements are made.
    $open_tag = '';

    for ($i = 0; $i < count($chunks); $i++) {
      if ($chunk_type == 'text') {
        // Only process this text if there are no unclosed $ignore_tags.
        if ($open_tag == '') {
          // If there is a match, inject a link into this chunk via the callback
          // function contained in $task.
          $chunks[$i] = preg_replace_callback($pattern, $task, $chunks[$i]);
        }
        // Text chunk is done, so next chunk must be a tag.
        $chunk_type = 'tag';
      }
      else {
        // Only process this tag if there are no unclosed $ignore_tags.
        if ($open_tag == '') {
          // Check whether this tag is contained in $ignore_tags.
          if (preg_match("`<($ignore_tags)(?:\s|>)`i", $chunks[$i], $matches)) {
            $open_tag = $matches[1];
          }
        }
        // Otherwise, check whether this is the closing tag for $open_tag.
        else {
          if (preg_match("`<\/$open_tag>`i", $chunks[$i], $matches)) {
            $open_tag = '';
          }
        }
        // Tag chunk is done, so next chunk must be text.
        $chunk_type = 'text';
      }
    }

    $text = implode($chunks);
    // Revert back to the original comment contents
    _filter_url_escape_comments('', FALSE);
    $text = preg_replace_callback('`<!--(.*?)-->`', '_filter_url_escape_comments', $text);
  }

  return $text;


'''
