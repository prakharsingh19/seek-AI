class Config:
    DEBUG = True
    SQL_ALCHEMY_TRACK_MODIFICATION = False


class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/seek_ai.sqlite3"
    DEBUG = True
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "thisshouldbekeptsecret"
    SECRET_KEY = "PKMKB"
    WTF_CSRF_ENABLED = False
