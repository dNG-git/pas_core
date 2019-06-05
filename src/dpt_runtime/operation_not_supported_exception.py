# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;runtime

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(dptRuntimeVersion)#
#echo(__FILEPATH__)#
"""

from .traced_exception import _TracedException

class OperationNotSupportedException(_TracedException):
    """
This exception should be used if specific API calls or parameter values are
not supported in a given implementation.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, value = "Operation not supported", _exception = None):
        """
Constructor __init__(OperationNotSupportedException)

:param value: Exception message value
:param _exception: Inner exception

:since: v1.0.0
        """

        _TracedException.__init__(self, value, _exception)
    #
#
