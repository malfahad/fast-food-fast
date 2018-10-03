from config_heroku import *

try:
    from config_local import *
except ImportError:
    pass
