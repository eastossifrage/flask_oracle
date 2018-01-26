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


class AlchemyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # 判断是否是Query
        if isinstance(obj, Query):
            # 定义一个字典数组
            fields = []
            # 检索结果集的行记录
            for rec in obj:
                # 定义一个字典对象
                record = {}
                # 检索记录中的成员
                for field in [x for x in dir(rec) if
                              # 过滤属性
                              not x.startswith('_')
                              # 过滤掉方法属性
                              and hasattr(rec.__getattribute__(x), '__call__') == False
                              # 过滤掉不需要的属性
                              and x != 'metadata']:
                    try:
                        record[field] = rec.__getattribute__(field)
                    except TypeError:
                        record[field] = None
                fields.append(record)
            # 返回字典数组
            return fields
        # 其他类型的数据按照默认的方式序列化成JSON
        return json.JSONEncoder.default(self, obj)
