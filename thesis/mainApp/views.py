from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import devicestatus
from .models import sensors
from .models import camerasnaps
from pygame.locals import *
from datetime import datetime
from numpy import interp  # To scale values
from time import sleep  # To add delay

# Importing modules
import spidev # To communicate with SPI devices
import sys
import pygame
import pygame.camera
import Adafruit_DHT
import RPi.GPIO as GPIO

sensor = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)  # Fan1
GPIO.setup(26, GPIO.OUT)  # Fan2
GPIO.setup(20, GPIO.OUT)  # Lights
GPIO.setup(16, GPIO.OUT)  # Seeder
GPIO.setup(12, GPIO.OUT)  # Water


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

        # Start SPI connection
        spi = spidev.SpiDev() # Created an object
        spi.open(0,0)

        humidity, temperature = Adafruit_DHT.read_retry(sensor, 1)
        
        print(" ")
        print("~Sensor dd Updated~")
        print(" ")
   

        def analogInput(channel):
          spi.max_speed_hz = 1350000
          adc = spi.xfer2([1,(8+channel)<<4,0])
          data = ((adc[1]&3) << 8) + adc[2]
          return data

        output = analogInput(0) # Reading from CH0
        output = interp(output, [0, 1023], [100, 0])
        output = int(output)
        #print("Moistures", output)

        currentTemperature = temperature
        currentHumidity = humidity
        currentMoisture = output
        currentSummary = 'Temperature and Humidity are okay!!!'
        
        insertSensors.temperature = currentTemperature
        insertSensors.humidity = currentHumidity
        insertSensors.moisture = currentMoisture
        insertSensors.summary = currentSummary

        insertSensors.save()
    
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

        # CameraPart
        pygame.init()
        pygame.camera.init()
        #screen = pygame.display.set_mode([640, 480])
        #cam = pygame.camera.Camera("/dev/video0", (640, 480))
        cam = pygame.camera.Camera("/dev/video0", (352, 288))
        cam.start()
        image = cam.get_image()
        pygame.image.save(image, '/home/pi/Desktop/thesis/thesis/assets/gardenPics/' +
                          datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + '.jpg')
        cam.stop()

        insertCamera.camera = datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + '.jpg'
        insertCamera.cameraURL = '../assets/gardenPics/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + '.jpg'
        insertCamera.save()

        cameraObjectsJSON = {
        'cameraURLJSON': '../assets/gardenPics/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + '.jpg',
        'cameraDateJSON': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p'))
        }

        return JsonResponse(cameraObjectsJSON)

    if response.POST.get('action') == 'onFan':
        
        print(" ")
        print("~Fans Activated~")
        print(" ")

        GPIO.output(21, GPIO.HIGH)
        GPIO.output(26, GPIO.HIGH)

        insertDeviceStatus.fansStatus = 'on'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offFan':
        
        print(" ")
        print("~Fans deactivated~")
        print(" ")

        GPIO.output(21, GPIO.LOW)
        GPIO.output(26, GPIO.LOW)

        insertDeviceStatus.fansStatus = 'off'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onLights':
        
        print(" ")
        print("~Lights Activated~")
        print(" ")

        GPIO.output(20, GPIO.HIGH)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'on'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offLights':
        
        print(" ")
        print("~Lights Deactivated~")
        print(" ")

        GPIO.output(20, GPIO.LOW)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'off'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onWater':
    
        print(" ")
        print("~Water System Activated~")
        print(" ")

        GPIO.output(16, GPIO.HIGH)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'on'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offWater':
        
        print(" ")
        print("~Water System Deactivated~")
        print(" ")
        
        GPIO.output(16, GPIO.LOW)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'off'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onSeed':
        
        print(" ")
        print("~Seeder Activated~")
        print(" ")

        GPIO.output(12, GPIO.HIGH)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'on'
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offSeed':
        
        print(" ")
        print("~Seeder Deactivated~")
        print(" ")

        GPIO.output(12, GPIO.LOW)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'off'
        insertDeviceStatus.save()

    # Dito nakalagay sa baba kasi if sa taas,
    # mauuna kunin data before saving the sensor data so late ng isang query
    sensorsObjects = sensors.objects.latest('date')
    cameraObjects = camerasnaps.objects.latest('date')

    myObjects = {'deviceStatusObjects': deviceStatusObjects,
                 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects}

    return render(response, 'main.html', context=myObjects)


def databasePage(response):

    deviceStatusObjects = devicestatus.objects.all()
    sensorsObjects = sensors.objects.all()
    cameraObjects = camerasnaps.objects.all()

    myObjects = {'deviceStatusObjects': deviceStatusObjects,
                 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects}

    return render(response, 'database.html', context=myObjects)
