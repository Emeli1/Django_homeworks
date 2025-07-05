from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CreateGetSensorsView, SensorView, UpdateMeasurement

urlpatterns = [
    path('sensor/', CreateGetSensorsView.as_view()),
    path('sensor/<pk>/', SensorView.as_view()),
    path('measurements/', UpdateMeasurement.as_view())
]
