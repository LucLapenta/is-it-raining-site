# Generated by Django 2.2.3 on 2019-07-08 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alert_alert_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='interval',
            field=models.CharField(choices=[('Daily', 'Daily'), ('Weekly', 'Weekly')], default='Daily', max_length=4),
        ),
        migrations.AlterField(
            model_name='alert',
            name='weather_type',
            field=models.CharField(choices=[('Rain', 'Rain'), ('Snow', 'Snow'), ('Cold', 'Cold'), ('Heat', 'Heat')], default='Rain', max_length=6),
        ),
    ]
