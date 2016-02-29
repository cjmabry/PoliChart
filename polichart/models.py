# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from extensions import db
from utils import get_current_time, SEX_TYPE, STRING_LEN

class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = Column(db.Integer, primary_key=True)

    last_name = Column(db.String(STRING_LEN), nullable=False)
    first_name = Column(db.String(STRING_LEN))
    pledged_delegates = Column(db.Integer(), default=0)
    unpledged_delegates = Column(db.Integer(), default=0)
    total_delegates = Column(db.Integer(), default=0)
    projected_pledged_delegates = Column(db.Float(), default=0)
    projected_unpledged_delegates = Column(db.Float(), default=0)
    projected_total_delegates = Column(db.Float(), default=0)

class Poll(db.Model):
    __tablename__ = 'polls'

    id = Column(db.Integer, primary_key=True)

    state = Column(db.String(3), nullable=False, unique=False)
    clinton = Column(db.Float(), nullable=False)
    sanders = Column(db.Float(), nullable=False)
    undecided = Column(db.Float(), nullable=False)
    date = db.Column(db.DateTime)

class State(db.Model):
    __tablename__ = 'states'

    id = Column(db.Integer, primary_key=True)

    state = Column(db.String(3), nullable=False, unique=False)
    pledged_available = Column(db.Integer())
    unpledged_available = Column(db.Integer())
    total_available = Column(db.Integer())
    clinton_percentage = Column(db.Float())
    sanders_percentage = Column(db.Float())
    clinton_delegates = Column(db.Integer())
    sanders_delegates = Column(db.Integer())
    clinton_percentage_results = Column(db.Float())
    sanders_percentage_results = Column(db.Float())
    clinton_pledged_delegates_results = Column(db.Integer())
    sanders_pledged_delegates_results = Column(db.Integer())
    clinton_unpledged_delegates_results = Column(db.Integer())
    sanders_unpledged_delegates_results = Column(db.Integer())
    url = Column(db.String(STRING_LEN))
    election_date = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime)

class Daily(db.Model):
    __tablename__ = 'daily'

    id = Column(db.Integer, primary_key=True)

    state = Column(db.String(3), nullable=False)
    date = db.Column(db.DateTime)
    clinton_percentage = Column(db.Float())
    sanders_percentage = Column(db.Float())
