from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager


# class BaseUserManager(models.Manager):
#     @classmethod
#     def normalize_username(cls, username):
#         """
#         Normalize the username by lowercasing it.
#         """
#         username = username or ""
#         if len(username) < 4:
#             raise ValueError(_('username must have at least 4 characters'))
#         return username.lower()
#
#     def get_by_natural_key(self, username):
#         return self.get(**{self.model.USERNAME_FIELD: username})


from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, username, email=None, full_name=None, phone=None, melicode=None, password=None):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username.lower(),
            full_name=full_name.capitalize() if full_name else None,
            phone=phone,
            melicode=melicode,
            email=self.normalize_email(email) if email else None,
        )

        user.set_password(password)
        user.is_active = True
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, full_name=None, phone=None, melicode=None, password=None):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(username, email, full_name, phone, melicode, password)

        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
