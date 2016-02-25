# -*- coding: utf-8 -*-

from uuid import uuid4

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)
from flask.ext.mail import Message
from flask.ext.babel import gettext as _
from flask.ext.login import login_required, login_user, current_user, logout_user, confirm_login, login_fresh

from ..user import User, UserDetail
from ..extensions import db, mail, login_manager, oid
from .forms import SignupForm, LoginForm, RecoverPasswordForm, ReauthForm, ChangePasswordForm, OpenIDForm, CreateProfileForm


frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    current_app.logger.debug('debug')

    page = int(request.args.get('page', 1))
    pagination = User.query.paginate(page=page, per_page=10)
    return render_template('index.html', pagination=pagination)

@frontend.route('/help')
def help():
    return render_template('frontend/footers/help.html', active="help")
