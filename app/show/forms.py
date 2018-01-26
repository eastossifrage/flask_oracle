# -*- coding:utf-8 -*-
__author__ = '东方鹗'
__blog__ = 'http://www.os373.cn'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    name = StringField(u'用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(label=u'记住我', default=False)
    submit = SubmitField(u'登 录')


class SearchForm(FlaskForm):
    name = StringField(u'使用员工')
    phone = StringField(u'手机号')
    start_time = StringField(u'开始时间',  validators=[DataRequired()])
    end_time = StringField(u'结束时间',  validators=[DataRequired()])
    submit = SubmitField(u'搜 索')