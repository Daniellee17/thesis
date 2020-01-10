from django.shortcuts import render
from django.http import HttpResponse
from .models import devicestatus
from .models import sensors
from pygame.locals import *

import sys
import pygame
import pygame.camera
import Adafruit_DHT
import RPi.GPIO as GPIO

sensor = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT, initial=0)  # Fans
GPIO.setup(20, GPIO.OUT, initial=0)  # Lights
GPIO.setup(16, GPIO.OUT, initial=0)  # Seeder
GPIO.setup(12, GPIO.OUT, initial=0)  # Water


def mainPage(response):

    print("------------------------------------------REFRESHED!------------------------------------------")

    deviceStatusObjects = devicestatus.objects.latest('date')
    sensorsObjects = sensors.objects.latest('date')

    # Create instance para makapag insert
    insertDeviceStatus = devicestatus()
    insertSensors = sensors()

    humidity, temperature = Adafruit_DHT.read_retry(sensor, 1)

    currentTemperature = temperature
    currentHumidity = humidity
    #currentMoisture = sensorsObjects.humidity
    #currentSummary = sensorsObjects.summary
    currentMoisture = '100'
    currentSummary = 'default'

    if response.POST.get('action') == 'onFan':

        GPIO.output(21, GPIO.HIGH)

        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = 'on'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offFan':

        GPIO.output(21, GPIO.LOW)

        insertDeviceStatus.fansStatus = 'off'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onLights':

        GPIO.output(20, GPIO.HIGH)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'on'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offLights':

        GPIO.output(20, GPIO.LOW)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'off'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onWater':

        GPIO.output(16, GPIO.HIGH)

        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'on'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offWater':

        GPIO.output(16, GPIO.LOW)

        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'off'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onSeed':

        GPIO.output(12, GPIO.HIGH)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'on'
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offSeed':

        GPIO.output(12, GPIO.LOW)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'off'
        insertDeviceStatus.save()

    if(currentTemp > 30):

        # Turn on fans automatically
        GPIO.output(21, GPIO.HIGH)
        insertDeviceStatus.fansStatus = 'on'
        insertSensors.temperature = currentTemperature
        insertSensors.humidity = currentHumidity
        insertSensors.moisture = currentMoisture

        if(currentHumidity < 40):
            insertSensors.summary = 'Temperature is too high and Humidity is too low!!!'
            save()
        else:
            insertSensors.summary = 'Temperature is too high!!!'
            save()

    if(currentHumidity < 40):

        insertSensors.temperature = currentTemperature
        insertSensors.humidity = currentHumidity
        insertSensors.moisture = currentMoisture

        if(currentTemp>30):
            insertSensors.summary = 'Temperature is too high and Humidity is too low!!!'
            save()
        else:
            insertSensors.summary = 'Humidity is too low!!!'
            save()

    if(currentTemp < 30):

        # Turn off fans automatically
        GPIO.output(21, GPIO.LOW)
        insertDeviceStatus.fansStatus = 'off'
        insertSensors.temperature = currentTemperature
        insertSensors.humidity = currentHumidity
        insertSensors.moisture = currentMoisture

        if(currentHumidity > 40):
            insertSensors.summary = 'Temperature and Humidity are okay!!!'
            save()
        else:
            insertSensors.summary = 'Humidity is too low!!!'
            save()





    return render(response, 'main.html', {'deviceStatusObjects': deviceStatusObjects})


def databasePage(response):

    deviceStatusObjects = devicestatus.objects.all()

    return render(response, 'database.html', {'deviceStatusObjects': deviceStatusObjects})


# Create your views here.
