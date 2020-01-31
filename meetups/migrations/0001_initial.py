# Generated by Django 3.0.2 on 2020-01-31 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0002_auto_20200131_2247'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=100)),
                ('details', models.TextField(max_length=500)),
                ('organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('personal_interests', models.ManyToManyField(blank=True, to='profiles.PersonalInterest')),
                ('prof_interests', models.ManyToManyField(blank=True, to='profiles.ProfessionalInterest')),
            ],
            options={
                'ordering': ['date', 'time'],
            },
        ),
    ]
