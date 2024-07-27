from django.urls import path,re_path

from .views import display_video
from .views  import display_web
from .views import submit_operation 
from .views import displaymyoperations
from .views import displaymydelayoperations

from . import views
urlpatterns = [
    #path('display/<path:url>/<str:searchtxt>', display_web, name='display_web'),


    re_path(r'^display/display/(?P<url>.+)/(?P<searchtxt>.*)$', views.display_web, name='display_web'),
     re_path(r'^display/display_video(?P<url>.+)/(?P<searchtxt>.*)$', views.display_video, name='display_video'),
  
     #path('display/display_video/<path:url>/<str:searchtxt>', views.display_video, name='display_video'),
    #re_path(r'^display_web/(?P<url>.+)$',views.display_web, name='display_web'),
    path('submit_operation/', submit_operation, name='submit_operation'),
    path('displaymyoperations/', displaymyoperations, name='displaymyoperations'),
    path('displaymydelayoperations/', displaymydelayoperations, name='displaymydelayoperations'),

] 



