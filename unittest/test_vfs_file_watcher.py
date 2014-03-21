# -*- coding: utf-8 -*-
##j## BOF

"""
UnitTest for dNG.pas.data.Binary
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

from os import path
from shutil import rmtree
from time import sleep
import os
import sys
import unittest

try: from tempfile import TemporaryDirectory
except ImportError:
#
	from tempfile import mkdtemp

	class TemporaryDirectory(object):
	#
		"""
python.org: Create and return a temporary directory.
		"""

		def __init__(self, suffix = "", prefix = "tmp", dir = None):
		#
			"""
Constructor __init__(TemporaryDirectory)
			"""

			self.dir = dir
			self.name = None
			self.prefix = prefix
			self.suffix = suffix
		#

		def __enter__(self):
		#
			"""
python.org: Enter the runtime context related to this object.
			"""

			self.name = mkdtemp(self.suffix, self.prefix, self.dir)
			return self.name
		#

		def __exit__(self, exc, value, tb):
		#
			"""
python.org: Exit the runtime context related to this object.
			"""

			self.cleanup()
		#

		def cleanup(self, _warn = False):
		#
			"""
python.org: The directory can be explicitly cleaned up by calling the cleanup() method.
			"""

			rmtree(self.name)
		#
	#
#

try: from urllib.parse import quote
except ImportError: from urllib import quote

from dNG.data.file import File
from dNG.pas.vfs.file.watcher import Watcher

try: from pyinotify import WatchManager
except ImportError: WatchManager = None

class TestVfsFileWatcher(unittest.TestCase):
#
	def setUp(self):
	#
		"""
Python.org: Hook method for setting up the test fixture before exercising
it.
		"""

		self.changed_list = [ ]
		self.watcher = Watcher()
	#

	def tearDown(self):
	#
		"""
Python.org: Hook method for deconstructing the test fixture after testing
it.
		"""

		if (self.watcher != None): self.watcher.disable()
		self.watcher = None
	#

	def changed_callback(self, event_type, url, changed_value = None):
	#
		"""
Saves callback URLs for later analysis.

:param event_type: Filesystem watcher event type
:param url: Filesystem URL watched
:param changed_value: Changed filesystem value
		"""

		self.changed_list.append({ "event_type": event_type, "url": url, "changed_value": changed_value })
	#

	def process_scenario(self, base_directory, base_url):
	#
		"""
Process a simple scenario.

:param event_type: Filesystem watcher event type
:param url: Filesystem URL watched
:param changed_value: Changed filesystem value
		"""

		self.assertFalse(self.watcher.is_watched(base_url))
		self.watcher.register(base_url, self.changed_callback)
		self.assertTrue(self.watcher.is_watched(base_url))

		unittest_directory = path.normpath("{0}/unittest".format(base_directory))
		unittest_url = base_url + "/unittest"

		os.mkdir(unittest_directory)

		self.assertFalse(self.watcher.is_watched(unittest_url))
		self.watcher.register(unittest_url, self.changed_callback)
		self.assertTrue(self.watcher.is_watched(unittest_url))

		unittest_file = path.normpath("{0}/unittest.txt".format(base_directory))
		unittest_url = base_url + "/unittest.txt"

		self.assertFalse(self.watcher.is_watched(unittest_url))
		self.watcher.register(unittest_url, self.changed_callback)
		self.assertTrue(self.watcher.is_watched(unittest_url))

		_file = File()
		_file.open(unittest_file)
		_file.close(False)
	#

	@unittest.skipIf((WatchManager == None), "pyinotify.WatchManager not usable")
	def test_inotify(self):
	#
		"""
