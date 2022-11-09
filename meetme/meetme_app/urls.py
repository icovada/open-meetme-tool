from django.urls import path, re_path, include
from rest_framework import routers

from .views import (
    EventApiViewSet,
    MeetingRequestApiViewSet,
    MeetingInvitationApiViewSet,
    TimeSlotApiViewSet
)

router = routers.DefaultRouter()
router.register(r'event', EventApiViewSet, basename="Customer")
router.register(r'meetingrequest', MeetingRequestApiViewSet, basename="Host")
router.register(r'meetinginvitation', MeetingInvitationApiViewSet, basename="Service")
router.register(r'timeslot', TimeSlotApiViewSet, basename="Event")

app_name = "meetme_app"

urlpatterns = [
    # main view
    re_path(r'api/(?P<version>v\d)/', include(router.urls))
]
