# Generated by Django 2.2.11 on 2020-04-08 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20200408_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policyitem',
            name='document',
        ),
    ]
