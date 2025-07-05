from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50, verbose_name='Датчик')
    description = models.CharField(max_length=50, verbose_name='Описание')


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Темпиратура')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
