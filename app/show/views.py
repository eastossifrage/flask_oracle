# -*- coding:utf-8 -*-
__author__ = '东方鹗'
__blog__ = 'http://www.os373.cn'

from .. import db
from . import show
from .forms import LoginForm, SearchForm
from flask import render_template, abort, redirect, request, current_app, url_for, flash, json, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from ..models import OusiStaff, OusiGuest, AlchemyJsonEncoder
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import aliased
from datetime import date
import os
from collections import OrderedDict
from config import basedir
from pyexcel_xls import save_data, get_data


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


@show.route('/01', methods = ['GET', 'POST'])
@login_required
def _01():
    search_form = SearchForm(prefix='search')
    g1 = aliased(OusiGuest)
    g2 = aliased(OusiGuest)
    page = request.args.get('page', 1, type=int)
    if current_user.role == 'admin':
        database = db.session.query(OusiStaff.department, OusiStaff.name.label('staff_name'), OusiStaff.phone,
                                    OusiStaff.role,
                                    g1.name.label('guest_name'), g1.month, g1.balance,
                                    func.nvl(db.session.query(g2.balance).filter(
                                        g1.name==g2.name,
                                        func.to_date(g2.month, 'yyyy-mm')==func.add_months(
                                            func.to_date(g1.month, 'yyyy-mm'), -1)
                                    ), 0).label('last_balance')
                                    ).filter(
            OusiStaff.phone==g1.staff_phone, current_user.department==OusiStaff.department,
            g1.month==date.today().strftime('%Y-%m')
        ).order_by(g1.name).group_by(OusiStaff.department, OusiStaff.name.label('staff_name'), OusiStaff.phone,
                                     OusiStaff.role,
                                     g1.name.label('guest_name'), g1.month, g1.balance)
        if search_form.validate_on_submit():
            database = db.session.query(OusiStaff.department, OusiStaff.name.label('staff_name'), OusiStaff.phone,
                                        OusiStaff.role,
                                        g1.name.label('guest_name'), g1.month, g1.balance,
                                        func.nvl(db.session.query(g2.balance).filter(
                                            g1.name==g2.name,
                                            func.to_date(g2.month, 'yyyy-mm')==func.add_months(
                                                func.to_date(g1.month, 'yyyy-mm'), -1)
                                        ), 0).label('last_balance')
                                        ).filter(
                OusiStaff.phone == g1.staff_phone, current_user.department==OusiStaff.department,
                and_(g1.month.between(search_form.start_time.data.strip(), search_form.end_time.data.strip()),
                     OusiStaff.name.like('%{}%'.format(search_form.name.data.strip())),
                     OusiStaff.phone.like('%{}%'.format(search_form.phone.data.strip())))
            ).order_by(g1.name).group_by(OusiStaff.department, OusiStaff.name.label('staff_name'), OusiStaff.phone,
                                         OusiStaff.role,
                                         g1.name.label('guest_name'), g1.month, g1.balance)
    else:
        database = db.session.query(OusiStaff.department, OusiStaff.name.label('staff_name'), OusiStaff.phone,
                                    OusiStaff.role,
                                    g1.name.label('guest_name'), g1.month, g1.balance,
                                    func.nvl(db.session.query(g2.balance).filter(
                                        g1.name==g2.name,
                                        func.to_date(g2.month, 'yyyy-mm')==func.add_months(
                                            func.to_date(g1.month, 'yyyy-mm'), -1)
                                    ), 0).label('last_balance')
                                    ).filter(
            OusiStaff.phone==g1.staff_phone, current_user.phone==g1.staff_phone,
            g1.month==date.today().strftime('%Y-%m')
            ).order_by(g1.name).group_by(OusiStaff.department, OusiStaff.name.label('staff_name'), OusiStaff.phone,
                                    OusiStaff.role,
                                    g1.name.label('guest_name'), g1.month, g1.balance)
        if search_form.validate_on_submit():
            database = db.session.query(OusiStaff.department, OusiStaff.name.label('staff_name'), OusiStaff.phone,
                                        OusiStaff.role,
                                        g1.name.label('guest_name'), g1.month, g1.balance,
                                        func.nvl(db.session.query(g2.balance).filter(
                                            g1.name == g2.name,
                                            func.to_date(g2.month, 'yyyy-mm') == func.add_months(
                                                func.to_date(g1.month, 'yyyy-mm'), -1)
                                        ), 0).label('last_balance')
                                        ).filter(
                OusiStaff.phone == g1.staff_phone, current_user.phone == OusiStaff.phone,
                g1.month.between(search_form.start_time.data.strip(), search_form.end_time.data.strip())
            ).order_by(g1.name).group_by(OusiStaff.department, OusiStaff.name.label('staff_name'), OusiStaff.phone,
                                         OusiStaff.role,
                                         g1.name.label('guest_name'), g1.month, g1.balance)
    data = database.paginate(page, per_page=current_app.config['OUSI_POSTS_PER_PAGE'], error_out=False)

    return render_template('show/01.html', data=data, searchForm=search_form, database=json.dumps(database, cls=AlchemyJsonEncoder))


