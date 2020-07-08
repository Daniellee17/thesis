# Generated by Django 3.0.7 on 2020-07-08 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='devices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calibrationStatus', models.TextField(default='Off', max_length=250)),
                ('fansStatus', models.TextField(default='Off', max_length=250)),
                ('lightsStatus', models.TextField(default='Off', max_length=250)),
                ('waterStatus', models.TextField(default='Off', max_length=250)),
                ('seedStatus', models.TextField(default='Off', max_length=250)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mode1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grid', models.TextField(default='5x2', max_length=250)),
                ('rows', models.IntegerField(default=5)),
                ('columns', models.IntegerField(default=2)),
                ('modeNumber', models.IntegerField(default=1)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mode1_vision_system',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField(blank=True, default='../assets/gardenPics/default.png')),
                ('plant1', models.IntegerField(default=0)),
                ('plant2', models.IntegerField(default=0)),
                ('plant3', models.IntegerField(default=0)),
                ('plant4', models.IntegerField(default=0)),
                ('plant5', models.IntegerField(default=0)),
                ('plant6', models.IntegerField(default=0)),
                ('plant7', models.IntegerField(default=0)),
                ('plant8', models.IntegerField(default=0)),
                ('plant9', models.IntegerField(default=0)),
                ('plant10', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mode2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grid', models.TextField(default='4x2', max_length=250)),
                ('rows', models.IntegerField(default=5)),
                ('columns', models.IntegerField(default=2)),
                ('modeNumber', models.IntegerField(default=2)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mode2_vision_system',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField(blank=True, default='../assets/gardenPics/default.png')),
                ('plant1', models.IntegerField(default=0)),
                ('plant2', models.IntegerField(default=0)),
                ('plant3', models.IntegerField(default=0)),
                ('plant4', models.IntegerField(default=0)),
                ('plant5', models.IntegerField(default=0)),
                ('plant6', models.IntegerField(default=0)),
                ('plant7', models.IntegerField(default=0)),
                ('plant8', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mode3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grid', models.TextField(default='6x3', max_length=250)),
                ('rows', models.IntegerField(default=5)),
                ('columns', models.IntegerField(default=2)),
                ('modeNumber', models.IntegerField(default=3)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mode3_vision_system',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField(blank=True, default='../assets/gardenPics/default.png')),
                ('plant1', models.IntegerField(default=0)),
                ('plant2', models.IntegerField(default=0)),
                ('plant3', models.IntegerField(default=0)),
                ('plant4', models.IntegerField(default=0)),
                ('plant5', models.IntegerField(default=0)),
                ('plant6', models.IntegerField(default=0)),
                ('plant7', models.IntegerField(default=0)),
                ('plant8', models.IntegerField(default=0)),
                ('plant9', models.IntegerField(default=0)),
                ('plant10', models.IntegerField(default=0)),
                ('plant11', models.IntegerField(default=0)),
                ('plant12', models.IntegerField(default=0)),
                ('plant13', models.IntegerField(default=0)),
                ('plant14', models.IntegerField(default=0)),
                ('plant15', models.IntegerField(default=0)),
                ('plant16', models.IntegerField(default=0)),
                ('plant17', models.IntegerField(default=0)),
                ('plant18', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mode4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grid', models.TextField(default='4x3', max_length=250)),
                ('rows', models.IntegerField(default=5)),
                ('columns', models.IntegerField(default=2)),
                ('modeNumber', models.IntegerField(default=4)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mode4_vision_system',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField(blank=True, default='../assets/gardenPics/default.png')),
                ('plant1', models.IntegerField(default=0)),
                ('plant2', models.IntegerField(default=0)),
                ('plant3', models.IntegerField(default=0)),
                ('plant4', models.IntegerField(default=0)),
                ('plant5', models.IntegerField(default=0)),
                ('plant6', models.IntegerField(default=0)),
                ('plant7', models.IntegerField(default=0)),
                ('plant8', models.IntegerField(default=0)),
                ('plant9', models.IntegerField(default=0)),
                ('plant10', models.IntegerField(default=0)),
                ('plant11', models.IntegerField(default=0)),
                ('plant12', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mode_selected',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daysCounter', models.IntegerField(default=0)),
                ('grid', models.TextField(default='5x2', max_length=250)),
                ('rows', models.IntegerField(default=5)),
                ('columns', models.IntegerField(default=2)),
                ('modeNumber', models.IntegerField(default=1)),
                ('image', models.TextField(blank=True, default='../assets/gardenPics/default.png')),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='sensors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField(default=0.0, max_length=250)),
                ('humidity', models.IntegerField(default=0)),
                ('moisture', models.IntegerField(default=0)),
                ('temperatureStatus', models.TextField(default='None', max_length=250)),
                ('humidityStatus', models.TextField(default='None', max_length=250)),
                ('soilMoistureStatus', models.TextField(default='None', max_length=250)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
