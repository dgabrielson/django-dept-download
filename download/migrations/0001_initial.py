# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Download_File',
            fields=[
                ('Active', models.BooleanField(default=True)),
                ('slug', models.SlugField(serialize=False, primary_key=True)),
                ('Name', models.CharField(max_length=32)),
                ('filename', models.FilePathField(path=b'/www/__download')),
            ],
            options={
                'ordering': ['software', 'platform', 'Name'],
                'verbose_name': 'Download File',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='History_Record',
            fields=[
                ('id',
                 models.AutoField(
                     verbose_name='ID',
                     serialize=False,
                     auto_created=True,
                     primary_key=True)),
                ('Active', models.BooleanField(default=True)),
                ('when', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'History Record',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('Active', models.BooleanField(default=True)),
                ('slug', models.SlugField(serialize=False, primary_key=True)),
                ('Name', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['Name'],
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('Active', models.BooleanField(default=True)),
                ('slug', models.SlugField(serialize=False, primary_key=True)),
                ('Name', models.CharField(max_length=32)),
                ('download_limit',
                 models.IntegerField(
                     help_text=b'Leave as empty for no limit.',
                     null=True,
                     blank=True)),
                ('groups',
                 models.ManyToManyField(
                     to='auth.Group', null=True, blank=True)),
            ],
            options={
                'ordering': ['Name'],
                'verbose_name_plural': 'Software',
            },
            bases=(models.Model, ),
        ),
        migrations.AddField(
            model_name='history_record',
            name='software',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to='download.Software'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='history_record',
            name='user',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download_file',
            name='platform',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to='download.Platform'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download_file',
            name='software',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to='download.Software'),
            preserve_default=True,
        ),
    ]
