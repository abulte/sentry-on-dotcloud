#!/usr/bin/env python

import json
import os

from django.contrib.auth.models import User

with open(os.path.expanduser('~/environment.json'), 'r') as env_file:
    dotcloud_env = json.load(env_file)

u, created = User.objects.get_or_create(username=dotcloud_env.get('SENTRY_WEB_ADMIN', 'admin'))
if created:
    u.set_password(dotcloud_env.get('SENTRY_WEB_ADMIN_PASSWORD', 'password'))
    u.is_superuser = True
    u.is_staff = True
    u.save()
