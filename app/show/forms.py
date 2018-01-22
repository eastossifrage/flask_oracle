# -*- coding:utf-8 -*-
__author__ = u'东方鹗'
__blog__ = u'http://www.os373.cn'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    name = StringField(u'用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(label=u'记住我', default=False)
    submit = SubmitField(u'登 录')