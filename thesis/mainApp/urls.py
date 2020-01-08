from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from . import views as main_views #this says that import views from the current directory were in

urlpatterns = [
    path('', main_views.mainPage, name="mainPage"), #home page
    path('databasePage/', main_views.databasePage, name="databasePage"), #help page

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
