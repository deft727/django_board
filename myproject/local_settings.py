from .settings import *


import socket
if socket.gethostname()=="http://127.0.0.1:8000/":
    from local_settings import *


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"