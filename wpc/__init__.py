from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask.ext.login import LoginManager

import logging
import os
from logentries import LogentriesHandler


def setup_logging(loggers_and_levels, logentries_id=None):
    log = logging.getLogger('logentries')
    log.setLevel(logging.INFO)
    if logentries_id:
        logentries_handler = LogentriesHandler(logentries_id)
        handler = logentries_handler
    else:
        handler = logging.StreamHandler()

    FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    formatter = logging.Formatter(fmt=FORMAT)
    handler.setFormatter(formatter)

    log.addHandler(handler)
    for logger, level in loggers_and_levels:
        logger.setLevel(level)
        logger.addHandler(handler)


def create_app():
    app = Flask(__name__)
    # Set crucial variables
    app.secret_key = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    #Set non crucial variables
    app.config['MAILGUN_API_URL'] = os.environ.get('MAILGUN_API_URL', '')
    app.config['MAILGUN_API_KEY'] = os.environ.get('MAILGUN_API_KEY', '')
    app.config['MAILGUN_TEST_OPTION'] = True if os.environ.get('MAILGUN_TEST_OPTION', 'True') == 'True' else False
    app.config['NOTIFICATION_EMAIL'] = os.environ.get('MAILGUN_SMTP_LOGIN', '')
    app.config['REDDIT_PASSWORD'] = os.environ.get('WPC_REDDIT_PASSWORD', '')
    app.config['REDDIT_USERNAME'] = os.environ.get('WPC_REDDIT_USERNAME', '')
    app.config['YOUTUBE_KEY'] = os.environ.get('WPC_YOUTUBE_KEY', '')
    app.config['GA_TRACKING_CODE'] = os.environ.get('GA_TRACKING_CODE', '')
    app.config['REDDIT_API_ID'] = os.environ.get('WPC_APP_ID', '')
    app.config['REDDIT_API_SECRET'] = os.environ.get('WPC_APP_SECRET', '')
    
    app.config['REDDIT_WEB_APP_USER_AGENT'] = "/r/WatchPeopleCode web app(main contact: /u/godlikesme)"

    Bootstrap(app)
    loggers_and_levels = [(app.logger, logging.INFO),
                          (logging.getLogger('sqlalchemy'), logging.WARNING),
                          (logging.getLogger('apscheduler.scheduler'), logging.INFO)]
    setup_logging(loggers_and_levels, logentries_id=os.environ.get('LOGENTRIES_ID', None))

    app.logger.info("App created!")

    return app

app = create_app()

db = SQLAlchemy(app)
login_manager = LoginManager(app)

import wpc.views  # NOQA
