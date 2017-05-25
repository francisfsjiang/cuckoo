# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2016 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import shlex

from lib.common.abstracts import Package

class PHP(Package):
    """Python analysis package."""

    PATHS = [
        ("HomeDrive", "PHP7", "php.exe"),
    ]

    def start(self, path):
        php = self.get_path("PHP")
        arguments = self.options.get("arguments", "")

        args = [path] + shlex.split(arguments)
        return self.execute(php, args=args, trigger="file:%s" % path)
