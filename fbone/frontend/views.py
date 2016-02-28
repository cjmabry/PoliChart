# -*- coding: utf-8 -*-

from uuid import uuid4

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)
from flask.ext.mail import Message
from flask.ext.babel import gettext as _
from flask.ext.login import login_required, login_user, current_user, logout_user, confirm_login, login_fresh

from ..extensions import db

from ..polling import *

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    current_app.logger.debug('debug')

    data = {}

    get_polls()

    states = models.State.query.all()

    clinton_sum = 0
    sanders_sum = 0
    undecided_sum = 0

    data['states'] = []

    for state in states:
        data['states'].append(state)
        if state.state != 'US':
            clinton_sum += int(state.clinton_percentage * state.pledged_available)
            sanders_sum += int(state.sanders_percentage * state.pledged_available)
            undecided_sum += int(state.pledged_available)

    data['projections'] = {}

    data['projections']['clinton'] = clinton_sum
    data['projections']['sanders'] = sanders_sum
    data['projections']['undecided'] = undecided_sum - (clinton_sum + sanders_sum)

    return render_template('index.html', data=data)

@frontend.route('/help')
def help():
    return render_template('frontend/footers/help.html', active="help")
