# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.runtime.Thread
"""
"""n// NOTE
----------------------------------------------------------------------------
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
----------------------------------------------------------------------------
NOTE_END //n"""

import threading

from dNG.pas.data.logging.log_line import LogLine

class Thread(threading.Thread):
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
	synchronized = threading.RLock()
	"""
Lock used in multi thread environments.
	"""

	def start(self):
	#
		"""
python.org: Start the thread's activity.

:since: v0.1.01
		"""

		with Thread.synchronized:
		#
			if (self.daemon or Thread._active): threading.Thread.start(self)
			else: LogLine.debug("pas.core.Thread prevented new non-daemon thread")
		#
	#

	@staticmethod
	def set_inactive():
	#
		"""
Prevents new non-daemon threads to be started.

:since: v0.1.00
		"""

		with Thread.synchronized: Thread._active = False
	#
#

##j## EOF