#coding=utf-8

from __future__ import print_function
import os
import sys
import datetime
import shutil

import sqlalchemy

from cuckoo.core.database import Task
from cuckoo.common.config import config
from cuckoo.misc import cwd

from cuckoo.core.database import Database


def cuckoo_clean_storage(days_before):
    print("正在清理 %d 日前数据" % days_before)
    analysis_path = os.path.join(cwd(root=True), "storage", "analyses")

    today = datetime.date.today()
    target_date = today - datetime.timedelta(days=days_before)

    db = Database()
    db.connect(schema_check=False)
    session = db.Session()
    try:
        tasks = session.query(Task).filter(Task.added_on<target_date).order_by(Task.id).all()
        for task in tasks:
            task_path = os.path.join(analysis_path, str(task.id))
            print("正在删除目录 %s" % task_path)
            shutil.rmtree(task_path)
    except Exception as e:
        print("error")
    finally:
        session.close()

