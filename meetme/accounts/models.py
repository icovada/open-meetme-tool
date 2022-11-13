from django.db import models
from django.contrib.auth.models import AbstractUser
from meetme_app.models import Event

class CustomUser(AbstractUser):
    company = models.CharField(max_length=30)
    events = models.ManyToManyField(Event)
