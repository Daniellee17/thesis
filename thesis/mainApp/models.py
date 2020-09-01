from django.db import models

class mode_selected(models.Model):
    daysCounter = models.IntegerField(default=0);
    grid = models.TextField(max_length=250, default="5x2");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=1);
    image = models.TextField(default='../assets/gardenPics/default.png', blank=True);
    date = models.DateTimeField(auto_now=True);

class devices(models.Model):
    calibrationStatus = models.TextField(max_length=250, default="Off");
    fansStatus = models.TextField(max_length=250, default="Off");
    rgbLedStatus = models.TextField(max_length=250, default="Off");
    whiteLedStatus = models.TextField(max_length=250, default="Off");
    waterStatus = models.TextField(max_length=250, default="Off");
    seedStatus = models.TextField(max_length=250, default="Off");
    date = models.DateTimeField(auto_now=True);

class sensors(models.Model):
    temperature = models.FloatField(max_length=250, default=0.0);
    humidity = models.IntegerField(default=0);
    moisture = models.IntegerField(default=0);
    temperatureStatus = models.TextField(max_length=250, default="None");
    humidityStatus = models.TextField(max_length=250, default="None");
    soilMoistureStatus = models.TextField(max_length=250, default="None");
    date = models.DateTimeField(auto_now=True);

class threshold(models.Model):
    temperature_low = models.FloatField(max_length=250, default=0.0);
    temperature_high = models.FloatField(max_length=250, default=0.0);
    humidity_low = models.IntegerField(default=0);
    humidity_high = models.IntegerField(default=0);
    moisture_dry = models.IntegerField(default=0);
    moisture_wet = models.IntegerField(default=0);
    date = models.DateTimeField(auto_now=True);

class mode1(models.Model):
    grid = models.TextField(max_length=250, default="5x2");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=1);
    date = models.DateTimeField(auto_now=True);

class mode2(models.Model):
    grid = models.TextField(max_length=250, default="4x2");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=2);
    date = models.DateTimeField(auto_now=True);

class mode3(models.Model):
    grid = models.TextField(max_length=250, default="6x3");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=3);
    date = models.DateTimeField(auto_now=True);

class mode4(models.Model):
    grid = models.TextField(max_length=250, default="4x3");
    rows = models.IntegerField(default=5);
    columns = models.IntegerField(default=2);
    modeNumber = models.IntegerField(default=4);
    date = models.DateTimeField(auto_now=True);

class mode1_vision_system(models.Model):
    image = models.TextField(default='../assets/gardenPics/default.png', blank=True);
    plant1 = models.IntegerField(default=0);
    status1 = models.TextField(max_length=250, default="Early");
    plant2 = models.IntegerField(default=0);
    status2 = models.TextField(max_length=250, default="Early");
    plant3 = models.IntegerField(default=0);
    status3 = models.TextField(max_length=250, default="Early");
    plant4 = models.IntegerField(default=0);
    status4 = models.TextField(max_length=250, default="Early");
    plant5 = models.IntegerField(default=0);
    status5 = models.TextField(max_length=250, default="Early");
    plant6 = models.IntegerField(default=0);
    status6 = models.TextField(max_length=250, default="Early");
    plant7 = models.IntegerField(default=0);
    status7 = models.TextField(max_length=250, default="Early");
    plant8 = models.IntegerField(default=0);
    status8 = models.TextField(max_length=250, default="Early");
    plant9 = models.IntegerField(default=0);
    status9 = models.TextField(max_length=250, default="Early");
    plant10 = models.IntegerField(default=0);
    status10 = models.TextField(max_length=250, default="Early");
    image1 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image2 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image3 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image4 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image5 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image6 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image7 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image8 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image9 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image10 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    date = models.DateTimeField(auto_now=True);

class mode2_vision_system(models.Model):
    image = models.TextField(default='../assets/gardenPics/default.png', blank=True);
    plant1 = models.IntegerField(default=0);
    status1 = models.TextField(max_length=250, default="Early");
    plant2 = models.IntegerField(default=0);
    status2 = models.TextField(max_length=250, default="Early");
    plant3 = models.IntegerField(default=0);
    status3 = models.TextField(max_length=250, default="Early");
    plant4 = models.IntegerField(default=0);
    status4 = models.TextField(max_length=250, default="Early");
    plant5 = models.IntegerField(default=0);
    status5 = models.TextField(max_length=250, default="Early");
    plant6 = models.IntegerField(default=0);
    status6 = models.TextField(max_length=250, default="Early");
    plant7 = models.IntegerField(default=0);
    status7 = models.TextField(max_length=250, default="Early");
    plant8 = models.IntegerField(default=0);
    status8 = models.TextField(max_length=250, default="Early");
    image1 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image2 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image3 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image4 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image5 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image6 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image7 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image8 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    date = models.DateTimeField(auto_now=True);

