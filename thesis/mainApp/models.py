from django.db import models

# Create your models here.
#ONE CLASS ONE TABLE

class sensors(models.Model):
    temperature = models.FloatField(max_length=250, default=0.0);
    humidity = models.FloatField(max_length=250, default=0.0);
    moisture = models.IntegerField(default=3);
    summary = models.TextField(max_length=250, default="None");
    date = models.DateTimeField(auto_now=True);


class devicestatus(models.Model):
    fansStatus = models.TextField(max_length=250, default="off");
    lightsStatus = models.TextField(max_length=250, default="off");
    waterStatus = models.TextField(max_length=250, default="off");
    seedStatus = models.TextField(max_length=250, default="off");
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
