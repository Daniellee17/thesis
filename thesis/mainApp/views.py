from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import devicestatus
from .models import sensors
from .models import camerasnaps

from datetime import datetime

import sys


def mainPage(response):

    print(" ")
    print("--------------------------- Main Page Refreshed! -------------------------------")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(" ")

    deviceStatusObjects = devicestatus.objects.latest('date')

    # Create instance para makapag insert
    insertDeviceStatus = devicestatus()
    insertCamera = camerasnaps()
    insertSensors = sensors()

    if response.POST.get('action') == 'getSensorValues':
        print(" ")
        print("~Sensor Values Updated~")
        print(" ")

        currentTemperature = 69
        currentHumidity = 11
        currentMoisture = 12

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

        currentSummary = 'pakyu'

        deviceStatusObjectsJSON = {
        'currentTemperatureJSON': currentTemperature,
        'currentHumidityJSON': currentHumidity,
        'currentMoistureJSON': currentMoisture,
        'currentSummaryJSON': currentSummary,
        }


        return JsonResponse(deviceStatusObjectsJSON)

    if response.POST.get('action') == 'snapImage':
        print(" ")
        print("~Image Captured~")
        print(" ")

        insertCamera.cameraURL = '../assets/gardenPics/rpilogo.png'
        insertCamera.save()

        cameraObjectsJSON = {
        'cameraURLJSON': '../assets/gardenPics/rpilogo.png',
        }
        return JsonResponse(cameraObjectsJSON)

    if response.POST.get('action') == 'onFan':
        print(" ")
        print("~Fans Activated~")
        print(" ")
        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = 'on'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offFan':
        print(" ")
        print("~Fans Deactivated~")
        print(" ")
        insertDeviceStatus.fansStatus = 'off'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onLights':
        print(" ")
        print("~Lights Activated~")
        print(" ")
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'on'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offLights':
        print(" ")
        print("~Lights Deactivated~")
        print(" ")
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'off'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onWater':
        print(" ")
        print("~Watering System Activated~")
        print(" ")
        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'on'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offWater':
        print(" ")
        print("~Watering System deactivated~")
        print(" ")
        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'off'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onSeed':
        print(" ")
        print("~Seeder Activated~")
        print(" ")
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'on'
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offSeed':
        print(" ")
        print("~Seeder deactivated~")
        print(" ")
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'off'
        insertDeviceStatus.save()

    # Dito nakalagay sa baba kasi if sa taas,
    # mauuna kunin data before saving the sensor data so late ng isang query
    sensorsObjects = sensors.objects.latest('date')
    cameraObjects = camerasnaps.objects.latest('date')

    myObjects = {'d': 'aa', 'deviceStatusObjects': deviceStatusObjects,
                 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects}

    return render(response, 'main.html', context=myObjects)


def databasePage(response):

    deviceStatusObjects = devicestatus.objects.all()
    sensorsObjects = sensors.objects.all()
    cameraObjects = camerasnaps.objects.all()

    myObjects = {'deviceStatusObjects': deviceStatusObjects,
                 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects}

    return render(response, 'database.html', context=myObjects)