Tests pyinotify ThreadedNotifier
		"""

		self.watcher.set_implementation(Watcher.IMPLEMENTATION_INOTIFY)
		self.assertFalse(self.watcher.is_synchronous())

		with TemporaryDirectory() as base_directory:
		#
			base_url = "file:///{0}".format(quote(base_directory, "/"))
			self.process_scenario(base_directory, base_url)

			# Let the thread process the changes
			sleep(2)
			self.watcher.stop()

			self.assertFalse(self.watcher.is_watched(base_url))
		#

		self.assertEqual(3, len(self.changed_list))

		# mkdir "unittest"
		self.assertEqual(Watcher.EVENT_TYPE_CREATED, self.changed_list[0]['event_type'])
		self.assertEqual(base_url, self.changed_list[0]['url'])
		self.assertEqual("unittest", self.changed_list[0]['changed_value'])

		# create "unittest.txt"
		self.assertEqual(Watcher.EVENT_TYPE_CREATED, self.changed_list[1]['event_type'])
		self.assertEqual(base_url, self.changed_list[1]['url'])
		self.assertEqual("unittest.txt", self.changed_list[1]['changed_value'])

		# modify "unittest.txt"
		self.assertEqual(Watcher.EVENT_TYPE_MODIFIED, self.changed_list[2]['event_type'])
		self.assertEqual("{0}/unittest.txt".format(base_url), self.changed_list[2]['url'])
		self.assertEqual(None, self.changed_list[2]['changed_value'])
	#

	@unittest.skipIf((WatchManager == None), "pyinotify.WatchManager not usable")
	def test_inotify_sync(self):
	#
		"""
Tests pyinotify manually triggered Notifier
		"""

		self.watcher.set_implementation(Watcher.IMPLEMENTATION_INOTIFY_SYNC)
		self.assertTrue(self.watcher.is_synchronous())

		with TemporaryDirectory() as base_directory:
		#
			base_url = "file:///{0}".format(quote(base_directory, "/"))
			self.process_scenario(base_directory, base_url)
			self.watcher.check(base_url + "/unittest.txt")

			self.watcher.stop()

			self.assertFalse(self.watcher.is_watched(base_url))
		#

		self.assertEqual(3, len(self.changed_list))

		# mkdir "unittest"
		self.assertEqual(Watcher.EVENT_TYPE_CREATED, self.changed_list[0]['event_type'])
		self.assertEqual(base_url, self.changed_list[0]['url'])
		self.assertEqual("unittest", self.changed_list[0]['changed_value'])

		# create "unittest.txt"
		self.assertEqual(Watcher.EVENT_TYPE_CREATED, self.changed_list[1]['event_type'])
		self.assertEqual(base_url, self.changed_list[1]['url'])
		self.assertEqual("unittest.txt", self.changed_list[1]['changed_value'])

		# modify "unittest.txt"
		self.assertEqual(Watcher.EVENT_TYPE_MODIFIED, self.changed_list[2]['event_type'])
		self.assertEqual("{0}/unittest.txt".format(base_url), self.changed_list[2]['url'])
		self.assertEqual(None, self.changed_list[2]['changed_value'])
	#

	def test_mtime(self):
	#
		"""
Tests filesystem mtime based, manually triggered check
		"""

		self.watcher = Watcher()
		self.watcher.set_implementation(Watcher.IMPLEMENTATION_MTIME)
		self.assertTrue(self.watcher.is_synchronous())

		with TemporaryDirectory() as base_directory:
		#
			base_url = "file:///{0}".format(quote(base_directory, "/"))
			self.process_scenario(base_directory, base_url)
			self.watcher.check(base_url + "/unittest.txt")

			self.watcher.stop()

			self.assertFalse(self.watcher.is_watched(base_url))
		#

		self.assertEqual(1, len(self.changed_list))

		# modify "unittest.txt"
		self.assertEqual(Watcher.EVENT_TYPE_MODIFIED, self.changed_list[0]['event_type'])
		self.assertEqual("{0}/unittest.txt".format(base_url), self.changed_list[0]['url'])
		self.assertEqual(None, self.changed_list[0]['changed_value'])
	#
#

if (__name__ == "__main__"):
#
	sys.path.append(path.normpath("../src"))
	unittest.main()
#

##j## EOF