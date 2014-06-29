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

from os import path
import sys
import unittest

from dNG.pas.data.binary import Binary
from dNG.pas.data.text.input_filter import InputFilter

class TestDataTextInputFilter(unittest.TestCase):
#
	"""
UnitTest for dNG.pas.data.text.InputFilter

:since: v0.1.01
	"""

	email_addresses = [
		( "test@local.invalid", "test@local.invalid" ),
		( "test@[127.0.0.1]", "test@[127.0.0.1]" ),
		( "test@@local.invalid", "" ),
		( "test@local@invalid", "" ),
		( "test.tester.testing@subdomain.local.invalid", "test.tester.testing@subdomain.local.invalid" ),
		( "test..tester.testing@subdomain.local.invalid", "" ),
		( "test.tester.testing@subdomain.local..invalid", "" ),
		( "\"test@\"@local.invalid", "\"test@\"@local.invalid" ),
		( "\"test@\"@@local.invalid", "" ),
		( "\"test@\"ali\"ba\"@ba@local.invalid", "" ),
		( "\"ali\"ba\"ba@\"@local.invalid", "\"ali\"ba\"ba@\"@local.invalid" ),
		( "\"very.(),:;<>[]\\\".VERY.\\\"very@\\ \\\"very\\\".unusual\"@strange.example.com", "\"very.(),:;<>[]\\\".VERY.\\\"very@\\ \\\"very\\\".unusual\"@strange.example.com" ),
		( Binary.utf8("\"Something with German symbols öäü\"@local.invalid"), "Something%20with%20German%20symbols%20%C3%B6%C3%A4%C3%BC@local.invalid" ), # Not sure about this one
		( Binary.utf8("\"Something with German symbols öäü\"@\"@local.invalid"), "" ),
		( Binary.utf8("test@öäü.de"), "test@xn--4ca9at.de" )
	]
	"""
List of tuples of the form input address, filtered address
	"""

	def test_value(self):
	#
		"""
One key tests everything :)
		"""

		for email_address, result in TestDataTextInputFilter.email_addresses:
		#
			self.assertEqual(
				result,
				InputFilter.filter_email_address(email_address)
			)
		#
	#
#

if (__name__ == "__main__"):
#
	sys.path.append(path.normpath("../src"))
	unittest.main()
#

##j## EOF