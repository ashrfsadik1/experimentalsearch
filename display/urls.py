from django.urls import path
from .views import display_page

urlpatterns = [
    path('display/', display_page, name='display_page'),
]
