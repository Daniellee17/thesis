from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import devicestatus
from .models import sensors
from .models import camerasnaps
from .models import counters
from .models import currentMode
from .models import mode1_pechay
from .models import mode2_plant2
from .models import mode3_plant3
from .models import mode4_plant4
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
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_SENSOR2 = Adafruit_DHT.DHT22
#Image Processing
import numpy as np
import cv2
import re

GPIO.setmode(GPIO.BCM) #Read GPIO# and not pin #!
#RIGHT TERMINAL
GPIO.setup(21, GPIO.OUT)  # Lights, PIN 40 (Right)
GPIO.setup(20, GPIO.OUT)  # Fan1, PIN 38 (Right)
GPIO.setup(16, GPIO.OUT)  # Fan2, PIN 36 (Right)

#LEFT TERMINAL
GPIO.setup(26, GPIO.OUT)  # CalibrationXYZ, PIN 37 (Left)

GPIO.setup(19, GPIO.OUT)  # WaterXYZ, PIN 35 (Left)
GPIO.setup(13, GPIO.OUT)  # SeederXYZ, PIN 33 (Left)

GPIO.setup(6, GPIO.OUT)  # Mode_1, PIN 31 (Left)
GPIO.setup(5, GPIO.OUT)  # Mode_2, PIN 29 (Left)
GPIO.setup(0, GPIO.OUT)  # GrowLights, PIN 27 (Left)

DHT_PIN = 1 # PIN 28 (Right)
DHT_PIN2 = 7 # PIN 26 (Right)


