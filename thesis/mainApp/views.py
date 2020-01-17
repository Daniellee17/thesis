from django.shortcuts import render
from django.http import HttpResponse
from .models import devicestatus
from .models import sensors
from .models import camerasnaps

from datetime import datetime

import sys



def mainPage(response):

    datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    print("------------------------------------------REFRESHED!------------------------------------------")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    deviceStatusObjects = devicestatus.objects.latest('date')

    # Create instance para makapag insert
    insertDeviceStatus = devicestatus()
    insertCamera = camerasnaps()
    insertSensors = sensors()








    currentTemperature = 1
    currentHumidity = 2
    #currentMoisture = sensorsObjects.humidity
    #currentSummary = sensorsObjects.summary
    currentMoisture = 3
    currentSummary = 'default'

    if response.POST.get('action') == 'onFan':



        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = 'on'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offFan':



        insertDeviceStatus.fansStatus = 'off'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onLights':



        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'on'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offLights':



        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'off'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onWater':



        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'on'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offWater':



        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'off'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onSeed':



        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'on'
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offSeed':



        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'off'
        insertDeviceStatus.save()

    if(currentTemperature > 30):

        # Turn on fans automatically

        insertDeviceStatus.fansStatus = 'on'
        insertSensors.temperature = currentTemperature
        insertSensors.humidity = currentHumidity
        insertSensors.moisture = currentMoisture

        if(currentHumidity < 40):
            insertSensors.summary = 'Temperature is too high and Humidity is too low!!!'
            insertSensors.save()
        else:
            insertSensors.summary = 'Temperature is too high!!!'
            insertSensors.save()

    if(currentHumidity < 40):

        insertSensors.temperature = currentTemperature
        insertSensors.humidity = currentHumidity
        insertSensors.moisture = currentMoisture

        if(currentTemperature > 30):
            insertSensors.summary = 'Temperature is too high and Humidity is too low!!!'
            insertSensors.save()
        else:
            insertSensors.summary = 'Humidity is too low!!!'
            insertSensors.save()

    if(currentTemperature < 30):

        # Turn off fans automatically

        insertDeviceStatus.fansStatus = 'off'
        insertSensors.temperature = currentTemperature
        insertSensors.humidity = currentHumidity
        insertSensors.moisture = currentMoisture

        if(currentHumidity > 40):
            insertSensors.summary = 'Temperature and Humidity are okay!!!'
            insertSensors.save()
        else:
            insertSensors.summary = 'Humidity is too low!!!'
            insertSensors.save()

    #Dito nakalagay sa baba kasi if sa taas,
    #mauuna kunin data before saving the sensor data so late ng isang query
    sensorsObjects = sensors.objects.latest('date')
    cameraObjects = camerasnaps.objects.latest('date')

    myObjects = {'deviceStatusObjects': deviceStatusObjects, 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects}

    return render(response, 'main.html', context = myObjects)


def databasePage(response):

    deviceStatusObjects = devicestatus.objects.all()
    sensorsObjects = sensors.objects.all()
    cameraObjects = camerasnaps.objects.all()

    myObjects = {'deviceStatusObjects': deviceStatusObjects, 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects}

    return render(response, 'database.html', context = myObjects)


# Create your views here.
