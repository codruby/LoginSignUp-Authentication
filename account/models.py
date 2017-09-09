from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AppUserManager(BaseUserManager):
    """
    Application User Manager
    """

    def create_superuser(self, email, first_name, password):
        """
        Application User model
        """
        if not email:
            raise ValueError('User must have a valid username')

        user = self.model(
            email=email,
            first_name=first_name,
            is_admin=True)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(email, password, **extra_fields)


class AppUser(AbstractBaseUser):
    """
    Application User model
    """
    first_name = models.CharField(verbose_name="first_name", default=None, max_length=50, null=True)
    middle_name = models.CharField(verbose_name="middle_name", default=None, max_length=50, null=True, blank=True)
    last_name = models.CharField(verbose_name="last_name", default=None, max_length=50, null=True, blank=True)
    email = models.EmailField(verbose_name="email", unique=True)
    mobile = models.BigIntegerField(verbose_name="mobile", null=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(verbose_name="otp", null=True)

    objects = AppUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def get_short_name(self):
        '''
        Method for getting Name
        '''
        return self.first_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    class Meta:
        '''model meta data'''
        verbose_name = "Application User"
        verbose_name_plural = "Application Users"
        db_table = "appuser"

    def __unicode__(self):
        '''model __unicode__ data'''
        return self.first_name
