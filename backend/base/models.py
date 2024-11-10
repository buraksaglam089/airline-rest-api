from django.db import models

class Airline(models.Model):
    airline_name = models.CharField(max_length=100)
    callsign = models.CharField(max_length=50)
    founded_year = models.IntegerField()
    base_airport = models.CharField(max_length=3)

    def __str__(self):
        return self.airline_name

class Aircraft(models.Model):
    manufacturer_serial_number = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    operator_airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='aircraft_set')
    number_of_engines = models.IntegerField()

    def __str__(self):
        return f"{self.type} {self.model} - {self.manufacturer_serial_number}"