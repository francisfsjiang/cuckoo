#coding=utf-8

from __future__ import print_function
import os
import sys
import datetime

import sqlalchemy

from cuckoo.core.database import Task
from cuckoo.common.config import config

from cuckoo.core.database import Database

CUCKOO_CWD = ""


def cuckoo_clean_storage(days_before):
    print("正在清理 %d 日前数据" % days_before)
    analysis_path = os.path.join(CUCKOO_CWD, "storage", "analyses")
    print(analysis_path)

    today = datetime.date.today()
    print(today)
    target_date = today - datetime.timedelta(days=days_before)
    print(target_date)

    db = Database()
    db.connect(schema_check=False)
    session = db.Session()
    try:
        tasks = session.query(Task).filter(Task.started_on).order_by(Task.id).all()
    except Exception as e:
        print("error")
    else:
        for task in tasks:
            print(task)
    finally:
        session.close()

