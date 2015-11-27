
from .tags import *
from .tags_themer import *
from .menu import *
from .pager import *
from .object_lister import *

def divider(text):
	output = ''.join(('''
<div class="i-grid i-container i-vertical-align">
	<div class="i-width-4-10 i-vertical-align-middle"><hr></div>
	<div class="i-container-center i-vertical-align-middle"><h2>''', text, '''</h2></div>
	<div class="i-width-4-10 i-vertical-align-middle"><hr></div>
</div>'''))
	return output
