# Include all global variables in this file.
# These are used across different modules/packages
# where required.

# Service Name
SVC_NAME = 'batman-ms-crons'

# DB Settings
DB_HOST_WRITER = ''
DB_HOST_READER = ''
DB_PORT = ''
DB_NAME = 'batman_crons'
DB_USER = ''
DB_PASS = ''

# Crons Settings
CRONS_MAX_EXEC_TIME = 15 #minutes
CRONS_MAX_LOG_RETENTION = 2880 #minutes

# Flask Settings
FLASK_PORT = 80
FLASK_DEBUG = False