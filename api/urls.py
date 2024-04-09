from django.urls import path
from . import views
import os

urlpatterns=[
    path('solar', views.getSolarData),
    path('rainwater', views.getRainwaterData),
    path('ping', views.ping),
]