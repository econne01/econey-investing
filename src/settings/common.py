
class Settings(object):
    DATABASE = '/home/eric/projects/personal/econey-investing/stocks.db'
    DEBUG = True
    SECRET_KEY = 'RVvgMpeGmq68ZKfv8nXE'
    USERNAME = 'admin'
    PASSWORD = 'default'

    STATIC_DIRECTORY = '/home/eric/projects/personal/econey-investing/src/static'
    UPLOAD_DIRECTORY = '/home/eric/projects/personal/econey-investing/uploads'
    TEMPLATE_DIRECTORY = '/home/eric/projects/personal/econey-investing/src/templates'
    SYNCDB_SQL = 'app/schema.sql'

    ALLOWED_UPLOAD_EXTENSIONS = set(['csv'])
