import os

_curr_dir_path = os.path.dirname(os.path.realpath(__file__))

LOGGING_CONF = _curr_dir_path + '/../logging.conf'
DB_URI = 'sqlite:///'
STATIC_FILES_DIR = _curr_dir_path + '/static'
