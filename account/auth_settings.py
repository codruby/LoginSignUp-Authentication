import os
from rest_framework_jwt.settings import api_settings


class AuthSettings:
    # ENCR_KEY = os.environ['ENCR_KEY']
      ENCR_KEY = 'DnniGPGO1svMw2RtVRrvPCDBFf829kzXnC72JVl99k0='

# api_settings.JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
api_settings.JWT_SECRET_KEY = 'j(i&j=0@@9@f4=srb12iixzhp(g=*g8)d!)bbdumdatm2#(22z'
