# -*- coding:utf-8 -*-
__author__ = '东方鹗'
__blog__ = u'http://www.os373.cn'

import os
from app import create_app, db
from app.models import OusiStaff, OusiGuest
from flask_script import Manager, Shell


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app=app)


def make_shell_context():
    return dict(app=app, db=db, OusiStaff=OusiStaff, OusiGuest=OusiGuest)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
    # app.run(host='0.0.0.0', port=5000, debug=False)
