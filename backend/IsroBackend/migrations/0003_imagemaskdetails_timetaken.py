# Generated by Django 3.0.4 on 2020-07-18 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IsroBackend', '0002_auto_20200717_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemaskdetails',
            name='timeTaken',
            field=models.FloatField(null=True),
        ),
    ]
