from django.shortcuts import render
from django.http import HttpResponse

def mainPage(response):
    return render(response, 'main.html')

def databasePage(response):
    return render(response, 'database.html')




# Create your views here.
