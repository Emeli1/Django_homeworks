from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField()

    def __str__(self):
        return self.name


class Measurement(models.Model):
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    update_datetime = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='measurements/', null=True, blank=True)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')

    def __str__(self):
        return f'Температура {self.temperature}°C в {self.sensor.name}'
