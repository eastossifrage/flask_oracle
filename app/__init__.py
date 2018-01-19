# -*- coding:utf-8 -*-
__author__ = '东方鹗'
__blog__ = u'http://www.os373.cn'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """ 使用工厂函数初始化程序实例"""
    app = Flask(__name__, template_folder="templates")

    app.config.from_object(config[config_name])
    config[config_name].init_app(app=app)

    db.init_app(app=app)
    login_manager.init_app(app=app)

    # 注册蓝本 show
    from .show import show as show_blueprint
    app.register_blueprint(show_blueprint, url_prefix='/show')

    return app
