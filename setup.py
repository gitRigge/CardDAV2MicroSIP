# The MIT License (MIT)
# 
# Copyright (c) 2015, Roland Rickborn (r_2@gmx.net)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Revision history:
# 2015-09-30  Created
# ---------------------------------------------------------------------------

from distutils.core import setup
import py2exe, sys, os
__author__ = 'Roland Rickborn'

sys.argv.append('py2exe')

setup(name='CardDAV2MicroSIP',
    version='1.0',
    description='A bridge from cardDAV to the VoIP client MicroSIP',
    author='Roland Rickborn',
    author_email='r_2@gmx.net',
    url='https://github.com/gitRigge/CardDAV2MicroSIP',
    options = {'py2exe': {'bundle_files': 1, 'compressed': True, 'optimize': 2}},
    windows = [{'script': 'bridge.py'}],
    zipfile = None,
)