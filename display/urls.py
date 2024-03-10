from django.urls import path

from .views import display_video
from .views  import display_web
 
urlpatterns = [
     path('display/<str:url>/', display_video, name='display_video'),
     path('display_web/<str:url>/', display_web  , name='display_web'),
      


]
