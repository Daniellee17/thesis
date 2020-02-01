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
DHT_PIN = 1
#Image Processing
import numpy as np
import cv2
import re

GPIO.setmode(GPIO.BCM) #Read GPIO# and not pin #!
GPIO.setup(21, GPIO.OUT)  # Fan1
GPIO.setup(7, GPIO.OUT)  # Fan2
GPIO.setup(20, GPIO.OUT)  # Lights
GPIO.setup(16, GPIO.OUT)  # Water
GPIO.setup(26, GPIO.OUT)  # WaterXYZ
GPIO.setup(12, GPIO.OUT)  # Seeder
GPIO.setup(19, GPIO.OUT)  # SeederXYZ


def mainPage(response):

    print(" ")
    print("--------------------------- Main Page Refreshed! -------------------------------")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(" ")

    deviceStatusObjects = devicestatus.objects.latest('date')

    # Create instance para makapag insert sa DB
    insertDeviceStatus = devicestatus()
    insertCamera = camerasnaps()
    insertSensors = sensors()


    if response.POST.get('action') == 'getSensorValues_':
        print(" ")
        print("~Sensor Values Updated~")
        print(" ")

        # Start SPI connection
        spi = spidev.SpiDev() # Created an object
        spi.open(0,0)

        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)


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
        currentMoisture = output
        currentSummary = 'Temperature and Humidity are okay!!!'

        print(currentTemperature)
        print(currentHumidity)

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
                #self.debug = "print"
                self.outdir = "./assets/gardenPics/"

        args = options()
        #pcv.params.debug = args.debug

        plant_area_list = [] #Plant area array for storage
        img, path, filename = pcv.readimage(filename='./assets/gardenPics/' + getTime + '.jpg', mode="native") # Read image to be used

        # START of  Multi Plant Workflow https://plantcv.readthedocs.io/en/stable/multi-plant_tutorial/

        # STEP 1: Check if this is a night image
        # STEP 2: Normalize the white color so you can later
        img1 = pcv.white_balance(img, roi = (120,130,30,30))
        # STEP 3: Rotate the image so that plants line up with grid
        # STEP 4: Shift image
        # STEP 5: Convert image from RGB colorspace to LAB colorspace Keep only the green-magenta channel (grayscale)
        a = pcv.rgb2gray_lab(rgb_img=img1, channel='a')
        # STEP 6: Set a binary threshold on the saturation channel image
        img_binary = pcv.threshold.binary(gray_img=a, threshold=120, max_value=255, object_type='dark')
        # STEP 7: Fill in small objects (speckles)
        fill_image = pcv.fill(bin_img=img_binary, size=40)
        # STEP 8: Dilate so that you don't lose leaves (just in case)
        dilated = pcv.dilate(gray_img=fill_image, ksize=2, i=1)
        # STEP 9: Find objects (contours: black-white boundaries)
        id_objects, obj_hierarchy = pcv.find_objects(img=img1, mask=dilated)
        # STEP 10: Define region of interest (ROI)
        roi_contour, roi_hierarchy = pcv.roi.rectangle(img=img1, x=0, y=100, h=200, w=400)
        # STEP 11: Keep objects that overlap with the ROI
        roi_objects, roi_obj_hierarchy, kept_mask, obj_area = pcv.roi_objects(img=img1, roi_contour=roi_contour,
                                                                                  roi_hierarchy=roi_hierarchy,
                                                                                  object_contour=id_objects,
                                                                                  obj_hierarchy=obj_hierarchy,
                                                                                  roi_type='partial')

        # END of Multi Plant Workflow

        # START of Create Multiple Regions of Interest (ROI) https://plantcv.readthedocs.io/en/stable/roi_multi/

        # Make a grid of ROIs
        roi1, roi_hier1  = pcv.roi.multi(img=img1, coord=(25,120), radius=20, spacing=(70, 70), nrows=3, ncols=6)

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

        out = args.outdir
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

        cameraObjects0 = camerasnaps.objects.latest('date')

        cameraObjectsJSON = {
        'cameraURLJSON': str(cameraObjects0.cameraURL),
        'cameraDateJSON': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p')),
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


    if response.POST.get('action') == 'onFan':

        print(" ")
        print("~Fans Activated~")
        print(" ")

        GPIO.output(21, GPIO.HIGH)
        GPIO.output(7, GPIO.HIGH)

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
        GPIO.output(7, GPIO.LOW)

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
        GPIO.output(26, GPIO.HIGH)

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
        GPIO.output(26, GPIO.LOW)

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
        GPIO.output(19, GPIO.HIGH)

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
        GPIO.output(19, GPIO.LOW)

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
