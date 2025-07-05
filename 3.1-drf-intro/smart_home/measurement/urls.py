from django.urls import path

from .views import SensorsView, MeasurementView

urlpatterns = [
    path('sensor/', SensorsView.as_view()),
    path('sensor/<pk>/', SensorsView.as_view()),
    path('measurements/', MeasurementView.as_view())
]
