# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasCoreVersion)#
#echo(__FILEPATH__)#
"""

from threading import Thread as PyThread

from dNG.pas.data.logging.log_line import LogLine

class Thread(PyThread):
#
	"""
"Thread" represents a deactivatable Thread implementation.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	_active = True
	"""
True if new non-daemon threads are allowed to be started.
	"""

	def run(self):
	#
		"""
python.org: Method representing the thread’s activity.

:since: v0.1.01
		"""

		# pylint: disable=broad-except

		try: PyThread.run(self)
		except Exception as handled_exception: LogLine.error(handled_exception, context = "pas_core")
	#

	def start(self):
	#
		"""
python.org: Start the thread's activity.

:since: v0.1.01
		"""

		if (self.daemon or Thread._active): PyThread.start(self)
		else: LogLine.debug("{0!r} prevented new non-daemon thread", self, context = "pas_core")
	#

	@staticmethod
	def set_inactive():
	#
		"""
Prevents new non-daemon threads to be started.

:since: v0.1.00
		"""

		Thread._active = False
	#
#

##j## EOF