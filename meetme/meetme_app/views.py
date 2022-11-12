from rest_framework import viewsets, status, mixins
from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser

from .models import Event, MeetingRequest, Booking
from .serializers import EventSerializer, MeetingRequestSerializer, BookingSerializer

# Create your views here.

def home_view(request):
    context = {}
    events = Event.objects.all().order_by('date')
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
    slots_range = range(event.meeting_time_slots)
    context['time_slots'] = slots_range
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


class MeetingRequestApiViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return MeetingRequestSerializer

    def get_queryset(self):
        queryset = None
        if self.request.user.is_superuser:
            return MeetingRequest.objects.all()

        if self.request.version == 'v1':
            queryset = MeetingRequest.objects.filter(inviter=self.request.user)

        return queryset


class MeetingInvitationApiViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == 'v1':
            return MeetingRequestSerializer

    def get_queryset(self):
        queryset = None
        if self.request.user.is_superuser:
            return MeetingRequest.objects.all()

        if self.request.version == 'v1':
            queryset = MeetingRequest.objects.filter(invitee=self.request.user)

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
