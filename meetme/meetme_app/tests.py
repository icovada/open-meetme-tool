import os
from django.test import TestCase
from django import setup

from .models import Event, MeetingRequest, TimeSlot
# Create your tests here.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
setup()

class TestAntani(TestCase):
    def test_antani_discover(self):
        Event(name="ciao")