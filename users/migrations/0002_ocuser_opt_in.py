# Generated by Django 2.0 on 2017-12-14 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocuser',
            name='opt_in',
            field=models.BooleanField(default=True, verbose_name='Allow emails?'),
        ),
    ]
