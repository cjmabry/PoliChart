from pollster import Pollster
from pprint import pprint
from sqlalchemy.sql import and_, or_
import models, csv
from datetime import datetime, timedelta

from extensions import db
from utils import get_current_time, get_current_date

pollster = Pollster()

def populate_states():
    with open('states.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]: {'pledged':rows[1], 'unpledged':rows[2]} for rows in reader}

        for state, delegates in mydict.items():
            if models.State.query.filter(models.State.state==str(state)).first():
                s = models.State.query.filter(models.State.state==state).first()
                s.pledged_available = int(delegates['pledged'])
                s.unpledged_available = int(delegates['unpledged'])
                s.clinton_delegates = int(s.clinton_percentage/100 * s.pledged_available)
                s.sanders_delegates = int(s.sanders_percentage/100 * s.pledged_available)
                db.session.add(s)
                db.session.commit()

def update(state, clinton_percentage, sanders_percentage):
    yesterday = get_current_date() - timedelta(days=1)
    tomorrow = get_current_date() + timedelta(days=1)

    if not models.Daily.query.filter(and_(models.Daily.date > yesterday, models.Daily.date < tomorrow, models.Daily.state == state)).first():
        date = models.Daily(state=state,date=get_current_date(), clinton_percentage=clinton_percentage, sanders_percentage=sanders_percentage)
        db.session.add(date)
        db.session.commit()

def get_polls():

    for chart in pollster.charts(topic='2016-president-dem-primary'):
        state = chart.state

        if len(chart.estimates) > 0:

            for x in chart.estimates:
                if x['choice'] == 'Sanders':
                    sanders = x['value']
                elif x['choice'] == 'Clinton':
                    clinton = x['value']

            update(state=state, clinton_percentage=clinton, sanders_percentage=sanders)

            if not models.State.query.filter(models.State.state==state).first():
                state =  models.State(state=state, clinton_percentage = clinton, sanders_percentage = sanders)
                db.session.add(state)
                db.session.commit()

            else:
                state = models.State.query.filter(models.State.state==state).first()
                state.clinton = clinton
                state.sanders = sanders
                db.session.commit()
