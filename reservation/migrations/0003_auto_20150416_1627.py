# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_flight_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='arrival',
            new_name='destination',
        ),
    ]
