# Generated by Django 4.1.3 on 2022-12-03 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App9SPL', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='systemuser',
            name='is_verify',
        ),
    ]
