# Generated by Django 2.2.3 on 2019-08-03 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.CharField(max_length=5, null=True, unique=True)),
                ('weather_station', models.CharField(max_length=3, null=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('grid_x', models.IntegerField()),
                ('grid_y', models.IntegerField()),
            ],
        ),
    ]
