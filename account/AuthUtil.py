from auth_settings import *
from cryptography.fernet import Fernet
from rest_framework_jwt.utils import *


class AuthUtil:

    _fernetObj = None

    @staticmethod
    def encrypt (payload):
        if AuthUtil._fernetObj is None:
            AuthUtil._fernetObj = Fernet(AuthSettings.ENCR_KEY)

        # return AuthUtil._fernetObj.encrypt(bytes(payload, 'utf-8')).decode('utf-8')
        return AuthUtil._fernetObj.encrypt(bytes(payload)).decode('utf-8')

    @staticmethod
    def decrypt (payload):
         if AuthUtil._fernetObj is None:
            AuthUtil._fernetObj = Fernet(AuthSettings.ENCR_KEY)

         return AuthUtil._fernetObj.decrypt(bytes(payload)).decode('utf-8')

    @staticmethod
    def getTokenContent (tokenPayload):
        try:
            decryptedToken = AuthUtil.decrypt(tokenPayload)
            decodedClaims = jwt_decode_handler(decryptedToken)
            return decodedClaims
        except BaseException as e:
            return None