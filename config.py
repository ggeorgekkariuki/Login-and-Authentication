class Config:
    SECRET_KEY = '9OLWxND4o83j4K4iuopO'


class Development(Config):
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://postgres:egroeg@127.0.0.1:5432/users_log'
    # Do not track all the modifications made to the file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


"""The server URI will change and the database name might change"""


class Production(Config):
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://postgres:egroeg@127.0.0.1:5432/june_payroll_system'
    # Do not track all the modifications made to the file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
