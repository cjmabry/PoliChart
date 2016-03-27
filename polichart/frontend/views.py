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
    clinton_result_sum = 0
    sanders_result_sum = 0
    undecided_result_sum = 0
    undecided_sum = 0
    clinton_projected = 0
    sanders_projected = 0
    undecided_projected = 0

    data['states'] = []

    for state in states:
        data['states'].append(state)
        if state.state != 'US':
            clinton_projected += round(state.clinton_percentage * (state.pledged_available), 0)
            sanders_projected += round(state.sanders_percentage * (state.pledged_available), 0)
            undecided_projected += state.pledged_available - (round(state.clinton_percentage * state.pledged_available, 0) + round(state.sanders_percentage * state.pledged_available, 0))

            if not state.clinton_pledged_delegates_results or not state.sanders_pledged_delegates_results:
                clinton_sum += round(state.clinton_percentage * (state.pledged_available), 0)
                sanders_sum += round((state.sanders_percentage * (state.pledged_available)), 0)
                undecided_sum += state.pledged_available - (round(state.clinton_percentage * state.pledged_available, 0) + round(state.sanders_percentage * state.pledged_available, 0))

            else:
                clinton_result_sum += round(state.clinton_pledged_delegates_results,0)
                sanders_result_sum += round(state.sanders_pledged_delegates_results,0)

    clinton_total_sum = clinton_sum + clinton_result_sum
    sanders_total_sum = sanders_sum + sanders_result_sum

    data['projections'] = {}
    data['combined'] = {}
    data['candidates'] = {}

    data['projections']['clinton'] = clinton_projected
    data['projections']['sanders'] = sanders_projected
    data['projections']['undecided'] = undecided_projected

    data['combined']['clinton'] = clinton_total_sum
    data['combined']['sanders'] = sanders_total_sum

    data['combined']['undecided'] = undecided_sum

    data['candidates']['clinton'] = models.Candidate.query.filter_by(last_name='Clinton').first()
    data['candidates']['sanders'] = models.Candidate.query.filter_by(last_name='Sanders').first()

    return render_template('index.html', data=data)

@frontend.route('/interactives/bern-path')
def bernPath():
    return render_template('layouts/bern-path.html')
