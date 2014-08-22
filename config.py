import os
basedir = os.path.abspath(os.path.dirname(__file__))

__version__ = '0.1 alpha'

SQLALCHEMY_DATABASE_NAME = 'sample_db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, \
                            'db/{}.db'.format(SQLALCHEMY_DATABASE_NAME))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_ECHO = False

# Seconds to wait before polling new data to refresh the stocks database.
UPDATE_INTERVAL = 5

default_parameters = {
    'DEBUG': False
    }

quote_properties = {
    'a0': 'Ask',
    'a2': 'AverageDailyVolume',
    'a5': 'AskSize',
    'b0': 'Bid',
    'b2': 'AskRealtime',
    'b3': 'BidRealtime',
    'b4': 'BookValuePerShare',
    'b6': 'BidSize',
    'c0': 'Change_ChangeInPercent',
    'c1': 'Change',
    'c3': 'Commission',
    'c4': 'Currency',
    'c6': 'ChangeRealtime',
    'c8': 'AfterHoursChangeRealtime',
    'd0': 'TrailingAnnualDividendYield',
    }