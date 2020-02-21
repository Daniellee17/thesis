from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import devicestatus
from .models import sensors
from .models import camerasnaps
from pygame.locals import *
from datetime import datetime
from datetime import date 
from numpy import interp  # To scale values
from time import sleep  # To add delay
from plantcv import plantcv as pcv

import os
import sys
import RPi.GPIO as GPIO
#Soil Moisture Sensor
import spidev # To communicate with SPI devices
#Camera
import pygame
import pygame.camera
#DHT22
import Adafruit_DHT
#sensor = Adafruit_DHT.DHT11
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_SENSOR2 = Adafruit_DHT.DHT22
#Image Processing
import numpy as np
import cv2
import re

GPIO.setmode(GPIO.BCM) #Read GPIO# and not pin #!
GPIO.setup(21, GPIO.OUT)  # Lights, PIN 40 (Right)
GPIO.setup(20, GPIO.OUT)  # Fan1, PIN 38 (Right)
GPIO.setup(26, GPIO.OUT)  # Fan2, PIN 37 (Left)
GPIO.setup(16, GPIO.OUT)  # Water, PIN 36 (Right)
GPIO.setup(19, GPIO.OUT)  # WaterXYZ, PIN 35 (Left)
GPIO.setup(12, GPIO.OUT)  # Seeder, PIN 32 (Right)
GPIO.setup(6, GPIO.OUT)  # SeederXYZ, PIN 31 (Left)
DHT_PIN = 1 # PIN 28 (Right)
DHT_PIN2 = 7 # PIN 26 (Right)


