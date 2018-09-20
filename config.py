import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
<<<<<<< HEAD
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
=======
>>>>>>> 20506119a5a18ca00fb65c9b1a0542ebfbfd52f9
