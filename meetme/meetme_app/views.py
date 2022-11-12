from rest_framework import viewsets, status, mixins
from django.shortcuts import render


from .models import Event, MeetingRequest, Booking
from .serializers import EventSerializer, MeetingRequestSerializer, BookingSerializer

# Create your views here.

def home_view(request):
    context = {}
    events = Event.objects.all()
    context['events'] = events
    
    if request.user is not None:
        user_events = request.user.event_set.all()
    else:
        user_events = Event.objects.none()

    context['user_events'] = user_events
    return render(request, "meetme_app/index.html", context=context)

def login_view(request):
    return render(request, "meetme_app/login.html")

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
