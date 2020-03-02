from django.db import models


class sensors(models.Model):
    temperature = models.FloatField(max_length=250, default=0.0);
    humidity = models.IntegerField(default=0);
    moisture = models.IntegerField(default=0);
    temperatureStatus = models.TextField(max_length=250, default="None");
    humidityStatus = models.TextField(max_length=250, default="None");
    soilMoistureStatus = models.TextField(max_length=250, default="None");
    date = models.DateTimeField(auto_now=True);


class devicestatus(models.Model):
    calibrationStatus = models.TextField(max_length=250, default="Off");
    fansStatus = models.TextField(max_length=250, default="Off");
    lightsStatus = models.TextField(max_length=250, default="Off");
    waterStatus = models.TextField(max_length=250, default="Off");
    seedStatus = models.TextField(max_length=250, default="Off");
    date = models.DateTimeField(auto_now=True);

class camerasnaps(models.Model):
    camera = models.ImageField(default='default.png', blank=True);
    cameraURL = models.ImageField(default='../assets/gardenPics/default.png', blank=True);
    plant1 = models.IntegerField(default=0);
    plant2 = models.IntegerField(default=0);
    plant3 = models.IntegerField(default=0);
    plant4 = models.IntegerField(default=0);
    plant5 = models.IntegerField(default=0);
    plant6 = models.IntegerField(default=0);
    plant7 = models.IntegerField(default=0);
    plant8 = models.IntegerField(default=0);
    plant9 = models.IntegerField(default=0);
    plant10 = models.IntegerField(default=0);
    date = models.DateTimeField(auto_now=True);

class counters(models.Model):
    daysCounter = models.IntegerField(default=0);
    date = models.DateTimeField(auto_now=True);

class currentMode(models.Model):
    grid = models.TextField(max_length=250, default="5x2");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=1);
    date = models.DateTimeField(auto_now=True);

class mode1_pechay(models.Model):
    grid = models.TextField(max_length=250, default="5x2");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=1);
    date = models.DateTimeField(auto_now=True);

class mode2_plant2(models.Model):
    grid = models.TextField(max_length=250, default="4x2");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=2);
    date = models.DateTimeField(auto_now=True);

class mode3_plant3(models.Model):
    grid = models.TextField(max_length=250, default="3x2");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=3);
    date = models.DateTimeField(auto_now=True);

class mode4_plant4(models.Model):
    grid = models.TextField(max_length=250, default="2x2");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=4);
    date = models.DateTimeField(auto_now=True);
