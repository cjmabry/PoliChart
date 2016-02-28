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

    get_charts()

    states = models.State.query.all()

    clinton_sum = 0
    sanders_sum = 0
    undecided_sum = 0

    data['states'] = []

    for state in states:
        data['states'].append(state)
        if state.state != 'US':
            if state.clinton_pledged_delegates_results and state.sanders_pledged_delegates_results:
                clinton_sum += int(state.clinton_pledged_delegates_results)
                sanders_sum += int(state.clinton_pledged_delegates_results)
            else:
                clinton_sum += int(state.clinton_percentage * state.pledged_available)
                sanders_sum += int(state.sanders_percentage * state.pledged_available)
                undecided_sum += int(state.pledged_available)

    data['projections'] = {}
    data['candidates'] = {}

    data['projections']['clinton'] = clinton_sum
    data['projections']['sanders'] = sanders_sum
    data['projections']['undecided'] = undecided_sum - (clinton_sum + sanders_sum)

    data['candidates']['clinton'] = models.Candidate.query.filter_by(last_name='Clinton').first()
    data['candidates']['sanders'] = models.Candidate.query.filter_by(last_name='Sanders').first()

    return render_template('index.html', data=data)

@frontend.route('/help')
def help():
    return render_template('frontend/footers/help.html', active="help")
