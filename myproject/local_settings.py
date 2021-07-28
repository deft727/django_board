from .settings import *


import socket
if socket.gethostname()=="Raouf-PC":
    from local_settings import *


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True