from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from meetme_app.models import Event, TimeSlot


@receiver(post_save, sender=Event)
def create_timeslots_for_new_event(sender: Event, instance, **kwargs):
    '''
    Create TimeSlots as per Event details
    '''

    if not kwargs.get('created'):
        return

    for time in range(instance.meeting_time_slots):
        for concurrency in range(instance.meeting_concurrencies):
            slot = TimeSlot(fkevent=instance,
                            time_slot = time,
                            concurrency = concurrency)
            
            slot.save()
