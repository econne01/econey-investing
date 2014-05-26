
class Settings(object):
    PROJECT_DIR = '/home/eric/projects/personal/econey-investing/'

    DB_NAME = 'stocks.db'
    DATABASE = PROJECT_DIR + DB_NAME
    DEBUG = True
    SECRET_KEY = 'RVvgMpeGmq68ZKfv8nXE'
    USERNAME = 'admin'
    PASSWORD = 'default'

    STATIC_DIRECTORY = PROJECT_DIR + 'src/static'
    UPLOAD_DIRECTORY = PROJECT_DIR + 'uploads'
    TEMPLATE_DIRECTORY = PROJECT_DIR + 'src/templates'
    SYNCDB_SQL = PROJECT_DIR + 'src/app/schema.sql'

    ALLOWED_UPLOAD_EXTENSIONS = set(['csv'])
