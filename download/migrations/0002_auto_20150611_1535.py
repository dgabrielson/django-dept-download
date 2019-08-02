# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', blank=True),
        ),
    ]
