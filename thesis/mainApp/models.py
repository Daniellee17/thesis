from django.db import models

# Create your models here.
#ONE CLASS ONE TABLE

class sensors(models.Model):
    temperature = models.IntegerField(default=1);
    moisture = models.IntegerField(default=2);
    humidity = models.IntegerField(default=3);
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
    date = models.DateTimeField(auto_now=True);
