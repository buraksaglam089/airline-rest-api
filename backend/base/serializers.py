from rest_framework import serializers
from .models import Airline, Aircraft

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'manufacturer_serial_number', 'type', 'model', 'operator_airline', 'number_of_engines']

class AirlineSerializer(serializers.ModelSerializer):
    aircraft_set = AircraftSerializer(many=True, read_only=True)

    class Meta:
        model = Airline
        fields = ['id', 'airline_name', 'callsign', 'founded_year', 'base_airport', 'aircraft_set']

    def to_internal_value(self, data):
        if 'name' in data:
            data = data.copy()
            data['airline_name'] = data.pop('name')
        return super().to_internal_value(data)