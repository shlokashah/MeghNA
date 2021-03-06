# Generated by Django 3.0.4 on 2020-08-01 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IsroBackend', '0006_auto_20200801_2301'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagePredictedMPA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predictionOf', models.FloatField(null=True)),
                ('pred_com_x', models.FloatField(null=True)),
                ('pred_com_y', models.FloatField(null=True)),
                ('error', models.FloatField(null=True)),
                ('name', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='IsroBackend.ImageFileName')),
            ],
        ),
    ]
