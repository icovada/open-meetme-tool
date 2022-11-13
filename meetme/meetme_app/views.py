from rest_framework import viewsets, status, mixins
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser

from .models import Event, Invite, Booking
from .serializers import EventSerializer, InviteSerializer, BookingSerializer

# Create your views here.

def home_view(request):
    context = {}
    events = Event.objects.all().order_by('datetime')
    context['events'] = events
    
    if isinstance(request.user, AnonymousUser):
        user_events = Event.objects.none()
    else:
        user_events = request.user.event_set.all()

    context['user_events'] = user_events
    return render(request, "meetme_app/index.html", context=context)

def login_view(request):
    return render(request, "meetme_app/login.html")

def event_view(request, slug):
    context = {}
    event = Event.objects.get(slug=slug)
    context["event"] = event
    
    # Becasue doing it inside the template is a pain
    base_time = event.datetime
    duration = timedelta(minutes=event.meeting_duration_mins)

    user_booking_dict = {}
    
    for x in request.user.invitations_sent.filter(booking__isnull=False):
        user_booking_dict[x.booking.time_slot] = x
    
    for x in request.user.invites_received.filter(booking__isnull=False):
        user_booking_dict[x.booking.time_slot] = x

    calendar = {}
    for x in range(event.meeting_time_slots):
        calendar[x] = {
            "begin": base_time+duration*x,
            "meeting": user_booking_dict.get(x)
        }

    context["calendar"] = calendar    
    return render(request, "meetme_app/event.html", context=context)
    

class EventApiViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return EventSerializer

    def get_queryset(self):
        queryset = None
        if self.request.version == 'v1':
            queryset = Event.objects.all()

        return queryset


class InviteApiViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return InviteSerializer

    def get_queryset(self):
        queryset = None
        if self.request.user.is_superuser:
            return Invite.objects.all()

        if self.request.version == 'v1':
            queryset = Invite.objects.filter(inviter=self.request.user)

        return queryset


class MeetingInvitationApiViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return InviteSerializer

    def get_queryset(self):
        queryset = None
        if self.request.user.is_superuser:
            return Invite.objects.all()

        if self.request.version == 'v1':
            queryset = Invite.objects.filter(invitee=self.request.user)

        return queryset


class BookingApiViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return Booking

    def get_queryset(self):
        queryset = None
        if self.request.version == 'v1':
            queryset = Booking.objects.all()

        return queryset
