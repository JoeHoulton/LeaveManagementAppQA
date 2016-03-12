from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_leavemanagementapp',
        'HOST': 'josephhoulton.mysql.pythonanywhere-services.com',
        'USER': 'JosephHoulton',
        'PASSWORD': 'testdatabasepassword',
    },
}