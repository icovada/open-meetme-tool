import os
from datetime import date, time
from django import setup
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Event, MeetingRequest, Booking
# Create your tests here.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
setup()


class TestEventSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.e = Event(
            name="ciao",
            date=date.today(),
            meeting_begins=time(12, 0),
            meeting_duration_mins=30,
            meeting_time_slots=2,
            meeting_concurrencies=2
        )

        cls.e.save()
        

    def test_timeslot_numbers(self):
        """
        Check the appropriate amount of TimeSlots is created
        """

        self.assertEqual(len(Booking.objects.all()), 4)

        self.e.meeting_time_slots = 4
        self.e.meeting_concurrencies = 4
        self.e.save()

        self.assertEqual(len(Booking.objects.all()), 16)

    def test_event_shrinkage_fails(self):
        """
        Check reducing the number of time slots or concurrencies
        raises a ValidationError exception
        """
        
        self.e.meeting_time_slots = 1
        self.e.meeting_concurrencies = 1
        self.assertRaises(ValidationError, self.e.save)
