# Copyright (C) 2013 Claudio Guarnieri.
# Copyright (C) 2014-2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from django.conf.urls import url

from cuckoo.web.controllers.control_board.routes import ControlBoardRoutes

urlpatterns = [
    url(r"^$", ControlBoardRoutes.index, name="control_board/index"),
    url(r"^reboot_sys$", ControlBoardRoutes.reboot_sys, name="control_board/reboot_sys"),
    url(r"^reboot$", ControlBoardRoutes.reboot, name="control_board/reboot"),
    url(r"^reboot_web$", ControlBoardRoutes.reboot_web, name="control_board/reboot_web"),
    url(r"^reboot_database$", ControlBoardRoutes.reboot_database, name="control_board/reboot_database"),
    url(r"^clean$", ControlBoardRoutes.clean, name="control_board/clean"),
]
