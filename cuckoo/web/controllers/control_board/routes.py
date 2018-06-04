# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import re
import datetime
import os
import json
import subprocess

from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

import bson
import pymongo

from cuckoo.core.database import Database
from cuckoo.common.mongo import mongo
from cuckoo.web.controllers.analysis.export.export import ExportController
from cuckoo.web.controllers.analysis.analysis import AnalysisController
from cuckoo.web.utils import view_error, render_template


class ControlBoardRoutes:
    @staticmethod
    def index(request):
        return render_template(request, "control_board/index.html")

    @staticmethod
    def reboot_sys(request):
        output = ControlBoardRoutes.execute(["reboot"])
        return render_template(request, "control_board/index.html", error=output)

    @staticmethod
    def reboot(request):
        output = ControlBoardRoutes.execute(["systemctl", "restart", "imcs.service"])
        return render_template(request, "control_board/index.html", error=output)

    @staticmethod
    def reboot_web(request):
        output = ControlBoardRoutes.execute(["systemctl", "restart", "imcs_web.service"])
        return render_template(request, "control_board/index.html", error=output)

    @staticmethod
    def reboot_database(request):
        output = ControlBoardRoutes.execute(["systemctl", "restart", "mysql.service"])
        output = ControlBoardRoutes.execute(["systemctl", "restart", "mongodb.service"])
        return render_template(request, "control_board/index.html", error=output)

    @staticmethod
    def clean(request):
        days = int(request.POST.get("days"))
        # output = ControlBoardRoutes.execute(["systemctl", "restart", "imcs"])
        output = ControlBoardRoutes.execute([
            "/usr/bin/python", "/home/imcs/cuckoo/cuckoo.py",
            "--cwd", "/home/imcs/cuckoo/cwd/", "clean_storage",
            "-d", "%d" % days
        ])
        return render_template(request, "control_board/index.html", error=output)

    @staticmethod
    def execute(args):
        base_command = []+args
        try:
            print(base_command)
            output = subprocess.check_output(base_command)
            print(output)
            return "执行成功"
        except subprocess.CalledProcessError as e:
            print(e.output)
            return "执行错误"

    @staticmethod
    def detail(request, task_id, page):
        report = AnalysisController.get_report(task_id)

        pages = {
            "summary": "summary/index",
            "static": "static/index",
            "extracted": "extracted/index",
            "behavior": "behavior/index",
            "network": "network/index",
            "misp": "misp/index",
            "dropped_files": "dropped/dropped_files",
            "dropped_buffers": "dropped/dropped_buffers",
            "memory": "memory/index",
            "procmemory": "procmemory/index",
            "options": "options/index",
            "feedback": "feedback/index"
        }

        if page in pages.keys():
            return render_template(
                request, "analysis/pages/%s.html" % pages[page],
                report=report, page=page
            )
        else:
            return view_error(
                request, msg="Analysis subpage not found", status=404
            )

    @staticmethod
    def redirect_default(request, task_id):
        if not isinstance(task_id, (unicode, str)):
            task_id = str(task_id)

        return redirect(reverse(
            "analysis",
            args=(re.sub(r"\^d+", "", task_id), "summary")),
            permanent=False
        )

