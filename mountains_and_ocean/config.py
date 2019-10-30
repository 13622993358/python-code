class Config():
    SECRET_KEY = "Supersjz*3358."
    JSON_AS_ASCII = False
    #数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mysql@127.0.0.1:3306/mao"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopConfig(Config):
    DEBUG = True

class ProductConfig(Config):
    pass

config_map={
    "develop":DevelopConfig,
    "product":ProductConfig
}