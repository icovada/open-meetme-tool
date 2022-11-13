from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.

class InvitationStatus(models.TextChoices):
    ACCEPTED = "ACK", "Accepted"
    REJECTED = "NAK", "Rejected"


class Event(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(primary_key=True)
    datetime = models.DateTimeField()
    address = models.TextField()
    meeting_duration_mins = models.PositiveIntegerField()
    meeting_time_slots = models.PositiveIntegerField()
    meeting_concurrencies = models.PositiveIntegerField()
    registered_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)


class Invite(models.Model):
    fkevent = models.ForeignKey(Event, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invites_sent")
    invitee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invites_received")
    creation_date = models.DateTimeField(default=timezone.now)
    acknowledge_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=6, choices=InvitationStatus.choices, null=True, blank=True)

    class Meta:
        permissions = (
            ("view_sent_invites", "Can view sent invites"),
            ("view_received_invites", "Can view received invites"),
            ('send_invite', "Can send invites"),
            ('accept_invite', "Can accept invites")
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
        Invite, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fkevent', 'time_slot', 'concurrency'], name="one_slot_per_room_per_event")
        ]
