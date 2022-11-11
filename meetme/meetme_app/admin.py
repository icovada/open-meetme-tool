from django.contrib import admin

# Register your models here.
from .models import Event, UserProfile, MeetingRequest, Booking

# customize default django admin site html meta
# default: "Django Administration"
admin.site.site_header = "Open Meet-Me Tool"

admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(MeetingRequest)
admin.site.register(Booking)
