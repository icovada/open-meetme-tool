from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from meetme_app.models import Event, Booking, MeetingRequest


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
                            time_slot = time,
                            concurrency = concurrency)
            
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
        pass # Object is new, so field hasn't technically changed, but you may want to do something else here.
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
                                time_slot = time,
                                concurrency = concurrency)
                
                slot.save()
                
@receiver(post_save, sender=MeetingRequest)
def assign_meeting_to_timeslot_on_accept(sender, instance: MeetingRequest, **kwargs):
    """If event is accepted (accepted_date is not Null), assign to TimeSlot
    if any are available"""
    
    if instance.acknowledge_date is None:
        # Event hasn't been accepted
        return
    
    # get time_slots where both users are not available
    inviter_available = instance.inviter.meeting_request__set.all()

    