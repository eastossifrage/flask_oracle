# -*- coding:utf-8 -*-
__author__ = '东方鹗'
__blog__ = 'http://www.os373.cn'


from . import db
from flask_login import UserMixin, AnonymousUserMixin, current_user
from . import login_manager
from datetime import date
from sqlalchemy import extract, and_, or_
from sqlalchemy.orm.query import Query
from collections import OrderedDict
from pyexcel_xls import get_data
import json


@login_manager.user_loader
def load_user(user_id):
    return OusiStaff.query.get(int(user_id))


class OusiStaff(UserMixin, db.Model):
    __tablename__ = 'ousi_staff'
    sid = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(8))
    name = db.Column(db.String(8))
    password = db.Column(db.String(8))
    phone = db.Column(db.String(11))
    role = db.Column(db.String(8))

    @property
    def id(self):
        return self.sid

    def verify_password(self, password):
        return self.password == password

    def is_admin(self):  # 自行定义的方法,用于权限判断
        return self.role == 'admin'


class AnonymousUser(AnonymousUserMixin):
    '''
    继承至该类的用户模型 将作为未登陆时的用户模型,可以保持代码的一致性。
    '''
    def is_admin(self): # 自行定义的方法,用于权限判断
        return False


login_manager.anonymous_user = AnonymousUser


class OusiGuest(db.Model):
    __tablename__ = 'ousi_guest'
    id = db.Column(db.Integer, primary_key=True)
    staff_phone = db.Column(db.String(11))
    name = db.Column(db.String(8))
    month = db.Column(db.String(8))
    balance = db.Column(db.Integer)
