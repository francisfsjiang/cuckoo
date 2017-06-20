# Copyright (C) 2016-2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import re
import datetime
import os

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

import bson
import pymongo

from cuckoo.core.database import Database
from cuckoo.common.mongo import mongo
from cuckoo.web.controllers.analysis.export.export import ExportController
from cuckoo.web.controllers.analysis.analysis import AnalysisController
from cuckoo.web.utils import view_error, render_template

class AnalysisRoutes:
    @staticmethod
    def recent(request):
        return render_template(request, "analysis/index.html")

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

    @staticmethod
    def export(request, task_id):
        if request.method == "POST":
            taken_dirs = request.POST.getlist("dirs")
            taken_files = request.POST.getlist("files")

            try:
                zip = ExportController.create(task_id=task_id,
                                              taken_dirs=taken_dirs,
                                              taken_files=taken_files)

                response = HttpResponse(zip.getvalue(), content_type="application/zip")
                response["Content-Disposition"] = "attachment; filename=%s.zip" % task_id
                return response

            except Exception as e:
                return view_error(request, str(e))

        report = AnalysisController.get_report(task_id)

        if "analysis_path" not in report.get("analysis", {}).get("info", {}):
            return view_error(request, "The analysis was created before the export "
                                       "functionality was integrated with Cuckoo and is "
                                       "therefore not available for this task (in order to "
                                       "export this analysis, please reprocess its report).")

        analysis_path = report["analysis"]["info"]["analysis_path"]
        dirs, files = ExportController.get_files(analysis_path)
        return render_template(request, "analysis/export.html",
                               report=report, dirs=dirs, files=files)

    @staticmethod
    def reboot(request, task_id):
        task_obj = Database().add_reboot(task_id=task_id)
        return render_template(request, "submission/reboot.html",
                               task_id=task_id, task_obj=task_obj,
                               baseurl=request.build_absolute_uri("/")[:-1])


    @staticmethod
    def recent_page(request):

        doc_filter = []

        filter_cat = []

        if request.GET.get("filter-file", "off") == "on":
            filter_cat.append({"info.category": "file"})
        if request.GET.get("filter-url", "off") == "on":
            filter_cat.append({"info.category": "url"})
        if len(filter_cat) == 2:
            doc_filter.append({"$or": filter_cat})
        elif len(filter_cat) == 1:
            doc_filter.append(filter_cat[0])

        filter_score = []
        if request.GET.get("filter-low", "off") == "on":
            filter_score.append({"info.score": {"$gte": 0, "$lt": 4}})
        if request.GET.get("filter-medium", "off") == "on":
            filter_score.append({"info.score": {"$gte": 4, "$lt": 7}})
        if request.GET.get("filter-high", "off") == "on":
            filter_score.append({"info.score": {"$gte": 7, "$lte": 10}})
        if len(filter_score) >= 2:
            doc_filter.append({"$or": filter_score})
        elif len(filter_score) == 1:
            doc_filter.append(filter_score[0])

        if len(doc_filter) == 2:
            doc_filter = {"$and": doc_filter}
        elif len(doc_filter) == 1:
            doc_filter = doc_filter[0]
        else:
            doc_filter = {}
        print doc_filter

        cursor = mongo.db.analysis.find(
            doc_filter,
            ["info", "target"]
        ).sort("info.id", pymongo.ASCENDING).limit(5)

        class Analysis:
            def __init__(self):
                pass

        analysis_list = []
        for analysis in cursor:

            info = analysis.get("info", {})
            target = analysis.get("target", {})
            category = info.get("category")
            if category == "file":
                f = target.get("file", {})
                if f.get("name"):
                    target_name = os.path.basename(f["name"])
                else:
                    target_name = None
                target_type = f.get("type", "Not detected")
                md5 = f.get("md5") or "-"
            elif category == "url":
                target_name = target.get("url", "-")
                target_type = "URL"
                md5 = "-"
            elif category == "archive":
                target_name = target.get("human", "-")
                target_type = "Archive"
                md5 = "-"
            else:
                target_name = "-"
                target_type = "Not Detected"
                md5 = "-"

            a = Analysis()
            a.id = info.get("id", "-")
            a.date = info.get("added", "-")
            if type(a.date) == datetime.datetime:
                a.date = a.date.isoformat(' ')
            a.md5 = md5
            a.file_name = target_name
            a.type = target_type
            a.score = info.get("score", 0.0)
            analysis_list.append(a)

        return render(request, "analysis/index_page.html", context={"analysis_list": analysis_list})
        # return render_template(request, "analysis/index_page.html", context={"analysis_list": analysis_list})
