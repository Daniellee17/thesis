from django.shortcuts import render
from django.http import HttpResponse
from .models import devicestatus;



def mainPage(response):
    deviceStatusObjects = devicestatus.objects.latest('date')
    insertDeviceStatus = devicestatus()

    if (response.GET.get('onFans_btn')):

        insertDeviceStatus.fansStatus = 'on'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if (response.GET.get('offFans_btn')):

        insertDeviceStatus.fansStatus = 'off'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if (response.GET.get('onLights_btn')):

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'on'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if (response.GET.get('offLights_btn')):

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'off'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()


    return render(response, 'main.html', {'deviceStatusObjects': deviceStatusObjects})

def databasePage(response):

    deviceStatusObjects = devicestatus.objects.all()

    return render(response, 'database.html', {'deviceStatusObjects': deviceStatusObjects})




# Create your views here.
