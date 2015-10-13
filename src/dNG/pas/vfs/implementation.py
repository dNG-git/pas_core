# -*- coding: utf-8 -*-
##j## BOF

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

from dNG.pas.data.binary import Binary
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.io_exception import IOException
from .abstract import Abstract

class Implementation(object):
#
	"""
"Implementation" provides implementation independent methods to access VFS
objects.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.03
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	TYPE_DIRECTORY = Abstract.TYPE_DIRECTORY
	"""
Directory (or collection like) type
	"""
	TYPE_FILE = Abstract.TYPE_FILE
	"""
File type
	"""
	TYPE_LINK = Abstract.TYPE_LINK
	"""
Link type
	"""

	@staticmethod
	def get_class(scheme):
	#
		"""
Returns an VFS object class for the given scheme.

:return: (object) VFS object class
:since:  v0.1.03
		"""

		_return = NamedLoader.get_class("dNG.pas.vfs.{0}.Object".format(scheme.replace("-", "_")))

		if (_return is None
		    or (not issubclass(_return, Abstract))
		   ): raise IOException("VFS object not defined for URI scheme '{0}'".format(scheme))

		return _return
	#

	@staticmethod
	def get_instance(scheme):
	#
		"""
Returns an VFS object instance for the given scheme.

:return: (object) VFS object instance
:since:  v0.1.03
		"""

		vfs_object_class = Implementation.get_class(scheme)
		return vfs_object_class()
	#

	@staticmethod
	def load_vfs_uri(vfs_uri, readonly = False):
	#
		"""
Returns the initialized object instance for the given VFS URI.

:param vfs_uri: VFS URI
:param readonly: Open object in readonly mode

:return: (object) VFS object instance
:since:  v0.1.03
		"""

		vfs_uri = Binary.str(vfs_uri)
		scheme = Abstract._get_scheme_from_vfs_uri(vfs_uri)

		_return = Implementation.get_instance(scheme)
		_return.open(vfs_uri, readonly)

		return _return
	#

	@staticmethod
	def new_vfs_uri(_type, vfs_uri):
	#
		"""
Returns a new object instance for the given VFS URI.

:param _type: VFS object type
:param vfs_uri: VFS URI

:return: (object) VFS object instance
:since:  v0.1.03
		"""

		vfs_uri = Binary.str(vfs_uri)
		scheme = Abstract._get_scheme_from_vfs_uri(vfs_uri)

		_return = Implementation.get_instance(scheme)
		_return.new(_type, vfs_uri)

		return _return
	#
#

##j## EOF