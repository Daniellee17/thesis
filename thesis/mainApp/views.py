from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import devicestatus
from .models import sensors
from .models import camerasnaps

from datetime import datetime

import sys
import numpy as np
import cv2
import re
from plantcv import plantcv as pcv

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
        print(" ")
        print("~Image Processing Started~")
        print(" ")

        getTime = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

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
        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = 'Activated'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offFan':
        print(" ")
        print("~Fans Deactivated~")
        print(" ")
        insertDeviceStatus.fansStatus = 'Deactivated'
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onLights':
        print(" ")
        print("~Lights Activated~")
        print(" ")
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'Activated'
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offLights':
        print(" ")
        print("~Lights Deactivated~")
        print(" ")
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = 'Deactivated'
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
        insertDeviceStatus.waterStatus = 'Activated'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offWater':
        print(" ")
        print("~Watering System deactivated~")
        print(" ")
        label = response.POST.get('label')
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = 'Deactivated'
        insertDeviceStatus.seedStatus = deviceStatusObjects.seedStatus
        insertDeviceStatus.save()

    if response.POST.get('action') == 'onSeed':
        print(" ")
        print("~Seeder Activated~")
        print(" ")
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'Activated'
        insertDeviceStatus.save()

    if response.POST.get('action') == 'offSeed':
        print(" ")
        print("~Seeder deactivated~")
        print(" ")
        insertDeviceStatus.fansStatus = deviceStatusObjects.fansStatus
        insertDeviceStatus.lightsStatus = deviceStatusObjects.lightsStatus
        insertDeviceStatus.waterStatus = deviceStatusObjects.waterStatus
        insertDeviceStatus.seedStatus = 'Deactivated'
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


