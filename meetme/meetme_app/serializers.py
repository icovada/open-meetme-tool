from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Event, MeetingRequest, Booking


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class MeetingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRequest
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
