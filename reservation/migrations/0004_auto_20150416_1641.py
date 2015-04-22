# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_auto_20150416_1627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='destination',
            new_name='arrival',
        ),
    ]
