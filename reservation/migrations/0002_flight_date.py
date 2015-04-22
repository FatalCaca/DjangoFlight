# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='date',
            field=models.DateTimeField(verbose_name='date decollage', default=datetime.datetime(2015, 4, 16, 12, 38, 59, 98660, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