def mainPage(response):

    print(" ")
    print("--------------------------- Main Page Refreshed! -------------------------------")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(" ")

    deviceStatusObjects = devicestatus.objects.latest('date')

    # Create instance so you can insert into DB
    insertDeviceStatus = devicestatus()
    insertCamera = camerasnaps()
    insertSensors = sensors()
    insertCounters = counters()


    if response.POST.get('action') == 'getSensorValues':
        print(" ")
        print("~Sensor Values Updated~")
        print(" ")

        # Start SPI connection
        spi = spidev.SpiDev() # Created an object
        spi.open(0,0)

        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        humidity2, temperature2 = Adafruit_DHT.read_retry(DHT_SENSOR2, DHT_PIN2)


        def analogInput(channel):
          spi.max_speed_hz = 1350000
          adc = spi.xfer2([1,(8+channel)<<4,0])
          data = ((adc[1]&3) << 8) + adc[2]
          return data

        output = analogInput(0) # Reading from CH0
        output = interp(output, [0, 1023], [100, 0])
        output = int(output)
        #print("Moistures", output)

        currentTemperature = round(temperature, 2)
        currentHumidity = round(humidity, 2)
        currentTemperature2 = round(temperature2, 2)
        currentHumidity2 = round(humidity2, 2)
        currentMoisture = output
        currentSummary = 'Temperature and Humidity are okay!!!'

        averageTemperature = (currentTemperature + currentTemperature2) / 2
        averageHumidity = (currentHumidity + currentHumidity2) / 2

        print("Current Temp1:")
        print(currentTemperature)
        print("Current Hum1:")
        print(currentHumidity)
        print("Current Temp2:")
        print(currentTemperature2)
        print("Current Hum2:")
        print(currentHumidity2)
        print("Current Moisture:")
        print(currentMoisture)
        print("Ave temp")
        print(round(averageTemperature, 2))
        print("Ave humidity")
        print(round(averageHumidity, 2))

        insertSensors.temperature = round(averageTemperature, 2)
        insertSensors.humidity = round(averageHumidity, 2)
        insertSensors.moisture = currentMoisture
        insertSensors.summary = currentSummary

        insertSensors.save()

        deviceStatusObjectsJSON = {
        'currentTemperatureJSON': round(averageTemperature, 2),
        'currentHumidityJSON': round(averageHumidity, 2),
        'currentMoistureJSON': currentMoisture,
        'currentSummaryJSON': currentSummary,
        }

        return JsonResponse(deviceStatusObjectsJSON)

    if response.POST.get('action') == 'snapImage':
        print(" ")
        print("~Image Captured~")
        print(" ")

        pygame.init()
        pygame.camera.init()
        cam = pygame.camera.Camera("/dev/video0", (960, 720))
        cam.start()
        image = cam.get_image()
        getTime = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        pygame.image.save(image, '/home/pi/Desktop/thesis/thesis/assets/gardenPics/' + getTime + '.jpg')
        cam.stop()

        print(" ")
        print("~Image Processing Started~")
        print(" ")

        class options:
            def __init__(self):
                self.debug = "plot"
                self.outdir = "./assets/gardenPics/"


        args = options()
        #pcv.params.debug = args.debug

        plant_area_list = [] #Plant area array for storage

        img, path, filename = pcv.readimage(filename='./assets/gardenPics/' + getTime + '.jpg', mode="native") # Read image to be used
        #img, path, filename = pcv.readimage(filename= './assets/gardenPics/test.png', mode="native") # Read image to be used

        # START of  Multi Plant Workflow https://plantcv.readthedocs.io/en/stable/multi-plant_tutorial/

        # STEP 1: Check if this is a night image
        # STEP 2: Normalize the white color so you can later
        img1 = pcv.white_balance(img, roi = (600,70,20,20))
        # STEP 3: Rotate the image so that plants line up with grid
        # STEP 4: Shift image
        # STEP 5: Convert image from RGB colorspace to LAB colorspace Keep only the green-magenta channel (grayscale)
        a = pcv.rgb2gray_lab(rgb_img=img1, channel='a')
        # STEP 6: Set a binary threshold on the saturation channel image
        img_binary = pcv.threshold.binary(gray_img=a, threshold=119, max_value=255, object_type='dark')
        # STEP 7: Fill in small objects (speckles)
        fill_image = pcv.fill(bin_img=img_binary, size=100)
        # STEP 8: Dilate so that you don't lose leaves (just in case)
        dilated = pcv.dilate(gray_img=fill_image, ksize=2, i=1)
        # STEP 9: Find objects (contours: black-white boundaries)
        id_objects, obj_hierarchy = pcv.find_objects(img=img1, mask=dilated)
        # STEP 10: Define region of interest (ROI)
        roi_contour, roi_hierarchy = pcv.roi.rectangle(img=img1, x=100, y=160, h=390, w=780)
        # STEP 11: Keep objects that overlap with the ROI
        roi_objects, roi_obj_hierarchy, kept_mask, obj_area = pcv.roi_objects(img=img1, roi_contour=roi_contour,
                                                                                  roi_hierarchy=roi_hierarchy,
                                                                                  object_contour=id_objects,
                                                                                  obj_hierarchy=obj_hierarchy,
                                                                                  roi_type='partial')

        # END of Multi Plant Workflow

        # START of Create Multiple Regions of Interest (ROI) https://plantcv.readthedocs.io/en/stable/roi_multi/

        # Make a grid of ROIs
        roi1, roi_hier1  = pcv.roi.multi(img=img1, coord=(180,260), radius=50, spacing=(150, 200), nrows=2, ncols=5)


        # Loop through and filter each plant, record the area
        for i in range(0, len(roi1)):
            roi = roi1[i]
            hierarchy = roi_hier1[i]
            # Find objects
            filtered_contours, filtered_hierarchy, filtered_mask, filtered_area = pcv.roi_objects(
                img=img, roi_type="partial", roi_contour=roi, roi_hierarchy=hierarchy, object_contour=roi_objects,
                obj_hierarchy=roi_obj_hierarchy)

            # Record the area
            plant_area_list.append(filtered_area)

            if(i<10):
                print(plant_area_list[i])

        # END of Create Multiple Regions of Interest (ROI)

        # Label area by plant ID, leftmost plant has id=0
        plant_area_labels = [i for i in range(0, len(plant_area_list))]

        #out = args.outdir
        # Create a new measurement
        pcv.outputs.add_observation(variable='plant_area', trait='plant area ',
                                    method='plantcv.plantcv.roi_objects', scale='pixels', datatype=list,
                                    value=plant_area_list, label=plant_area_labels)

        # Print areas to XML
        #pcv.print_results(filename="./assets/gardenPics/plant_area_results.xml")

        insertCamera.camera = getTime + '.jpg'
        insertCamera.cameraURL = '../assets/gardenPics/' + getTime + '.jpg'
        insertCamera.plant1 = plant_area_list[0]
        insertCamera.plant2 = plant_area_list[1]
        insertCamera.plant3 = plant_area_list[2]
        insertCamera.plant4 = plant_area_list[3]
        insertCamera.plant5 = plant_area_list[4]
        insertCamera.plant6 = plant_area_list[5]
        insertCamera.plant7 = plant_area_list[6]
        insertCamera.plant8 = plant_area_list[7]
        insertCamera.plant9 = plant_area_list[8]
        insertCamera.plant10 = plant_area_list[9]
        insertCamera.save()

        cameraObjectsSnap = camerasnaps.objects.latest('date')
        countersObjectSnap_first = counters.objects.first()

        date1 = countersObjectSnap_first.date
        date2 = cameraObjectsSnap.date
        print(date1)
        print(date2)     
                
        def numOfDays(date1, date2): 
            return (date2-date1).days
        
        print(numOfDays(date1, date2), "days")       
        
        
        insertCounters.daysCounter = numOfDays(date1, date2)
        insertCounters.save()

        cameraObjectsJSON = {
        'cameraURLJSON': str(cameraObjectsSnap.cameraURL),
        'cameraDateJSON': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p')),
        'daysCounterJSON' : str(numOfDays(date1, date2)),
        'plant1JASON': plant_area_list[0],
        'plant2JASON': plant_area_list[1],
        'plant3JASON': plant_area_list[2],
        'plant4JASON': plant_area_list[3],
        'plant5JASON': plant_area_list[4],
        'plant6JASON': plant_area_list[5],
        'plant7JASON': plant_area_list[6],
        'plant8JASON': plant_area_list[7],
        'plant9JASON': plant_area_list[8],
        'plant10JASON': plant_area_list[9]
        }
        
        return JsonResponse(cameraObjectsJSON)

    if response.POST.get('action') == 'fullReset':
        
        print(" ")
        print("~Database Cleared~")
        print(" ")
        devicestatus.objects.all().delete()
        insertDeviceStatus.fansStatus = 'start'
        insertDeviceStatus.lightsStatus = 'start'
        insertDeviceStatus.waterStatus = 'start'
        insertDeviceStatus.seedStatus = 'start'
        insertDeviceStatus.save()
        
        camerasnaps.objects.all().delete()
        insertCamera.camera = 'defaultBG.jpg'
        insertCamera.cameraURL = '../assets/background/defaultBG.jpg'
        insertCamera.plant1 = 0
        insertCamera.plant2 = 0
        insertCamera.plant3 = 0
        insertCamera.plant4 = 0
        insertCamera.plant5 = 0
        insertCamera.plant6 = 0
        insertCamera.plant7 = 0
        insertCamera.plant8 = 0
        insertCamera.plant9 = 0
        insertCamera.plant10 = 0
        insertCamera.save()

        sensors.objects.all().delete()
        insertSensors.temperature = 0
        insertSensors.humidity = 0
        insertSensors.moisture = 0
        insertSensors.summary = 'start'
        insertSensors.save()
        
        counters.objects.all().delete()
        insertCounters.daysCounter = 0
        insertCounters.save()
        
        sensorsObjectsReset = sensors.objects.latest('date')
        
        daysJSON = {
        'day1Formatted': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p')),
        'temperatureJSON': sensorsObjectsReset.temperature,
        'humidityJSON': sensorsObjectsReset.humidity,
        'moistureJSON': sensorsObjectsReset.moisture,
        'summaryJSON': sensorsObjectsReset.summary,
               
        }

        return JsonResponse(daysJSON)



    if response.POST.get('action') == 'onFan':

        print(" ")
        print("~Fans Activated~")
        print(" ")

        GPIO.output(20, GPIO.HIGH)
        GPIO.output(26, GPIO.HIGH)

        insertDeviceStatus.fansStatus = 'Activated'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offFan':

        print(" ")
        print("~Fans deactivated~")
        print(" ")

        GPIO.output(20, GPIO.LOW)
        GPIO.output(26, GPIO.LOW)

        insertDeviceStatus.fansStatus = 'Deactivated'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onLights':

        print(" ")
        print("~Lights Activated~")
        print(" ")

        GPIO.output(21, GPIO.HIGH)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'Activated'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offLights':

        print(" ")
        print("~Lights Deactivated~")
        print(" ")

        GPIO.output(21, GPIO.LOW)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'Deactivated'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onWater':

        print(" ")
        print("~Water System Activated~")
        print(" ")

        GPIO.output(16, GPIO.HIGH)
        GPIO.output(19, GPIO.HIGH)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'Activated'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offWater':

        print(" ")
        print("~Water System Deactivated~")
        print(" ")

        GPIO.output(16, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'Deactivated'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onSeed':

        print(" ")
        print("~Seeder Activated~")
        print(" ")

        GPIO.output(12, GPIO.HIGH)
        GPIO.output(6, GPIO.HIGH)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'Activated'
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offSeed':

        print(" ")
        print("~Seeder Deactivated~")
        print(" ")

        GPIO.output(12, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'Deactivated'
        insertDeviceStatus.save()

    # Dito nakalagay sa baba kasi if sa taas,
    # mauuna kunin data before saving the sensor data so late ng isang query
    sensorsObjects = sensors.objects.latest('date')
    cameraObjects = camerasnaps.objects.latest('date')
    countersObject = counters.objects.latest('date')
    countersObject_first = counters.objects.first()

    myObjects = {'deviceStatusObjects': deviceStatusObjects, 
                 'countersObject': countersObject, 'countersObject_first': countersObject_first, 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects}

    return render(response, 'main.html', context=myObjects)


def databasePage(response):

    deviceStatusObjects = devicestatus.objects.all()
    sensorsObjects = sensors.objects.all()
    cameraObjects = camerasnaps.objects.all()

    myObjects = {'deviceStatusObjects': deviceStatusObjects,
                 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects}

    return render(response, 'database.html', context=myObjects)






