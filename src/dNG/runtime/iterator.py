# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
#echo(__FILEPATH__)#
"""

try: from collections.abc import Iterator as _Iterator
except ImportError: from collections import Iterator as _Iterator

class Iterator(_Iterator):
    """
"Iterator" provides an iterator class that is compatible with Python 2.x and
newer.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def next(self):
        """
python.org: Return the next item from the container. (Python 2.x)

:return: (object) Result object
:since:  v1.0.0
        """

        # pylint: disable=no-member

        return self.__next__()
    #
#
