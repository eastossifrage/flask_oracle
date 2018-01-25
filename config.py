# -*- coding:utf-8 -*-
__author__ = u'东方鹗'
__blog__ = u'http://www.os373.cn'

import os
import hashlib

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 5 # 指定数据库连接池的超时时间。默认是10s。
    SQLALCHEMY_POOL_RECYCLE = 3000 # 配置连接池的 recyle 时间。默认是7200s。
    SECRET_KEY = os.environ.get('SECRET_KEY') or hashlib.new(name='md5', string='ousi keji hawk@#').hexdigest()
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    OUSI_POSTS_PER_PAGE = 20


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                            'oracle+cx_oracle://xxpost:%s@172.21.204.170:1521/orcl' % 'xxpost3710806#'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
