from __future__ import unicode_literals

from django.apps import AppConfig


class AwxConfig(AppConfig):
    name = 'awx'

    def ready(self):

        super().ready()

