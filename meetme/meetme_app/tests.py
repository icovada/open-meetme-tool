import os
from datetime import date, time, datetime
from django import setup
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Event, MeetingRequest, Booking, InvitationStatus
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


class TestBooking(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.e = Event(
            name="ciao",
            date=date.today(),
            meeting_begins=time(12, 0),
            meeting_duration_mins=30,
            meeting_time_slots=2,
            meeting_concurrencies=1
        )

        cls.e.save()

        cls.user1 = User.objects.create_user(
            username='user1', password='12345')
        cls.user2 = User.objects.create_user(
            username='user2', password='12345')
        cls.user3 = User.objects.create_user(
            username='user3', password='12345')
        cls.user4 = User.objects.create_user(
            username='user4', password='12345')

        cls.user1.save()
        cls.user2.save()
        cls.user3.save()
        cls.user4.save()

    def test_fill_bookings(self):
        invite1 = MeetingRequest(
            fkevent=self.e,
            inviter=self.user1,
            invitee=self.user2,
        )

        invite2 = MeetingRequest(
            fkevent=self.e,
            inviter=self.user3,
            invitee=self.user4,
        )

        invite1.save()
        invite2.save()

        invite1.acknowledge_date = datetime.now()
        invite1.status = InvitationStatus.ACCEPTED

        invite1.save()

        self.assertEqual(invite1.booking.time_slot, 0)

        invite2.acknowledge_date = datetime.now()
        invite2.status = InvitationStatus.ACCEPTED

        invite2.save()
        self.assertEqual(invite2.booking.time_slot, 1)
