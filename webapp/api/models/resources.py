from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


User = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=128, default='')

    class Meta:
        db_table = 'organization'


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization)

    class Meta:
        db_table = 'membership'

    @classmethod
    def get_org_of_user(cls, user):
        try:
            m = cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None
        return m.organization


class Stage(models.Model):
    STATUS_CHOICES = (
        ('creating', 'Creating'),
        ('running', 'Running'),
        ('paused', 'Paused'),
    )

    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, default='')
    endpoint = models.CharField(max_length=256, default='')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='paused')
    repo = models.CharField(max_length=256, default='')
    branch = models.CharField(max_length=256, default='')
    commits = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stages'

    @property
    def created_ts(self):
        return 0
