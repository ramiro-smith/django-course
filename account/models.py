# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """Manager for user create and update"""
    def create_user(self, username, email, password=None,
                    is_admin=False, is_staff=False, is_active=True):
        # check that all data is here
        if not username:
            raise ValueError("username is required")

        if not email:
            raise ValueError("email is required")

        if not password:
            raise ValueError("you must have password")

        # put the info to user
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )

        # to set the password to user
        user.set_password(password)
        # to make sure that user is not superuser
        # we want normal user
        user.admin = is_admin
        user.active = is_active
        user.staff = is_staff
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password=None):
        # for create user just change the kwargs is_admin, is_active, is_staff
        user = self.create_user(username=username, email=email, password=password,
                                is_active=True, is_admin=True, is_staff=True)
        return user





class User(AbstractBaseUser):
    username = models.CharField(max_length=155, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        if self.first_name and self.last_name:
            return "{first} {last}".format(first=self.first_name,
                                           last=self.last_name)
        return self.username

    def get_short_name(self):
        return self.username

    def get_email_address(self):
        return self.email

    @property
    def is_staff(self):
        """ IS User member of staff """
        return self.staff

    @property
    def is_admin(self):
        """Is User member of admin"""
        # all member of admin are member of is_staff
        return self.admin

    @property
    def is_active(self):
        """check  if user is active or not"""
        return self.active
