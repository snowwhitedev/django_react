# Generated by Django 2.2.11 on 2020-04-10 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20200410_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentstructure',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