@show.route('/02', methods = ['GET', 'POST'])
@login_required
def _02():
    search_form = SearchForm(prefix='search')
    page = request.args.get('page', 1, type=int)
    g1 = aliased(OusiGuest)
    g2 = aliased(OusiGuest)
    if current_user.role == 'admin':
        sbq = db.session.query(OusiStaff.department, OusiStaff.role, OusiStaff.name.label('staff_name'),
                               g1.staff_phone, g1.name.label('guest_name'), g1.month, g1.balance,
                               func.nvl(db.session.query(g2.balance).filter(
                                   g1.name==g2.name,
                                   func.add_months(func.to_date(g1.month, 'yyyy-mm'), -1) == func.to_date(g2.month,
                                                                                                          'yyyy-mm')
                                                                             ), 0).label('last_balance')).filter(
            OusiStaff.phone==g1.staff_phone,
            OusiStaff.department==current_user.department
        ).group_by(OusiStaff.department, OusiStaff.role, OusiStaff.name.label('staff_name'),
                               g1.staff_phone, g1.name.label('guest_name'), g1.month, g1.balance).subquery()
        database = db.session.query(sbq.c.department, sbq.c.role, sbq.c.staff_name, sbq.c.staff_phone,
                                    sbq.c.month, func.count(sbq.c.guest_name).label('members'),
                                    func.sum(sbq.c.balance).label('balance'), func.sum(sbq.c.last_balance).label('last_balance')).\
            filter(sbq.c.month==date.today().strftime('%Y-%m')).group_by(sbq.c.department, sbq.c.role,
                                                                         sbq.c.staff_name, sbq.c.staff_phone,
                                                                         sbq.c.month)
        if search_form.validate_on_submit():
            database = db.session.query(sbq.c.department, sbq.c.role, sbq.c.staff_name, sbq.c.staff_phone,
                                        sbq.c.month, func.count(sbq.c.guest_name).label('members'),
                                        func.sum(sbq.c.balance).label('balance'),
                                        func.sum(sbq.c.last_balance).label('last_balance')). \
                filter(and_(sbq.c.month.between(search_form.start_time.data.strip(), search_form.end_time.data.strip()),
                            sbq.c.staff_name.like('%{}%'.format(search_form.name.data.strip())),
                            sbq.c.staff_phone.like('%{}%'.format(search_form.phone.data.strip())))
                       ).group_by(sbq.c.department, sbq.c.role,
                                                                               sbq.c.staff_name, sbq.c.staff_phone,
                                                                               sbq.c.month)
    else:
        sbq = db.session.query(OusiStaff.department, OusiStaff.role, OusiStaff.name.label('staff_name'),
                               g1.staff_phone, g1.name.label('guest_name'), g1.month, g1.balance,
                               func.nvl(db.session.query(g2.balance).filter(
                                   g1.name == g2.name,
                                   func.add_months(func.to_date(g1.month, 'yyyy-mm'), -1) == func.to_date(g2.month,
                                                                                                          'yyyy-mm')
                               ), 0).label('last_balance')).filter(
            OusiStaff.phone == g1.staff_phone,
            OusiStaff.phone == current_user.phone
        ).group_by(OusiStaff.department, OusiStaff.role, OusiStaff.name.label('staff_name'),
                   g1.staff_phone, g1.name.label('guest_name'), g1.month, g1.balance).subquery()
        database = db.session.query(sbq.c.department, sbq.c.role, sbq.c.staff_name, sbq.c.staff_phone,
                                    sbq.c.month, func.count(sbq.c.guest_name).label('members'),
                                    func.sum(sbq.c.balance).label('balance'),
                                    func.sum(sbq.c.last_balance).label('last_balance')). \
            filter(sbq.c.month == date.today().strftime('%Y-%m')).group_by(sbq.c.department, sbq.c.role,
                                                                           sbq.c.staff_name, sbq.c.staff_phone,
                                                                           sbq.c.month)
        if search_form.validate_on_submit():
            database = db.session.query(sbq.c.department, sbq.c.role, sbq.c.staff_name, sbq.c.staff_phone,
                                        sbq.c.month, func.count(sbq.c.guest_name).label('members'),
                                        func.sum(sbq.c.balance).label('balance'),
                                        func.sum(sbq.c.last_balance).label('last_balance')). \
                filter(sbq.c.month.between(search_form.start_time.data.strip(),
                                           search_form.end_time.data.strip())).group_by(sbq.c.department, sbq.c.role,
                                                                               sbq.c.staff_name, sbq.c.staff_phone,
                                                                               sbq.c.month)
    data = database.paginate(page, per_page=current_app.config['OUSI_POSTS_PER_PAGE'], error_out=False)

    return render_template('show/02.html', data=data, searchForm=search_form, database=json.dumps(database, cls=AlchemyJsonEncoder))


excel_path = os.path.join(basedir, 'app/show/static/excel_files/')

@show.route('/<path:filename>', methods=['GET', 'POST'])
def download_xls(filename):
    data = OrderedDict()
    data_path = os.path.join(excel_path, filename)

    num = 0
    if '01.xls' in filename:
        header_data = ['序号', '部门', '角色', '员工', '电话', '客户', '月份',
                       '本月资产余额	', '上月资产余额', '新增余额']
        body_data = [header_data]
        for t in json.loads(request.get_data()):
            num += 1
            body_data.append([num, t["department"], t["role"], t["staff_name"], t["phone"], t["guest_name"],
                              t["month"], t["balance"], t["last_balance"],
                              float('%.2f' % t["balance"]) - float('%.2f' % t["last_balance"])])
        data.update({'01报表': body_data})

    if '02.xls' in filename:
        header_data = ['序号', '部门', '角色', '员工', '电话', '月份', '管户数'
                       '本月资产余额	', '上月资产余额', '新增余额']
        body_data = [header_data]
        for t in json.loads(request.get_data()):
            num += 1
            body_data.append([num, t["department"], t["role"], t["staff_name"], t["staff_phone"],
                              t["month"], t["balance"], t["last_balance"],
                              float('%.2f' % t["balance"]) - float('%.2f' % t["last_balance"])])
        data.update({'02报表': body_data})
    save_data(data_path, data)
    return jsonify({"data": "ok"})


@show.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('show.login'))