def mainPage(response):

    print(" ")
    print("--------------------------- Main Page Refreshed! -------------------------------")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(" ")
    
    modeObject0 = currentMode.objects.latest('date')
    deviceStatusObjects = devicestatus.objects.latest('date')
    
    if response.POST.get('action') == 'setup':
        print(" ")
        print("~Initializing~")
        print(" ")
        print("Mode: " + str(modeObject0.modeNumber))
        print("Grid: " + modeObject0.grid)
        print(" ")
        print(" ")
        
        json = {
        'grid' :str(modeObject0.grid)
        }

        return JsonResponse(json)


    # Create instance so you can insert into DB
    insertDeviceStatus = devicestatus()
    insertDeviceStatus2 = devicestatus()
    insertDeviceStatus_temperature = devicestatus()
    insertDeviceStatus_humidity = devicestatus()
    insertDeviceStatus_soilMoisture = devicestatus()
    insertDeviceStatus_soilMoisture2 = devicestatus()

    insertCamera = camerasnaps()
    insertSensors = sensors()
    insertCounters = counters()
    insertMode = currentMode()


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
        
        currentMoisture = output
        averageTemperature = (temperature + temperature2) / 2
        averageHumidity = (humidity + humidity2) / 2

        temperatureStatus = 'good'
        humidityStatus = 'good'
        soilMoistureStatus = 'good'

        temperatureStatusSummary = "Default"
        humidityStatusSummary = "Default"
        soilMoistureStatusSummary = "Default"

        if(averageTemperature > 26 ):
            temperatureStatus = 'high' # Too High
        else:
            temperatureStatus = 'good' # Good

        if (averageHumidity < 50):
            humidityStatus = 'low' # Too Low
        elif (averageHumidity > 80):
            humidityStatus = 'high' # Too High
        else:
            temperatureStatus = 11 # Good

        if (currentMoisture >= 10 and currentMoisture <= 30):
            soilMoistureStatus = 'dry'; # Dry
        elif (currentMoisture >= 31 and currentMoisture <= 70):
            soilMoistureStatus = 'moist'; # Moist
        elif (currentMoisture >= 71):
            soilMoistureStatus = 'wet'; # Wet

        if(temperatureStatus == 'high'):
            temperatureStatusSummary = 'Too High!'
        else:
            temperatureStatusSummary = 'Good'

        if (humidityStatus == 'high'):
            humidityStatusSummary = 'Too High!'
        elif (humidityStatus == 'low'):
            humidityStatusSummary = 'Too Low!'
        else:
            humidityStatusSummary = 'Good'
            
        if (soilMoistureStatus == 'dry'):            
            soilMoistureStatus = 'Dry!'
            print(" ")
            print("~ (PIN 19) Watering System Activated~")
            print(" ")
            insertDeviceStatus_soilMoisture.fansStatus = deviceStatusObjects.fansStatus
            insertDeviceStatus_soilMoisture.lightsStatus = deviceStatusObjects.lightsStatus
            insertDeviceStatus_soilMoisture.calibrationStatus = deviceStatusObjects.calibrationStatus
            insertDeviceStatus_soilMoisture.waterStatus = 'On'
            insertDeviceStatus_soilMoisture.seedStatus = deviceStatusObjects.seedStatus
            insertDeviceStatus_soilMoisture.save()
            GPIO.output(19, GPIO.HIGH)
            sleep(1)
            GPIO.output(19, GPIO.LOW)
            print(" ")
            print("~ (PIN 19) Watering System Deactivated~")
            print(" ")
            insertDeviceStatus_soilMoisture2.fansStatus = deviceStatusObjects.fansStatus
            insertDeviceStatus_soilMoisture2.lightsStatus = deviceStatusObjects.lightsStatus
            insertDeviceStatus_soilMoisture2.calibrationStatus = deviceStatusObjects.calibrationStatus
            insertDeviceStatus_soilMoisture2.waterStatus = 'Off'
            insertDeviceStatus_soilMoisture2.seedStatus = deviceStatusObjects.seedStatus
            insertDeviceStatus_soilMoisture2.save()

        elif (soilMoistureStatus == 'moist'):
            soilMoistureStatus = 'Moist'
        elif (soilMoistureStatus == 'wet'):
            soilMoistureStatus = 'Wet!'
            
        print("Temp1: " + str(temperature))
        print("Hum1: "+ str(humidity))
        print("Temp2: "+ str(temperature2))
        print("Hum2: "+ str(humidity2))
        print("Moisture: "+ str(currentMoisture))
        print("Ave temp: "+ str(round(averageTemperature, 2)))
        print("Ave humidity: "+ str(round(averageHumidity, 0)))
          
        if(temperatureStatus == 'low' and humidityStatus == 'low'):
            print(" ")
            print("~Fans Deactivated~")
            print(" ")
            GPIO.output(20, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            insertDeviceStatus_humidity.fansStatus = 'Off'
            insertDeviceStatus_humidity.lightsStatus = deviceStatusObjects.lightsStatus
            insertDeviceStatus_humidity.calibrationStatus = deviceStatusObjects.calibrationStatus
            insertDeviceStatus_humidity.waterStatus = deviceStatusObjects.waterStatus
            insertDeviceStatus_humidity.seedStatus = deviceStatusObjects.seedStatus
            insertDeviceStatus_humidity.save()            
        elif(temperatureStatus == 'high' and humidityStatus == 'high'):
            print(" ")
            print("~Fans Activated~")
            print(" ")
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
            insertDeviceStatus_humidity.fansStatus = 'On'
            insertDeviceStatus_humidity.lightsStatus = deviceStatusObjects.lightsStatus
            insertDeviceStatus_humidity.calibrationStatus = deviceStatusObjects.calibrationStatus
            insertDeviceStatus_humidity.waterStatus = deviceStatusObjects.waterStatus
            insertDeviceStatus_humidity.seedStatus = deviceStatusObjects.seedStatus
            insertDeviceStatus_humidity.save()            
        elif(temperatureStatus == 'low' and humidityStatus == 'high'):
            print(" ")
            print("~Fans Activated~")
            print(" ")
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
            insertDeviceStatus_humidity.fansStatus = 'On'
            insertDeviceStatus_humidity.lightsStatus = deviceStatusObjects.lightsStatus
            insertDeviceStatus_humidity.calibrationStatus = deviceStatusObjects.calibrationStatus
            insertDeviceStatus_humidity.waterStatus = deviceStatusObjects.waterStatus
            insertDeviceStatus_humidity.seedStatus = deviceStatusObjects.seedStatus
            insertDeviceStatus_humidity.save()            
        elif(temperatureStatus == 'high' and humidityStatus == 'low'):
            print(" ")
            print("~Fans Activated~")
            print(" ")
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
            insertDeviceStatus_humidity.fansStatus = 'On'
            insertDeviceStatus_humidity.lightsStatus = deviceStatusObjects.lightsStatus
            insertDeviceStatus_humidity.calibrationStatus = deviceStatusObjects.calibrationStatus
            insertDeviceStatus_humidity.waterStatus = deviceStatusObjects.waterStatus
            insertDeviceStatus_humidity.seedStatus = deviceStatusObjects.seedStatus
            insertDeviceStatus_humidity.save()

        insertSensors.temperature = round(averageTemperature, 2)
        insertSensors.humidity = round(averageHumidity, 0)
        insertSensors.moisture = currentMoisture
        insertSensors.temperatureStatus = temperatureStatusSummary
        insertSensors.humidityStatus = humidityStatusSummary
        insertSensors.soilMoistureStatus = soilMoistureStatus
        insertSensors.save()

        sensorsObjects = sensors.objects.latest('date')
        countersObjectSensors_first = counters.objects.first()

        date1 = countersObjectSensors_first.date
        date2 = sensorsObjects.date

        def numOfDays(date1, date2):
            return (date2-date1).days

        insertCounters.daysCounter = numOfDays(date1, date2)
        insertCounters.save()

        json = {
        'daysCounterJSON' : str(numOfDays(date1, date2)),
        'dateJSON': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p')),
        'currentTemperatureJSON': round(averageTemperature, 2),
        'currentHumidityJSON': round(averageHumidity, 0),
        'currentMoistureJSON': currentMoisture,
        'temperatureStatusJSON' : temperatureStatusSummary,
        'humidityStatusJSON' : humidityStatusSummary,
        'soilMoistureStatusJSON' : soilMoistureStatus,
        }

        return JsonResponse(json)

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

        json = {
        'cameraURLJSON': str(cameraObjectsSnap.cameraURL),
        'cameraDateJSON': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p')),
        'daysCounterJSON' : str(numOfDays(date1, date2)),
        'plant1JSON': plant_area_list[0],
        'plant2JSON': plant_area_list[1],
        'plant3JSON': plant_area_list[2],
        'plant4JSON': plant_area_list[3],
        'plant5JSON': plant_area_list[4],
        'plant6JSON': plant_area_list[5],
        'plant7JSON': plant_area_list[6],
        'plant8JSON': plant_area_list[7],
        'plant9JSON': plant_area_list[8],
        'plant10JSON': plant_area_list[9]
        }

        return JsonResponse(json)

    if response.POST.get('action') == 'fullReset':

        print(" ")
        print("~Database Cleared~")
        print(" ")
        devicestatus.objects.all().delete()
        insertDeviceStatus.calibrationStatus = 'Off'
        insertDeviceStatus.fansStatus = 'Off'
        insertDeviceStatus.lightsStatus = 'Off'
        insertDeviceStatus.waterStatus = 'Off'
        insertDeviceStatus.seedStatus = 'Off'
        insertDeviceStatus.save()

        camerasnaps.objects.all().delete()
        insertCamera.camera = 'rpiBG.gif'
        insertCamera.cameraURL = '../assets/background/rpiBG.gif'
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
        insertSensors.temperatureStatus = "Good"
        insertSensors.humidityStatus = "Good"
        insertSensors.soilMoistureStatus = "Good"
        insertSensors.save()

        counters.objects.all().delete()
        insertCounters.daysCounter = 0
        insertCounters.save()

        mode1Object = mode1_pechay.objects.latest('date')

        currentMode.objects.all().delete()
        insertMode.grid = mode1Object.grid
        insertMode.rows = mode1Object.rows
        insertMode.columns = mode1Object.columns
        insertMode.modeNumber = mode1Object.modeNumber
        insertMode.save()

        countersObjectsReset = counters.objects.latest('date')
        camerasnapsObjectsReset = camerasnaps.objects.latest('date')
        sensorsObjectsReset = sensors.objects.latest('date')
        deviceStatusObjectsReset = devicestatus.objects.latest('date')
        currentModeObjectsReset = currentMode.objects.latest('date')

        json = {
        'day1Formatted': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p')),
        'temperatureJSON': sensorsObjectsReset.temperature,
        'humidityJSON': sensorsObjectsReset.humidity,
        'moistureJSON': sensorsObjectsReset.moisture,
        'temperatureStatusJSON': sensorsObjectsReset.temperatureStatus,
        'humidityStatusJSON': sensorsObjectsReset.humidityStatus,
        'soilMoistureStatusJSON': sensorsObjectsReset.soilMoistureStatus,

        'fansStatusJSON' : deviceStatusObjectsReset.fansStatus,
        'lightsStatusJSON' : deviceStatusObjectsReset.lightsStatus,
        'calibrationStatusJSON' : deviceStatusObjectsReset.calibrationStatus,
        'waterStatusJSON' : deviceStatusObjectsReset.waterStatus,
        'seedStatusJSON' : deviceStatusObjectsReset.seedStatus,

        'cameraJSON' : str(camerasnapsObjectsReset.camera),
        'cameraURLJSON' : str(camerasnapsObjectsReset.cameraURL),
        'plant1JSON' : camerasnapsObjectsReset.plant1,
        'plant2JSON' : camerasnapsObjectsReset.plant2,
        'plant3JSON' : camerasnapsObjectsReset.plant3,
        'plant4JSON' : camerasnapsObjectsReset.plant4,
        'plant5JSON' : camerasnapsObjectsReset.plant5,
        'plant6JSON' : camerasnapsObjectsReset.plant6,
        'plant7JSON' : camerasnapsObjectsReset.plant7,
        'plant8JSON' : camerasnapsObjectsReset.plant8,
        'plant9JSON' : camerasnapsObjectsReset.plant9,
        'plant10JSON' : camerasnapsObjectsReset.plant10,

        'gridJson': currentModeObjectsReset.grid,
        'modeNumberJson': currentModeObjectsReset.modeNumber,
        }

        return JsonResponse(json)


    if response.POST.get('action') == 'onMode1':

        print(" ")
        print("~Mode 1 Activated~")
        print(" ")

        GPIO.output(6, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)

        mode = 1

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

        mode1Object = mode1_pechay.objects.latest('date')

        insertMode.grid = mode1Object.grid
        insertMode.rows = mode1Object.rows
        insertMode.columns = mode1Object.columns
        insertMode.modeNumber = mode1Object.modeNumber
        insertMode.save()

        modeObject = currentMode.objects.latest('date')

        json = {
        'gridJson': modeObject.grid,
        'modeNumberJson': modeObject.modeNumber,
        }

        return JsonResponse(json)

    if response.POST.get('action') == 'onMode2':

        print(" ")
        print("~Mode 2 Activated~")
        print(" ")

        GPIO.output(6, GPIO.LOW)
        GPIO.output(5, GPIO.HIGH)

        mode = 2

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

        mode2Object = mode2_plant2.objects.latest('date')

        insertMode.grid = mode2Object.grid
        insertMode.rows = mode2Object.rows
        insertMode.columns = mode2Object.columns
        insertMode.modeNumber = mode2Object.modeNumber
        insertMode.save()

        modeObject = currentMode.objects.latest('date')

        json = {
        'gridJson': modeObject.grid,
        'modeNumberJson': modeObject.modeNumber,
        }

        return JsonResponse(json)

    if response.POST.get('action') == 'onMode3':

        print(" ")
        print("~Mode 3 Activated~")
        print(" ")

        GPIO.output(6, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)

        mode = 3

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

        mode3Object = mode3_plant3.objects.latest('date')

        insertMode.grid = mode3Object.grid
        insertMode.rows = mode3Object.rows
        insertMode.columns = mode3Object.columns
        insertMode.modeNumber = mode3Object.modeNumber
        insertMode.save()

        modeObject = currentMode.objects.latest('date')

        json = {
        'gridJson': modeObject.grid,
        'modeNumberJson': modeObject.modeNumber,
        }

        return JsonResponse(json)

    if response.POST.get('action') == 'onMode4':

        print(" ")
        print("~Mode 4 Activated~")
        print(" ")

        GPIO.output(6, GPIO.HIGH)
        GPIO.output(5, GPIO.HIGH)

        mode = 4

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

        mode4Object = mode4_plant4.objects.latest('date')

        insertMode.grid = mode4Object.grid
        insertMode.rows = mode4Object.rows
        insertMode.columns = mode4Object.columns
        insertMode.modeNumber = mode4Object.modeNumber
        insertMode.save()

        modeObject = currentMode.objects.latest('date')

        json = {
        'gridJson': modeObject.grid,
        'modeNumberJson': modeObject.modeNumber,
        }

        return JsonResponse(json)


    if response.POST.get('action') == 'onCalibration':

        print(" ")
        print("~ (PIN 26) Calibration Activated~")
        print(" ")

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = 'On'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

        GPIO.output(26, GPIO.HIGH)
        sleep(1)
        GPIO.output(26, GPIO.LOW)

        print(" ")
        print("~ (PIN 26) Calibration Deactivated~")
        print(" ")

        insertDeviceStatus2.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus2.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus2.calibrationStatus = 'Off'
        insertDeviceStatus2.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus2.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus2.save()

    if response.POST.get('action') == 'onFan':

        print(" ")
        print("~Fans Activated~")
        print(" ")

        GPIO.output(20, GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)

        insertDeviceStatus.fansStatus = 'On'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offFan':

        print(" ")
        print("~Fans deactivated~")
        print(" ")

        GPIO.output(20, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)

        insertDeviceStatus.fansStatus = 'Off'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onLights':

        print(" ")
        print("~Lights Activated~")
        print(" ")

        GPIO.output(21, GPIO.HIGH)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'On'
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()


    if response.POST.get('action') == 'offLights':

        print(" ")
        print("~Lights Deactivated~")
        print(" ")

        GPIO.output(21, GPIO.LOW)

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'Off'
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onWater':

        print(" ")
        print("~ (PIN 19) Watering System Activated~")
        print(" ")

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = 'On'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

        GPIO.output(19, GPIO.HIGH)
        sleep(1)
        GPIO.output(19, GPIO.LOW)

        print(" ")
        print("~ (PIN 19) Watering System Deactivated~")
        print(" ")

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = 'Off'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onSeed':

        print(" ")
        print("~ (PIN 13) Seeder Activated~")
        print(" ")

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'On'
        insertDeviceStatus.save()

        GPIO.output(13, GPIO.HIGH)
        sleep(1)
        GPIO.output(13, GPIO.LOW)

        print(" ")
        print("~Seeder Deactivated~")
        print(" ")

        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.calibrationStatus = deviceStatusObjects.calibrationStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'Off'
        insertDeviceStatus.save()

    sensorsObjects = sensors.objects.latest('date')
    cameraObjects = camerasnaps.objects.latest('date')
    countersObject_first = counters.objects.first()
    countersObject = counters.objects.latest('date')
    modeObject = currentMode.objects.latest('date')

    myObjects = {'modeObject': modeObject, 'deviceStatusObjects': deviceStatusObjects,
                 'countersObject': countersObject, 'countersObject_first': countersObject_first, 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects}

    return render(response, 'main.html', context=myObjects)


def databasePage(response):

    deviceStatusObjects = devicestatus.objects.all()
    sensorsObjects = sensors.objects.all()
    cameraObjects = camerasnaps.objects.all()
    countersObjects = counters.objects.all()

    myObjects = {'deviceStatusObjects': deviceStatusObjects,
                 'sensorsObjects': sensorsObjects, 'cameraObjects': cameraObjects, 'countersObjects': countersObjects}

    return render(response, 'database.html', context=myObjects)
