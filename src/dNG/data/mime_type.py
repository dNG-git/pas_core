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

from weakref import ref
import mimetypes

from dNG.runtime.instance_lock import InstanceLock

from .cache.json_file_content import JsonFileContent
from .logging.log_line import LogLine
from .settings import Settings

class MimeType(object):
    """
Provides mime type related methods on top of Python basic ones.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    _weakref_instance = None
    """
MimeType weakref instance
    """
    _weakref_lock = InstanceLock()
    """
Thread safety weakref lock
    """

    def __init__(self):
        """
Constructor __init__(MimeType)

:since: v1.0.0
        """

        self.definitions = None
        """
Mime type definitions
        """
        self.extensions = { }
        """
Mime type extension list
        """
    #

    def get(self, extension = None, mimetype = None):
        """
Returns the mime type definition. Either extension or mime type can be
looked up.

:param extension: Extension to look up
:param mimetype: Mime type to look up

:return: (dict) Mime type definition
:since:  v1.0.0
        """

        _return = None

        if (extension is not None):
            extension = (extension[1:].lower() if (extension[:1] == ".") else extension.lower())

            if (extension in self.extensions and self.extensions[extension] in self.definitions):
                _return = self.definitions[self.extensions[extension]]
                if ("type" not in _return): _return['type'] = self.extensions[extension]
            else:
                mimetype = mimetypes.guess_type("file.{0}".format(extension), False)[0]
                if (mimetype is not None): _return = { "type": mimetype, "extension": extension, "class": mimetype.split("/")[0] }
            #

            if (mimetype is not None and mimetype != _return['type']): _return = None
        elif (mimetype is not None):
            mimetype = mimetype.lower()

            if (mimetype in self.definitions):
                _return = self.definitions[mimetype]
                if ("type" not in _return): _return['type'] = mimetype
            elif (mimetypes.guess_extension(mimetype, False) is not None): _return = { "type": mimetype, "class": mimetype.split("/")[0] }
        #

        return _return
    #

    def get_extensions(self, mimetype):
        """
Returns the list of extensions known for the given mime type.

:param mimetype: Mime type to return the extensions for.

:return: (list) Extensions
:since:  v1.0.0
        """

        _return = [ ]

        if (mimetype is not None or mimetype in self.definitions):
            _return = self.definitions[mimetype].get("extensions", [ ])
            if (type(_return) is not list): _return = [ _return ]
        #

        return _return
    #

    def refresh(self):
        """
Refresh all mime type definitions from the file.

:since: v1.0.0
        """

        json_data = JsonFileContent.read("{0}/settings/core_mimetypes.json".format(Settings.get("path_data")))

        if (type(json_data) is dict):
            aliases = { }
            self.definitions = { }
            self.extensions = { }

            for mimetype in json_data:
                if ("type" in json_data[mimetype]): aliases[mimetype] = json_data[mimetype]['type']
                else:
                    self.definitions[mimetype] = json_data[mimetype].copy()

                    if ("class" not in json_data[mimetype]):
                        _class = mimetype.split("/", 1)[0]
                        self.definitions[mimetype]['class'] = (_class if (_class not in json_data or "class" not in json_data[_class]) else json_data[_class]['class'])
                    #

                    if (type(json_data[mimetype].get("extensions")) is list):
                        for extension in json_data[mimetype]['extensions']:
                            if (extension not in self.extensions): self.extensions[extension] = mimetype
                            else: LogLine.warning("Extension '{0}' declared for more than one mime type", self.extensions[extension], context = "pas_core")
                        #
                    elif ("extension" in json_data[mimetype]):
                        if (json_data[mimetype]['extension'] not in self.extensions): self.extensions[json_data[mimetype]['extension']] = mimetype
                        else: LogLine.warning("Extension '{0}' declared for more than one mime type", self.extensions[json_data[mimetype]['extension']], context = "pas_core")
                    #
                #
            #

            for mimetype in aliases:
                if (mimetype not in self.definitions and aliases[mimetype] in self.definitions):
                    self.definitions[mimetype] = self.definitions[aliases[mimetype]]
                    self.definitions[mimetype]['type'] = aliases[mimetype]
                #
            #
        #
    #

    @staticmethod
    def get_instance():
    #
        """
Get the MimeType singleton.

:return: (MimeType) Object on success
:since:  v1.0.0
        """

        _return = None

        with MimeType._weakref_lock:
            if (MimeType._weakref_instance is not None): _return = MimeType._weakref_instance()

            if (_return is None):
                _return = MimeType()
                _return.refresh()

                MimeType._weakref_instance = ref(_return)
            #
        #

        return _return
    #
#
