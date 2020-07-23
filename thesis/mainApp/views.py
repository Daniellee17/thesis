from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import mode_selected
from .models import devices
from .models import sensors
from .models import mode1
from .models import mode2
from .models import mode3
from .models import mode4
from .models import mode1_vision_system
from .models import mode2_vision_system
from .models import mode3_vision_system
from .models import mode4_vision_system

from datetime import datetime
from datetime import date
from time import sleep

import sys
import numpy as np
import cv2
import re
from plantcv import plantcv as pcv

def mainPage(response):

    mode_selected_obj_global = mode_selected.objects.latest('date')
    devices_obj_global = devices.objects.latest('date')

    mode1_obj_global = mode1.objects.latest('date')
    mode2_obj_global = mode2.objects.latest('date')
    mode3_obj_global = mode3.objects.latest('date')
    mode4_obj_global = mode4.objects.latest('date')

    # Create instances so you can insert into the database
    mode_selected_ = mode_selected()
    devices_ = devices()
    devices_2 = devices()
    sensors_ = sensors()

    mode1_ = mode1()
    mode2_ = mode2()
    mode3_ = mode3()
    mode4_ = mode4()

    mode1_vision_system_ = mode1_vision_system()
    mode2_vision_system_ = mode2_vision_system()
    mode3_vision_system_ = mode3_vision_system()
    mode4_vision_system_ = mode4_vision_system()

    if response.POST.get('action') == 'setup':

        print(" ")
        print("--------------------------- GrowSmart Initializing -----------------------------")
        print("Time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("Mode: " + str(mode_selected_obj_global.modeNumber))
        print("Grid: " + mode_selected_obj_global.grid)
        print(" ")
        print(" ")

        json = {
        'modeNumber' :mode_selected_obj_global.modeNumber
        }
        return JsonResponse(json)

    if response.POST.get('action') == 'getSensorValues':
        print(" ")
        print("~Sensor Values Updated~")
        print(" ")

        currentMoisture = 51
        temperature = 68
        temperature2 = 70
        humidity = 68
        humidity2 = 70

        averageTemperature = (temperature + temperature2) / 2
        averageHumidity = (humidity + humidity2) / 2

        temperatureStatus = 'good'
        humidityStatus = 'good'
        soilMoistureStatus = 'good'

        temperatureStatusSummary = "Default"
        humidityStatusSummary = "Default"
        soilMoistureStatusSummary = "Default"

        if(averageTemperature < 20):
            temperatureStatus = 'low' # Too Low
        elif(averageTemperature > 30 ):
            temperatureStatus = 'high' # Too High
        else:
            temperatureStatus = 'good' # Good

        if (averageHumidity < 50):
            humidityStatus = 'low' # Too Low
        elif (averageHumidity > 80):
            humidityStatus = 'high' # Too High
        else:
            humidityStatus = 'good' # Good

        if (currentMoisture <= 30):
            soilMoistureStatus = 'dry'; # Dry
        elif (currentMoisture >= 31 and currentMoisture <= 70):
            soilMoistureStatus = 'moist'; # Moist
        elif (currentMoisture >= 71):
            soilMoistureStatus = 'wet'; # Wet

        if(temperatureStatus == 'high'):
            temperatureStatusSummary = 'Too High!'
        elif (temperatureStatus == 'low'):
            temperatureStatusSummary = 'Too Low!'
        else:
            temperatureStatusSummary = 'Good'

        if (humidityStatus == 'high'):
            humidityStatusSummary = 'Too High!'
        elif (humidityStatus == 'low'):
            humidityStatusSummary = 'Too Low!'
        else:
            humidityStatusSummary = 'Good'

        print("Moisture: "+ str(currentMoisture))
        print("Temp1: " + str(temperature))
        print("Temp2: "+ str(temperature2))
        print("Ave temp: "+ str(round(averageTemperature, 2)))
        print("Hum1: "+ str(humidity))
        print("Hum2: "+ str(humidity2))
        print("Ave humidity: "+ str(round(averageHumidity, 0)))

        # Adaptive Irrigation System Code
        if (soilMoistureStatus == 'dry'):
            soilMoistureStatus = 'Dry!'
            print(" ")
            print("~ Soil moisture is dry, adaptive irrigation system activated~")
            print(" ")
            devices_.fansStatus = devices_obj_global.fansStatus
            devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
            devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
            devices_.calibrationStatus = devices_obj_global.calibrationStatus
            devices_.waterStatus = 'On'
            devices_.seedStatus = devices_obj_global.seedStatus
            devices_.save()

            sleep(1)

            print(" ")
            print("~Adaptive irrigation system deactivated~")
            print(" ")
            devices_2.fansStatus = devices_obj_global.fansStatus
            devices_2.whiteLedStatus = devices_obj_global.whiteLedStatus
            devices_2.rgbLedStatus = devices_obj_global.rgbLedStatus
            devices_2.calibrationStatus = devices_obj_global.calibrationStatus
            devices_2.waterStatus = 'Off'
            devices_2.seedStatus = devices_obj_global.seedStatus
            devices_2.save()

        elif (soilMoistureStatus == 'moist'):
            soilMoistureStatus = 'Moist'
        elif (soilMoistureStatus == 'wet'):
            soilMoistureStatus = 'Wet!'

        if(temperatureStatus == 'low'):
            print(" ")
            print("~Temperatures is low, fans deactivated~")
            print(" ")
            devices_.fansStatus = 'Off'
            devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
            devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
            devices_.calibrationStatus = devices_obj_global.calibrationStatus
            devices_.waterStatus = devices_obj_global.waterStatus
            devices_.seedStatus = devices_obj_global.seedStatus
            devices_.save()
        elif(temperatureStatus == 'high'):
            print(" ")
            print("~Temperatures is high, fans activated~")
            print(" ")
            devices_.fansStatus = 'On'
            devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
            devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
            devices_.calibrationStatus = devices_obj_global.calibrationStatus
            devices_.waterStatus = devices_obj_global.waterStatus
            devices_.seedStatus = devices_obj_global.seedStatus
            devices_.save()
        elif(temperatureStatus != 'low' and humidityStatus == 'high'):
            print(" ")
            print("~Temperatures is not low and humidity is high, fans activated~")
            print(" ")
            devices_.fansStatus = 'On'
            devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
            devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
            devices_.calibrationStatus = devices_obj_global.calibrationStatus
            devices_.waterStatus = devices_obj_global.waterStatus
            devices_.seedStatus = devices_obj_global.seedStatus
            devices_.save()

        sensors_.temperature = round(averageTemperature, 2)
        sensors_.humidity = round(averageHumidity, 0)
        sensors_.moisture = currentMoisture
        sensors_.temperatureStatus = temperatureStatusSummary
        sensors_.humidityStatus = humidityStatusSummary
        sensors_.soilMoistureStatus = soilMoistureStatus
        sensors_.save()

        sensors_obj = sensors.objects.latest('date')
        mode_selected_obj_first = mode_selected.objects.first()
        mode_selected_obj = mode_selected.objects.latest('date')

        date1 = mode_selected_obj_first.date
        date2 = sensors_obj.date

        def numOfDays(date1, date2):
            return (date2-date1).days

        mode_selected_.daysCounter = numOfDays(date1, date2)
        mode_selected_.grid = mode_selected_obj.grid
        mode_selected_.rows = mode_selected_obj.rows
        mode_selected_.columns = mode_selected_obj.columns
        mode_selected_.modeNumber = mode_selected_obj.modeNumber
        mode_selected_.image = mode_selected_obj.image
        mode_selected_.save()

        mode_selected_obj_2 = mode_selected.objects.latest('date')

        json = {
        'daysCounter_json' : str(mode_selected_obj_2.daysCounter),
        'date_json': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p')),
        'temperature_json': sensors_obj.temperature,
        'humidity_json': sensors_obj.humidity,
        'soilMoisture_json': sensors_obj.moisture,
        'temperatureStatus_json' : sensors_obj.temperatureStatus,
        'humidityStatus_json' : sensors_obj.humidityStatus,
        'soilMoistureStatus_json' : sensors_obj.soilMoistureStatus,
        }

        return JsonResponse(json)

    if response.POST.get('action') == 'snapImage':
        mode_selected_obj = mode_selected.objects.latest('date')
        if(mode_selected_obj.modeNumber == 1):
            print(" ")
            print("~[ Mode 1 ] Vision System Starting~")
            print(" ")
            print(" ")

            getTime = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

            class options:
                def __init__(self):
                    self.debug = "plot"
                    self.outdir = "./assets/gardenPics/"


            args = options()
            #pcv.params.debug = args.debug

            plant_area_list = [] #Plant area array for storage

            #img, path, filename = pcv.readimage(filename='./assets/gardenPics/' + getTime + '.jpg', modeNumber="native") # Read image to be used
            img, path, filename = pcv.readimage(filename= './assets/gardenPics/test.jpg', mode="native") # Read image to be used

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


            mode1_vision_system_.image = '../assets/gardenPics/' + 'test' + '.jpg'
            mode1_vision_system_.plant1 = plant_area_list[0]
            mode1_vision_system_.plant2 = plant_area_list[1]
            mode1_vision_system_.plant3 = plant_area_list[2]
            mode1_vision_system_.plant4 = plant_area_list[3]
            mode1_vision_system_.plant5 = plant_area_list[4]
            mode1_vision_system_.plant6 = plant_area_list[5]
            mode1_vision_system_.plant7 = plant_area_list[6]
            mode1_vision_system_.plant8 = plant_area_list[7]
            mode1_vision_system_.plant9 = plant_area_list[8]
            mode1_vision_system_.plant10 = plant_area_list[9]
            mode1_vision_system_.save()

            mode1_visionSystem_obj_afterInsertion = mode1_vision_system.objects.latest('date')
            mode_selected_obj_first = mode_selected.objects.first()
            mode_selected_obj = mode_selected.objects.latest('date')

            date1 = mode_selected_obj_first.date
            date2 = mode1_visionSystem_obj_afterInsertion.date

            def numOfDays(date1, date2):
                return (date2-date1).days

            mode_selected_.daysCounter = numOfDays(date1, date2)
            mode_selected_.grid = mode_selected_obj.grid
            mode_selected_.rows = mode_selected_obj.rows
            mode_selected_.columns = mode_selected_obj.columns
            mode_selected_.modeNumber = mode_selected_obj.modeNumber
            mode_selected_.image = '../assets/gardenPics/' + getTime + '.jpg'
            mode_selected_.save()

            json = {
            'image_json': str(mode1_vision_system_.image),
            'cameraDateJSON': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p')),
            'daysCounter_json' : str(numOfDays(date1, date2)),
            'plant1_json': mode1_vision_system_.plant1,
            'plant2_json': mode1_vision_system_.plant2,
            'plant3_json': mode1_vision_system_.plant3,
            'plant4_json': mode1_vision_system_.plant4,
            'plant5_json': mode1_vision_system_.plant5,
            'plant6_json': mode1_vision_system_.plant6,
            'plant7_json': mode1_vision_system_.plant7,
            'plant8_json': mode1_vision_system_.plant8,
            'plant9_json': mode1_vision_system_.plant9,
            'plant10_json': mode1_vision_system_.plant10
            }

            return JsonResponse(json)

        if(mode_selected_obj.modeNumber == 2):
            print(" ")
            print("~[ Mode 2 ] Vision System Starting~")
            print(" ")
            print(" ")

        if(mode_selected_obj.modeNumber == 3):
            print(" ")
            print("~[ Mode 3 ] Vision System Starting~")
            print(" ")
            print(" ")

        if(mode_selected_obj.modeNumber == 4):
            print(" ")
            print("~[ Mode 4 ] Vision System Starting~")
            print(" ")
            print(" ")

    if response.POST.get('action') == 'onMode1':

        print(" ")
        print("~Mode 1 Activated~")
        print(" ")

        mode_selected_.grid = mode1_obj_global.grid
        mode_selected_.rows = mode1_obj_global.rows
        mode_selected_.columns = mode1_obj_global.columns
        mode_selected_.modeNumber = mode1_obj_global.modeNumber
        mode_selected_.image = '../assets/background/rpiBG.gif'
        mode_selected_.save()

        mode_selected_obj = mode_selected.objects.latest('date')

        json = {
        'image_json': mode_selected_obj.image,
        'grid_json': mode_selected_obj.grid,
        'mode_json': mode_selected_obj.modeNumber,
        }

        return JsonResponse(json)

    if response.POST.get('action') == 'onMode2':

        print(" ")
        print("~Mode 2 Activated~")
        print(" ")

        mode_selected_.grid = mode2_obj_global.grid
        mode_selected_.rows = mode2_obj_global.rows
        mode_selected_.columns = mode2_obj_global.columns
        mode_selected_.modeNumber = mode2_obj_global.modeNumber
        mode_selected_.image = '../assets/background/rpiBG.gif'
        mode_selected_.save()

        mode_selected_obj = mode_selected.objects.latest('date')

        json = {
        'image_json': mode_selected_obj.image,
        'grid_json': mode_selected_obj.grid,
        'mode_json': mode_selected_obj.modeNumber,
        }

        return JsonResponse(json)

    if response.POST.get('action') == 'onMode3':

        print(" ")
        print("~Mode 3 Activated~")
        print(" ")

        mode_selected_.grid = mode3_obj_global.grid
        mode_selected_.rows = mode3_obj_global.rows
        mode_selected_.columns = mode3_obj_global.columns
        mode_selected_.modeNumber = mode3_obj_global.modeNumber
        mode_selected_.image = '../assets/background/rpiBG.gif'
        mode_selected_.save()

        mode_selected_obj = mode_selected.objects.latest('date')

        json = {
        'image_json': mode_selected_obj.image,
        'grid_json': mode_selected_obj.grid,
        'mode_json': mode_selected_obj.modeNumber,
        }

        return JsonResponse(json)

    if response.POST.get('action') == 'onMode4':

        print(" ")
        print("~Mode 4 Activated~")
        print(" ")

        mode_selected_.grid = mode4_obj_global.grid
        mode_selected_.rows = mode4_obj_global.rows
        mode_selected_.columns = mode4_obj_global.columns
        mode_selected_.modeNumber = mode4_obj_global.modeNumber
        mode_selected_.image = '../assets/background/rpiBG.gif'
        mode_selected_.save()

        mode_selected_obj = mode_selected.objects.latest('date')

        json = {
        'image_json': mode_selected_obj.image,
        'grid_json': mode_selected_obj.grid,
        'mode_json': mode_selected_obj.modeNumber,
        }

        return JsonResponse(json)

    if response.POST.get('action') == 'onFan':

        print(" ")
        print("~Air Circulation System Activated~")
        print(" ")

        devices_.fansStatus = 'On'
        devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
        devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
        devices_.calibrationStatus = devices_obj_global.calibrationStatus
        devices_.waterStatus = devices_obj_global.waterStatus
        devices_.seedStatus = devices_obj_global.seedStatus
        devices_.save()


    if response.POST.get('action') == 'offFan':

        print(" ")
        print("~Air Circulation System Deactivated~")
        print(" ")

        devices_.fansStatus = 'Off'
        devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
        devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
        devices_.calibrationStatus = devices_obj_global.calibrationStatus
        devices_.waterStatus = devices_obj_global.waterStatus
        devices_.seedStatus = devices_obj_global.seedStatus
        devices_.save()

    if response.POST.get('action') == 'onWhiteLed':

        print(" ")
        print("~White LED Activated~")
        print(" ")

        devices_.fansStatus = devices_obj_global.fansStatus
        devices_.whiteLedStatus = 'On'
        devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
        devices_.calibrationStatus = devices_obj_global.calibrationStatus
        devices_.waterStatus = devices_obj_global.waterStatus
        devices_.seedStatus = devices_obj_global.seedStatus
        devices_.save()

    if response.POST.get('action') == 'offWhiteLed':

        print(" ")
        print("~White LED Deactivated~")
        print(" ")

        devices_.fansStatus = devices_obj_global.fansStatus
        devices_.whiteLedStatus = 'Off'
        devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
        devices_.calibrationStatus = devices_obj_global.calibrationStatus
        devices_.waterStatus = devices_obj_global.waterStatus
        devices_.seedStatus = devices_obj_global.seedStatus
        devices_.save()

    if response.POST.get('action') == 'onRgbLed':

        print(" ")
        print("~Grow Lights Activated~")
        print(" ")

        devices_.fansStatus = devices_obj_global.fansStatus
        devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
        devices_.rgbLedStatus = 'On'
        devices_.calibrationStatus = devices_obj_global.calibrationStatus
        devices_.waterStatus = devices_obj_global.waterStatus
        devices_.seedStatus = devices_obj_global.seedStatus
        devices_.save()


    if response.POST.get('action') == 'offRgbLed':

        print(" ")
        print("~Grow Lights Deactivated~")
        print(" ")

        devices_.fansStatus = devices_obj_global.fansStatus
        devices_.whiteLedStatus =  devices_obj_global.whiteLedStatus
        devices_.rgbLedStatus = 'Off'
        devices_.calibrationStatus = devices_obj_global.calibrationStatus
        devices_.waterStatus = devices_obj_global.waterStatus
        devices_.seedStatus = devices_obj_global.seedStatus
        devices_.save()

    if response.POST.get('action') == 'onWater':

        sensors_water = sensors.objects.latest('date')

        if (sensors_water.moisture < 50):
            print(" ")
            print("Soil Moisture: " + str(sensors_water.moisture))
            print("~Automatic Irrigation System Activated~")
            print(" ")

            devices_.fansStatus = devices_obj_global.fansStatus
            devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
            devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
            devices_.calibrationStatus = devices_obj_global.calibrationStatus
            devices_.waterStatus = 'On'
            devices_.seedStatus = devices_obj_global.seedStatus
            devices_.save()

            sleep(1)

            print(" ")
            print("~Automatic Irrigation System Deactivated~")
            print(" ")

            devices_2.fansStatus = devices_obj_global.fansStatus
            devices_2.whiteLedStatus = devices_obj_global.whiteLedStatus
            devices_2.rgbLedStatus = devices_obj_global.rgbLedStatus
            devices_2.calibrationStatus = devices_obj_global.calibrationStatus
            devices_2.waterStatus = 'Off'
            devices_2.seedStatus = devices_obj_global.seedStatus
            devices_2.save()

        else:
            print(" ")
            print("Soil Moisture: " + str(sensors_water.moisture))
            print("~Automatic Irrigation System Can't Activate~")
            print(" ")

    if response.POST.get('action') == 'onCalibration':

        print(" ")
        print("~Calibration Activated~")
        print(" ")

        devices_.fansStatus = devices_obj_global.fansStatus
        devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
        devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
        devices_.calibrationStatus = 'On'
        devices_.waterStatus = devices_obj_global.waterStatus
        devices_.seedStatus = devices_obj_global.seedStatus
        devices_.save()

        sleep(1)

        print(" ")
        print("~Calibration Deactivated~")
        print(" ")

        devices_2.fansStatus = devices_obj_global.fansStatus
        devices_2.whiteLedStatus = devices_obj_global.whiteLedStatus
        devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
        devices_2.calibrationStatus = 'Off'
        devices_2.waterStatus = devices_obj_global.waterStatus
        devices_2.seedStatus = devices_obj_global.seedStatus
        devices_2.save()


    if response.POST.get('action') == 'onSeed':

        print(" ")
        print("~Seeding System Activated~")
        print(" ")

        devices_.fansStatus = devices_obj_global.fansStatus
        devices_.whiteLedStatus = devices_obj_global.whiteLedStatus
        devices_.rgbLedStatus = devices_obj_global.rgbLedStatus
        devices_.calibrationStatus = devices_obj_global.calibrationStatus
        devices_.waterStatus = devices_obj_global.waterStatus
        devices_.seedStatus = 'On'
        devices_.save()

        sleep(1)

        print(" ")
        print("~Seeding System Deactivated~")
        print(" ")

        devices_2.fansStatus = devices_obj_global.fansStatus
        devices_2.whiteLedStatus = devices_obj_global.whiteLedStatus
        devices_2.rgbLedStatus = devices_obj_global.rgbLedStatus
        devices_2.calibrationStatus = devices_obj_global.calibrationStatus
        devices_2.waterStatus = devices_obj_global.waterStatus
        devices_2.seedStatus = 'Off'
        devices_2.save()

    if response.POST.get('action') == 'fullReset':

        print(" ")
        print("~Formatting Database, Turning Off Devices...~")
        print(" ")
        print(" ")
        print(" ")

        mode_selected.objects.all().delete()
        mode_selected_.daysCounter = 0
        mode_selected_.grid = mode1_obj_global.grid
        mode_selected_.rows = mode1_obj_global.rows
        mode_selected_.columns = mode1_obj_global.columns
        mode_selected_.modeNumber = mode1_obj_global.modeNumber
        mode_selected_.image = '../assets/background/rpiBG.gif'
        mode_selected_.save()

        devices.objects.all().delete()
        devices_.calibrationStatus = 'Off'
        devices_.fansStatus = 'Off'
        devices_.whiteLedStatus = 'Off'
        devices_.rgbLedStatus = 'Off'
        devices_.waterStatus = 'Off'
        devices_.seedStatus = 'Off'
        devices_.save()

        sensors.objects.all().delete()
        sensors_.temperature = 0
        sensors_.humidity = 0
        sensors_.moisture = 0
        sensors_.temperatureStatus = "Good"
        sensors_.humidityStatus = "Good"
        sensors_.soilMoistureStatus = "Good"
        sensors_.save()

        mode1.objects.all().delete()
        mode1_.grid = '2x5'
        mode1_.rows = 2
        mode1_.columns = 5
        mode1_.modeNumber = 1
        mode1_.save()

        mode2.objects.all().delete()
        mode2_.grid = '2x4'
        mode2_.rows = 2
        mode2_.columns = 4
        mode2_.modeNumber = 2
        mode2_.save()

        mode3.objects.all().delete()
        mode3_.grid = '3x6'
        mode3_.rows = 3
        mode3_.columns = 6
        mode3_.modeNumber = 3
        mode3_.save()

        mode4.objects.all().delete()
        mode4_.grid = '3x4'
        mode4_.rows = 3
        mode4_.columns = 4
        mode4_.modeNumber = 4
        mode4_.save()

        mode1_vision_system.objects.all().delete()
        mode1_vision_system_.image = '../assets/background/rpiBG.gif'
        mode1_vision_system_.plant1 = 0
        mode1_vision_system_.plant2 = 0
        mode1_vision_system_.plant3 = 0
        mode1_vision_system_.plant4 = 0
        mode1_vision_system_.plant5 = 0
        mode1_vision_system_.plant6 = 0
        mode1_vision_system_.plant7 = 0
        mode1_vision_system_.plant8 = 0
        mode1_vision_system_.plant9 = 0
        mode1_vision_system_.plant10 = 0
        mode1_vision_system_.save()

        mode2_vision_system.objects.all().delete()
        mode2_vision_system_.image = '../assets/background/rpiBG.gif'
        mode2_vision_system_.plant1 = 0
        mode2_vision_system_.plant2 = 0
        mode2_vision_system_.plant3 = 0
        mode2_vision_system_.plant4 = 0
        mode2_vision_system_.plant5 = 0
        mode2_vision_system_.plant6 = 0
        mode2_vision_system_.plant7 = 0
        mode2_vision_system_.plant8 = 8
        mode2_vision_system_.save()

        mode3_vision_system.objects.all().delete()
        mode3_vision_system_.image = '../assets/background/rpiBG.gif'
        mode3_vision_system_.plant1 = 0
        mode3_vision_system_.plant2 = 0
        mode3_vision_system_.plant3 = 0
        mode3_vision_system_.plant4 = 0
        mode3_vision_system_.plant5 = 0
        mode3_vision_system_.plant6 = 0
        mode3_vision_system_.plant7 = 0
        mode3_vision_system_.plant8 = 0
        mode3_vision_system_.plant9 = 0
        mode3_vision_system_.plant10 = 0
        mode3_vision_system_.plant11 = 0
        mode3_vision_system_.plant12 = 0
        mode3_vision_system_.plant13 = 0
        mode3_vision_system_.plant14 = 0
        mode3_vision_system_.plant15 = 0
        mode3_vision_system_.plant16 = 0
        mode3_vision_system_.plant17 = 0
        mode3_vision_system_.plant18 = 18
        mode3_vision_system_.save()

        mode4_vision_system.objects.all().delete()
        mode4_vision_system_.image = '../assets/background/rpiBG.gif'
        mode4_vision_system_.plant1 = 0
        mode4_vision_system_.plant2 = 0
        mode4_vision_system_.plant3 = 0
        mode4_vision_system_.plant4 = 0
        mode4_vision_system_.plant5 = 0
        mode4_vision_system_.plant6 = 0
        mode4_vision_system_.plant7 = 0
        mode4_vision_system_.plant8 = 0
        mode4_vision_system_.plant9 = 0
        mode4_vision_system_.plant10 = 0
        mode4_vision_system_.plant11 = 0
        mode4_vision_system_.plant12 = 12
        mode4_vision_system_.save()

        mode_selected_obj = mode_selected.objects.latest('date')
        mode1_visionSystem_obj = mode1_vision_system.objects.latest('date')
        sensors_obj = sensors.objects.latest('date')
        devices_obj = devices.objects.latest('date')

        json = {
        'mode_json': mode_selected_obj.modeNumber,
        'grid_json': mode_selected_obj.grid,
        'startDate_json': str(datetime.now().strftime('%b. %d, %Y, %-I:%M %p')),
        'daysCounter_json' : str(mode_selected_obj.daysCounter),

        'calibration_json' : devices_obj.calibrationStatus,
        'fans_json' : devices_obj.fansStatus,
        'whiteLed_json' : devices_obj.whiteLedStatus,
        'rgbLed_json' : devices_obj.rgbLedStatus,
        'water_json' : devices_obj.waterStatus,
        'seeder_json' : devices_obj.seedStatus,

        'temperature_json': sensors_obj.temperature,
        'humidity_json': sensors_obj.humidity,
        'soilMoisture_json': sensors_obj.moisture,
        'temperatureStatus_json': sensors_obj.temperatureStatus,
        'humidityStatus_json': sensors_obj.humidityStatus,
        'soilMoistureStatus_json': sensors_obj.soilMoistureStatus,

        'image_json' : str(mode1_visionSystem_obj.image),
        'plant1_json' : mode1_visionSystem_obj.plant1,
        'plant2_json' : mode1_visionSystem_obj.plant2,
        'plant3_json' : mode1_visionSystem_obj.plant3,
        'plant4_json' : mode1_visionSystem_obj.plant4,
        'plant5_json' : mode1_visionSystem_obj.plant5,
        'plant6_json' : mode1_visionSystem_obj.plant6,
        'plant7_json' : mode1_visionSystem_obj.plant7,
        'plant8_json' : mode1_visionSystem_obj.plant8,
        'plant9_json' : mode1_visionSystem_obj.plant9,
        'plant10_json' : mode1_visionSystem_obj.plant10,

        }

        print("--------------------------- GrowSmart Initializing -----------------------------")
        print("Time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("Mode: " + str(mode_selected_obj.modeNumber))
        print("Grid: " + mode_selected_obj.grid)
        print(" ")
        print(" ")

        return JsonResponse(json)

    sensors_obj_global = sensors.objects.latest('date')
    mode1_vision_system_obj_global = mode1_vision_system.objects.latest('date')
    mode2_vision_system_obj_global = mode2_vision_system.objects.latest('date')
    mode3_vision_system_obj_global = mode3_vision_system.objects.latest('date')
    mode4_vision_system_obj_global = mode4_vision_system.objects.latest('date')
    mode_selected_obj_global_first = mode_selected.objects.first()
    mode_selected_obj_global_2 = mode_selected.objects.latest('date')

    myObj = {'mode_selected_obj_global_first': mode_selected_obj_global_first, 'mode_selected_obj_global_2': mode_selected_obj_global_2, 'devices_obj_global': devices_obj_global,
                'sensors_obj_global': sensors_obj_global, 'mode1_vision_system_obj_global': mode1_vision_system_obj_global, 'mode2_vision_system_obj_global': mode2_vision_system_obj_global
                , 'mode3_vision_system_obj_global': mode3_vision_system_obj_global, 'mode4_vision_system_obj_global': mode4_vision_system_obj_global }

    return render(response, 'main.html', context=myObj)

def databasePage(response):

    devices_obj_global = devices.objects.all()
    sensors_obj_global = sensors.objects.all()
    mode1_vision_system_obj_global = mode1_vision_system.objects.all()
    mode_selected_obj_global = mode_selected.objects.all()
    mode_selected_obj_global_2 = mode_selected.objects.latest('date')

    myObj = {'mode_selected_obj_global': mode_selected_obj_global, 'mode_selected_obj_global_2': mode_selected_obj_global_2, 'devices_obj_global': devices_obj_global,
                'sensors_obj_global': sensors_obj_global, 'mode1_vision_system_obj_global': mode1_vision_system_obj_global}

    return render(response, 'database.html', context=myObj)
