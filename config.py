import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'oqkj412409sdovisdj124124asdlkjlfkjAASLAKJLSKJ'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAGENTO_REST_URL = os.environ.get('MAGENTO_REST_URL') or 'http://prenota.parrocchiaportile.it/rest'
    MAGENTO_STORE = os.environ.get('MAGENTO_STORE') or 'default'
    MAGENTO_TOKEN = os.environ.get('MAGENTO_TOKEN') or '2krqq7u6cnle34rchzy1jddo3x2rfjf9'



