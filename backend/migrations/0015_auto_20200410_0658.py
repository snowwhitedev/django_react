# Generated by Django 2.2.11 on 2020-04-10 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_auto_20200410_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhandbook',
            name='policy',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.PolicyItem'),
        ),
    ]
