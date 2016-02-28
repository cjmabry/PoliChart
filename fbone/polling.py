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
        mydict = {rows[0]: {'pledged':rows[1], 'unpledged':rows[2], 'date': rows[4]} for rows in reader}

        for state, delegates in mydict.items():
            s = models.State(state=state)
            s.pledged_available = int(delegates['pledged'])
            s.unpledged_available = int(delegates['unpledged'])

            try:
                s.election_date = datetime.strptime(delegates['date'], '%m/%d/%Y')
            except ValueError as e:
                print delegates['date']

            s.total_available = s.pledged_available + s.unpledged_available
            s.clinton_percentage = 0
            s.sanders_percentage = 0
            s.clinton_delegates = 0
            s.sanders_delegates = 0
            s.last_updated = get_current_time()
            db.session.add(s)
            db.session.commit()

    get_charts()

def get_charts():

    for chart in pollster.charts(topic='2016-president-dem-primary'):
        state = chart.state

        if len(chart.estimates) > 0:

            for x in chart.estimates:
                if x['choice'] == 'Sanders':
                    sanders = x['value']/100
                elif x['choice'] == 'Clinton':
                    clinton = x['value']/100

            update(state=state, clinton_percentage=clinton, sanders_percentage=sanders)

            if not models.State.query.filter(models.State.state==state).first():
                state =  models.State(state=state, clinton_percentage = clinton, sanders_percentage = sanders, url = chart.url)
                state.clinton_delegates = clinton * state.pledged_available
                state.sanders_delegates = sanders * state.pledged_available
                db.session.add(state)
                db.session.commit()

            else:
                state = models.State.query.filter(models.State.state==state).first()
                state.clinton = clinton
                state.sanders = sanders
                state.clinton_percentage = clinton
                state.sanders_percentage = sanders
                state.clinton_delegates = clinton * state.pledged_available
                state.sanders_delegates = sanders * state.pledged_available
                state.url = chart.url
                db.session.commit()

def update(state, clinton_percentage, sanders_percentage):
    yesterday = get_current_date() - timedelta(days=1)
    tomorrow = get_current_date() + timedelta(days=1)

    if not models.Daily.query.filter(and_(models.Daily.date > yesterday, models.Daily.date < tomorrow, models.Daily.state == state)).first():
        date = models.Daily(state=state,date=get_current_date(), clinton_percentage=clinton_percentage, sanders_percentage=sanders_percentage)
        db.session.add(date)
        db.session.commit()
