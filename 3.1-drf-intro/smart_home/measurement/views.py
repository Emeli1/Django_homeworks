from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementDetailsSerializer


class SensorsView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        Sensor.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return Response({'status': 'OK'})


class SensorView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    def patch(self, request, pk):
        sensor = Sensor.objects.get(id=pk)
        sensor.name = request.data['name']
        sensor.description = request.data['description']
        sensor.save()
        return Response({'status': 'OK'})


class MeasurementView(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementDetailsSerializer

    def post(self, request):
        Measurement.objects.create(
            sensor=request.POST.get('sensor'),
            temperature=request.POST.get('temperature')
        )
        return Response({'status': 'OK'})


