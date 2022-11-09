from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    meeting_begins = models.TimeField(editable=False)
    meeting_duration_mins = models.PositiveIntegerField(editable=False)
    meeting_time_slots = models.PositiveIntegerField(editable=False)
    meeting_concurrencies = models.PositiveIntegerField(editable=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=30)
    event_participations = models.ManyToManyField(Event)


class MeetingRequest(models.Model):
    fkevent = models.ForeignKey(Event, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invitations_sent")
    invitee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invites_received")
    accepted_date = models.DateTimeField(null=True)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = (
            ("view_sent_invitations", "View sent invitations"),
            ("view_received_invitations", "View received invitations"),
            ('send_invitation', "Send invitation"),
            ('accept_invitation', "Accept invitation")
        )
        constraints = [
            models.UniqueConstraint(
                fields=['fkevent', 'inviter', 'invitee'], name="one_invite_per_pair_per_event")
        ]


class TimeSlot(models.Model):
    fkevent = models.ForeignKey(Event, on_delete=models.CASCADE)
    time_slot = models.PositiveIntegerField()
    concurrency = models.PositiveIntegerField()
    booked_meeting = models.OneToOneField(
        MeetingRequest, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fkevent', 'time_slot', 'concurrency'], name="one_slot_per_room_per_event")
        ]
