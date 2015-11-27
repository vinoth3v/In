# Copyright (c) Vinoth Kanyakumari vinoth.3v@gmail.com
#
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

__author__      = 'Vinoth Kanyakumari (vinoth.3v@gmail.com)'
__copyright__   = 'Copyright Vinoth Kanyakumari'

import builtins
builtins.builtins = builtins  #recursive

builtins.__In_globals_dict__ = globals()


import In.core.bootstrap