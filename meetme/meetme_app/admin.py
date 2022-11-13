from django.contrib import admin

# Register your models here.
from .models import Event, Invite, Booking

# customize default django admin site html meta
# default: "Django Administration"
admin.site.site_header = "Open Meet-Me Tool"

admin.site.register(Event)
admin.site.register(Invite)
admin.site.register(Booking)
