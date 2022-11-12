from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class InvitationStatus(models.TextChoices):
    ACCEPTED = "ACK", "Accepted"
    REJECTED = "NAK", "Rejected"


class Event(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(primary_key=True)
    date = models.DateField()
    meeting_begins = models.TimeField()
    meeting_duration_mins = models.PositiveIntegerField()
    meeting_time_slots = models.PositiveIntegerField()
    meeting_concurrencies = models.PositiveIntegerField()
    registered_users = models.ManyToManyField(User, null=True, blank=True)


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
    creation_date = models.DateTimeField(default=timezone.now)
    acknowledge_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=6, choices=InvitationStatus.choices, null=True, blank=True)

    class Meta:
        permissions = (
            ("view_sent_invitations", "Can view sent invitations"),
            ("view_received_invitations", "Can view received invitations"),
            ('send_invitation', "Can send invitation"),
            ('accept_invitation', "Can accept invitation")
        )
        constraints = [
            models.UniqueConstraint(
                fields=['fkevent', 'inviter', 'invitee'], name="one_invite_per_pair_per_event")
        ]


class Booking(models.Model):
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
