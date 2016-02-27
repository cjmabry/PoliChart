# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from fbone import create_app, polling
from fbone.extensions import db
from fbone.utils import MALE

app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run()


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()
    db.session.commit()
    polling.populate_states()

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
