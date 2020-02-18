import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER=os.path.join('.','uploads')
    CORS_HEADERS='Content-Type'
    def __init__(self):
        for key,val in os.environ.items():
            if not key.upper().startswith('APP_'):continue
            self.__setattr__(key.upper(),val)