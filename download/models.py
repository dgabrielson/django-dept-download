from __future__ import print_function, unicode_literals

# -*- coding: utf-8 -*-
###############
###############
import os

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group, User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

my_auth = user_passes_test(lambda u: u.is_authenticated, login_url='/login')

############################################################################


class Software_Manager(models.Manager):
    def __group_test(self, software, test_grp_set):
        soft_grp_set = set(software.groups.all())
        if not soft_grp_set:
            return True
        return bool(soft_grp_set.intersection(test_grp_set))

    def list_for_user(self, user, **kwargs):
        qs = self.filter(Active=True, **kwargs)
        user_grp_set = set(user.groups.all())
        return [s for s in qs if self.__group_test(s, user_grp_set)]

    def get_for_user(self, user, slug):
        available = self.list_for_user(user, slug=slug)
        if len(available) == 1:
            return available[0]


# Products
@python_2_unicode_compatible
class Software(models.Model):

    Active = models.BooleanField(default=True)

    slug = models.SlugField(primary_key=True)
    Name = models.CharField(max_length=32)
    groups = models.ManyToManyField(Group, blank=True)
    download_limit = models.IntegerField(
        blank=True, null=True, help_text='Leave as empty for no limit.')
    # does not apply to users belonging to the 'Statistics Staff' group.

    objects = Software_Manager()

    class Meta:
        verbose_name_plural = 'Software'
        ordering = [
            'Name',
        ]

    def __str__(self):
        return self.slug


# Platforms
@python_2_unicode_compatible
class Platform(models.Model):

    Active = models.BooleanField(default=True)

    slug = models.SlugField(primary_key=True)
    Name = models.CharField(max_length=32)

    class Meta:
        ordering = [
            'Name',
        ]

    def __str__(self):
        return self.slug


# Files
@python_2_unicode_compatible
class Download_File(models.Model):

    Active = models.BooleanField(default=True)

    slug = models.SlugField(primary_key=True)
    Name = models.CharField(max_length=32)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)

    filename = models.FilePathField(
        path=settings.DOWNLOAD_STORAGE_PATH, recursive=False)

    class Meta:
        verbose_name = 'Download File'
        ordering = [
            'software',
            'platform',
            'Name',
        ]

    def __str__(self):
        return self.slug


# History
@python_2_unicode_compatible
class History_Record(models.Model):
    Active = models.BooleanField(default=True)
    when = models.DateField(auto_now=True, editable=False)
    # TODO: should be a date time field.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.when) + u' / ' + "{}".format(
            self.user) + u' / ' + "{}".format(self.software)

    class Meta:
        verbose_name = 'History Record'


#
