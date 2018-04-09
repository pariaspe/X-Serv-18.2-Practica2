# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shorterapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urls',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
