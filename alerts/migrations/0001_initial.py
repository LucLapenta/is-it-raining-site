# Generated by Django 2.2.3 on 2019-08-18 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weather_type', models.CharField(choices=[('Rain', 'Rain'), ('Snow', 'Snow'), ('Cold', 'Cold'), ('Heat', 'Heat')], default='Rain', max_length=6)),
                ('interval', models.IntegerField(choices=[(24, 24), (12, 12), (8, 8)], default=24)),
                ('active', models.BooleanField(default=False)),
                ('alert_time', models.TimeField(default='05:00 PM')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
