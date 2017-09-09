'''Defines which authentication backend for registration app.'''
from django.contrib.auth.backends import ModelBackend
from .models import AppUser


class AppUserModelBackend(ModelBackend):

    '''Authenticate AppUser'''

    def authenticate(self, username=None, password=None):
        '''
        Method for authentication
        '''
        try:
            user = AppUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except AppUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        '''
        Method for getting user data by passing user_id
        '''
        try:
            return AppUser.objects.get(pk=user_id)
        except AppUser.DoesNotExist:
            return None
