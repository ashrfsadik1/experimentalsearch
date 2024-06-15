from django.urls import path,re_path

from .views import display_video
from .views  import display_web
from .views import submit_operation 
from .views import displaymyoperations
from .views import displaymydelayoperations

from . import views
urlpatterns = [
    path('display/<str:url>/<str:searchtxt>', display_web, name='display_web'),
     path('display/display_video/<str:url>/<str:searchtxt>', views.display_video, name='display_video'),
    #re_path(r'^display_web/(?P<url>.+)$',views.display_web, name='display_web'),
    path('submit_operation/', submit_operation, name='submit_operation'),
    path('displaymyoperations/', displaymyoperations, name='displaymyoperations'),
    path('displaymydelayoperations/', displaymydelayoperations, name='displaymydelayoperations'),

] 