class mode3_vision_system(models.Model):
    image = models.TextField(default='../assets/gardenPics/default.png', blank=True);
    plant1 = models.IntegerField(default=0);
    status1 = models.TextField(max_length=250, default="Early");
    plant2 = models.IntegerField(default=0);
    status2 = models.TextField(max_length=250, default="Early");
    plant3 = models.IntegerField(default=0);
    status3 = models.TextField(max_length=250, default="Early");
    plant4 = models.IntegerField(default=0);
    status4 = models.TextField(max_length=250, default="Early");
    plant5 = models.IntegerField(default=0);
    status5 = models.TextField(max_length=250, default="Early");
    plant6 = models.IntegerField(default=0);
    status6 = models.TextField(max_length=250, default="Early");
    plant7 = models.IntegerField(default=0);
    status7 = models.TextField(max_length=250, default="Early");
    plant8 = models.IntegerField(default=0);
    status8 = models.TextField(max_length=250, default="Early");
    plant9 = models.IntegerField(default=0);
    status9 = models.TextField(max_length=250, default="Early");
    plant10 = models.IntegerField(default=0);
    status10 = models.TextField(max_length=250, default="Early");
    plant11 = models.IntegerField(default=0);
    status11 = models.TextField(max_length=250, default="Early");
    plant12 = models.IntegerField(default=0);
    status12 = models.TextField(max_length=250, default="Early");
    plant13 = models.IntegerField(default=0);
    status13 = models.TextField(max_length=250, default="Early");
    plant14 = models.IntegerField(default=0);
    status14 = models.TextField(max_length=250, default="Early");
    plant15 = models.IntegerField(default=0);
    status15 = models.TextField(max_length=250, default="Early");
    plant16 = models.IntegerField(default=0);
    status16 = models.TextField(max_length=250, default="Early");
    plant17 = models.IntegerField(default=0);
    status17 = models.TextField(max_length=250, default="Early");
    plant18 = models.IntegerField(default=0);
    status18 = models.TextField(max_length=250, default="Early");
    image1 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image2 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image3 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image4 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image5 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image6 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image7 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image8 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image9 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image10 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image11 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image12 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image13 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image14 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image15 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image16 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image17 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image18 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    date = models.DateTimeField(auto_now=True);

class mode4_vision_system(models.Model):
    image = models.TextField(default='../assets/gardenPics/default.png', blank=True);
    plant1 = models.IntegerField(default=0);
    status1 = models.TextField(max_length=250, default="Early");
    plant2 = models.IntegerField(default=0);
    status2 = models.TextField(max_length=250, default="Early");
    plant3 = models.IntegerField(default=0);
    status3 = models.TextField(max_length=250, default="Early");
    plant4 = models.IntegerField(default=0);
    status4 = models.TextField(max_length=250, default="Early");
    plant5 = models.IntegerField(default=0);
    status5 = models.TextField(max_length=250, default="Early");
    plant6 = models.IntegerField(default=0);
    status6 = models.TextField(max_length=250, default="Early");
    plant7 = models.IntegerField(default=0);
    status7 = models.TextField(max_length=250, default="Early");
    plant8 = models.IntegerField(default=0);
    status8 = models.TextField(max_length=250, default="Early");
    plant9 = models.IntegerField(default=0);
    status9 = models.TextField(max_length=250, default="Early");
    plant10 = models.IntegerField(default=0);
    status10 = models.TextField(max_length=250, default="Early");
    plant11 = models.IntegerField(default=0);
    status11 = models.TextField(max_length=250, default="Early");
    plant12 = models.IntegerField(default=0);
    status12 = models.TextField(max_length=250, default="Early");
    image1 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image2 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image3 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image4 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image5 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image6 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image7 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image8 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image9 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image10 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image11 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    image12 = models.TextField(default='../assets/icons/seedIcon.png', blank=True);
    date = models.DateTimeField(auto_now=True);
