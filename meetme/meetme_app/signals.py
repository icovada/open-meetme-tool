from django.db import transaction
from django.db.models.signals import post_save, pre_save, post_delete
from django.db.models import Q, signals
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from meetme_app.models import Event, Booking, Invite, InvitationStatus


def find_booking_per_invite(instance):
    # get time_slots where both users are not available
    inviter_bookings = Invite.objects.filter(
        Q(Q(inviter=instance.inviter) | Q(invitee=instance.inviter)) & Q(booking__isnull=False))
    invitee_bookings = Invite.objects.filter(
        Q(Q(inviter=instance.invitee) | Q(invitee=instance.invitee)) & Q(booking__isnull=False))

    inviter_busy_time_slots = [x.booking.time_slot for x in inviter_bookings]
    inviter_busy_time_slots = [x.booking.time_slot for x in invitee_bookings]

    first_available_slot = Booking.objects.filter(Q(Q(booked_meeting__isnull=True) & ~Q(
        time_slot__in=inviter_busy_time_slots) & ~Q(time_slot__in=inviter_busy_time_slots))).first()

    if first_available_slot is None:
        # Can't find a slot
        return

    first_available_slot.booked_meeting = instance
    first_available_slot.save()


@receiver(post_save, sender=Event)
def create_timeslots_for_new_event(sender, instance: Event, **kwargs):
    '''
    Create TimeSlots as per Event details
    '''

    if not kwargs.get('created'):
        return

    for time in range(instance.meeting_time_slots):
        for concurrency in range(instance.meeting_concurrencies):
            slot = Booking(fkevent=instance,
                           time_slot=time,
                           concurrency=concurrency)

            slot.save()


@receiver(pre_save, sender=Event)
@transaction.atomic
def expand_timeslots_for_existing_event(sender, instance: Event, **kwargs):
    """
    Check Event is valid when changing parameters.
    Create additional TimeSlots if time_slots or concurrencies have increased

    :raises ValidationError: a numeric field was decreased

    """
    if kwargs.get('created'):
        return

    try:
        old_instance: Event = sender.objects.select_for_update().get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so field hasn't technically changed, but you may want to do something else here.
        pass
    else:
        if instance.meeting_time_slots < old_instance.meeting_time_slots:
            raise ValidationError("Cannot reduce amount of time slots")

        if instance.meeting_concurrencies < old_instance.meeting_concurrencies:
            raise ValidationError("Cannot reduce amount of time slots")

        for time in range(instance.meeting_time_slots):
            for concurrency in range(instance.meeting_concurrencies):
                if time in range(old_instance.meeting_time_slots) and concurrency in range(old_instance.meeting_concurrencies):
                    continue

                slot = Booking(fkevent=instance,
                               time_slot=time,
                               concurrency=concurrency)

                slot.save()


@receiver(post_save, sender=Invite)
def assign_meeting_to_timeslot_on_save(sender, instance: Invite, **kwargs):
    """If event is accepted (accepted_date is not Null), assign to TimeSlot
    if any are available"""

    if instance.status != InvitationStatus.ACCEPTED:
        # Event hasn't been accepted
        return
    
    find_booking_per_invite(instance)



@receiver(post_delete, sender=Invite)
def fill_available_slots_in_same_event(sender, instance:Invite, **kwargs):
    """
    If an event is removed there might be a Booking that just freed up
    Fill them up in order of Invite creation
    """
    
    # Get all accepted Invites that still have no Booking, per event
    event = instance.fkevent
    
    pending_requests = Invite.objects.filter(Q(Q(fkevent=event) & Q(booking__isnull=True) & Q(status=InvitationStatus.ACCEPTED))).order_by('creation_date')
    
    for x in pending_requests:
        find_booking_per_invite(x)
        