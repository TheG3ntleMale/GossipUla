class Config:
    SECRET_KEY = 'B*1agBSo2L.%kvuA*S.'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'ula'
    MYSQL_CHARSET = 'utf8mb4'

config = {
    'development': DevelopmentConfig
}