from pollster import Pollster
from pprint import pprint
from sqlalchemy.sql import and_, or_
import models, csv
from datetime import datetime, timedelta

from extensions import db
from utils import get_current_time, get_current_date

pollster = Pollster()

def populate_db():
    with open('data/states.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]: {'pledged':rows[1], 'unpledged':rows[2], 'date': rows[4]} for rows in reader}

        for state, delegates in mydict.items():
            s = models.State(state=state)
            s.pledged_available = int(delegates['pledged'])
            s.unpledged_available = int(delegates['unpledged'])

            try:
                s.election_date = datetime.strptime(delegates['date'], '%m/%d/%Y')
            except ValueError as e:
                print 439750983246709479074092760974092764097460927903467
                print delegates['date']

            s.total_available = s.pledged_available + s.unpledged_available
            s.clinton_percentage = 0
            s.sanders_percentage = 0
            s.clinton_delegates = 0
            s.sanders_delegates = 0
            s.last_updated = get_current_time()
            db.session.add(s)
            db.session.commit()

    clinton = models.Candidate(last_name='Clinton', first_name='Hillary')
    sanders = models.Candidate(last_name='Sanders', first_name='Bernie')

    db.session.add(clinton)
    db.session.add(sanders)
    db.session.commit()

    get_charts()
    get_results()

def get_results():
    with open('data/results.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]: {'clinton_pledged':rows[1], 'clinton_unpledged':rows[2], 'sanders_pledged':rows[3], 'sanders_unpledged':rows[4], 'clinton_percentage':rows[5], 'sanders_percentage':rows[6]} for rows in reader}

        clinton = models.Candidate.query.filter_by(last_name='Clinton').first()
        sanders = models.Candidate.query.filter_by(last_name='Sanders').first()

        for state, results in mydict.items():
            if models.State.query.filter_by(state=state).first():
                s = models.State.query.filter_by(state=state).first()
                s.last_updated = get_current_time()
                s.clinton_pledged_delegates_results = int(results['clinton_pledged'])
                s.sanders_pledged_delegates_results = int(results['sanders_pledged'])
                s.clinton_unpledged_delegates_results = int(results['clinton_unpledged'])
                s.sanders_unpledged_delegates_results = int(results['sanders_unpledged'])
                db.session.add(s)

                s.clinton_percentage_results = float(results['clinton_percentage'])
                s.sanders_percentage_results = float(results['sanders_percentage'])

            clinton.pledged_delegates += int(results['clinton_pledged'])
            clinton.unpledged_delegates += int(results['clinton_unpledged'])
            sanders.pledged_delegates += int(results['sanders_pledged'])
            sanders.unpledged_delegates += int(results['sanders_unpledged'])

        clinton.total_delegates = clinton.pledged_delegates + clinton.unpledged_delegates
        sanders.total_delegates = sanders.pledged_delegates + sanders.unpledged_delegates

        db.session.commit()

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
                s =  models.State(state=state, clinton_percentage = clinton, sanders_percentage = sanders, url = chart.url)
                s.clinton_delegates = round(clinton * state.pledged_available,0)
                s.sanders_delegates = round(sanders * state.pledged_available,0)
                db.session.add(s)
                db.session.commit()

            else:
                state = models.State.query.filter(models.State.state==state).first()
                state.clinton_percentage = clinton
                state.sanders_percentage = sanders
                state.clinton_delegates = round(clinton * state.pledged_available)
                state.sanders_delegates = round(sanders * state.pledged_available)
                state.url = chart.url
                db.session.commit()

def update(state, clinton_percentage, sanders_percentage):
    yesterday = get_current_date() - timedelta(days=1)
    tomorrow = get_current_date() + timedelta(days=1)

    if not models.Daily.query.filter(and_(models.Daily.date > yesterday, models.Daily.date < tomorrow, models.Daily.state == state)).first():
        date = models.Daily(state=state,date=get_current_date(), clinton_percentage=clinton_percentage, sanders_percentage=sanders_percentage)
        db.session.add(date)
        db.session.commit()
