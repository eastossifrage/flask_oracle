# -*- coding:utf-8 -*-
__author__ = u'东方鹗'
__blog__ = u'http://www.os373.cn'

from .. import db
from . import show
from .forms import LoginForm
from flask import render_template, abort, redirect, request, current_app, url_for, flash, json, jsonify, send_from_directory
from flask_login import login_required, login_user, logout_user
from ..models import OusiStaff, OusiGuest


@show.route('/', methods = ['GET', 'POST'])
@show.route('/index', methods = ['GET', 'POST'])
@login_required
def index():

    return render_template('show/index.html')


@show.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = LoginForm(prefix='login')
    if login_form.validate_on_submit():
        u = OusiStaff.query.filter_by(name=login_form.name.data.strip()).first()
        if u is None:
            flash({'error': u'用户名未注册！'})
        elif u and u.verify_password(login_form.password.data.strip()):
            login_user(user=u, remember=login_form.remember_me.data)
            return  redirect(request.args.get('next') or url_for('show.index'))
        elif u and not u.verify_password(login_form.password.data.strip()):
            flash({'error': u'密码错误！'})
        else:
            abort(403)

    return render_template('show/login.html', loginForm=login_form)