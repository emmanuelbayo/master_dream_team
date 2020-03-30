class Config(object):

    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG =True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):

    #Les configurations de production

    DEBUG = False

class TestingConfig(Config):

    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
    }