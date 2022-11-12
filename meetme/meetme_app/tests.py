import os
from datetime import date, time, datetime
from django import setup
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import signals

from .models import Event, MeetingRequest, Booking, InvitationStatus
from .signals import assign_meeting_to_timeslot_on_accept
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

        cls.important_user = User.objects.create_user(
            username='important_user', password='12345')
        cls.test_user = User.objects.create_user(
            username='test_user', password='12345')

        cls.user1 = User.objects.create_user(
            username='user1', password='12345')
        cls.user2 = User.objects.create_user(
            username='user2', password='12345')
        cls.user3 = User.objects.create_user(
            username='user3', password='12345')
        cls.user4 = User.objects.create_user(
            username='user4', password='12345')
        cls.user5 = User.objects.create_user(
            username='user5', password='12345')

        cls.important_user.save()
        cls.test_user.save()
        cls.user1.save()
        cls.user2.save()
        cls.user3.save()
        cls.user4.save()
        cls.user5.save()
        
    def generate_accepted_meeting(self, event: Event, inviter: User, invitee: User) -> MeetingRequest:
        invite = MeetingRequest(
            fkevent=event,
            inviter=inviter,
            invitee=invitee,
            acknowledge_date=datetime.now(),
            status=InvitationStatus.ACCEPTED
        )
        
        invite.save()
        return invite
    
    def generate_accepted_meeting_in_slot(self, event: Event, inviter: User, invitee: User, concurrency: int, time_slot: int) -> MeetingRequest:
        # Disconnect signal first or it won't go where we want it to
        signals.post_save.disconnect(assign_meeting_to_timeslot_on_accept, sender=MeetingRequest)

        invite = self.generate_accepted_meeting(event, inviter, invitee)
        booking = Booking.objects.get(concurrency=concurrency, time_slot=time_slot)
        booking.booked_meeting = invite
        booking.save()
        
        # Restore signal
        signals.post_save.connect(assign_meeting_to_timeslot_on_accept, sender=MeetingRequest)
        
        return invite

    def fill_concurrency_0(self):
        """
        imp = important_user
        Final goal: set event schedule like this
        
        +------+-------------+--------------+
        | Slot | Concurr0    | Concurr1     |
        +======+=============+==============+
        | 0    | imp-user1   |              |
        +------+-------------+--------------+
        | 1    | imp-user2   |              |
        +------+-------------+--------------+
        | 2    | user3-user2 |              |
        +------+-------------+--------------+
        | 3    | imp-user3   |              |
        +------+-------------+--------------+
        | 4    | imp-user4   |              |
        +------+-------------+--------------+
        """
        
        self.e.meeting_concurrencies=2
        self.e.meeting_time_slots=5
        self.e.save()
        
        slot00 = self.generate_accepted_meeting_in_slot(self.e, self.user1, self.important_user, 0, 0)
        slot01 = self.generate_accepted_meeting_in_slot(self.e, self.user2, self.important_user, 0, 1)
        slot02 = self.generate_accepted_meeting_in_slot(self.e, self.user3, self.user2, 0, 2)
        slot03 = self.generate_accepted_meeting_in_slot(self.e, self.important_user, self.user3, 0, 3)
        slot04 = self.generate_accepted_meeting_in_slot(self.e, self.important_user, self.user4, 0, 4)

        self.assertEqual(slot00.booking.concurrency, 0)
        self.assertEqual(slot00.booking.time_slot, 0)

        self.assertEqual(slot01.booking.concurrency, 0)
        self.assertEqual(slot01.booking.time_slot, 1)

        self.assertEqual(slot02.booking.concurrency, 0)
        self.assertEqual(slot02.booking.time_slot, 2)

        self.assertEqual(slot03.booking.concurrency, 0)
        self.assertEqual(slot03.booking.time_slot, 3)

        self.assertEqual(slot04.booking.concurrency, 0)
        self.assertEqual(slot04.booking.time_slot, 4)


    def test_fill_bookings(self):
        invite1 = MeetingRequest(
            fkevent=self.e,
            inviter=self.important_user,
            invitee=self.test_user,
        )

        invite2 = MeetingRequest(
            fkevent=self.e,
            inviter=self.user1,
            invitee=self.user2,
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


    def test_get_slot_3_w_important_user(self):
        """
        imp = important_user
        Final goal: get slot 3 with important_user
        
        +------+-------------+--------------+
        | Slot | Concurr0    | Concurr1     |
        +======+=============+==============+
        | 0    | imp-user1   |              |
        +------+-------------+--------------+
        | 1    | imp-user2   |              |
        +------+-------------+--------------+
        | 2    | user3-user2 | imp-testuser |
        +------+-------------+--------------+
        | 3    | imp-user3   |              |
        +------+-------------+--------------+
        | 4    | imp-user4   |              |
        +------+-------------+--------------+
        """
        
        self.fill_concurrency_0()

        slot12 = self.generate_accepted_meeting(self.e, self.test_user, self.important_user)

        self.assertEqual(slot12.booking.concurrency, 1)
        self.assertEqual(slot12.booking.time_slot, 2)
