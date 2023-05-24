from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField

User = get_user_model()

# Create your models here.

class Timestamp(models.Model):
    # Store created and updated time stamp
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Event(Timestamp):
    # Event class to store event information
    EVENT_MODE = (
        ('online', 'Online'), 
        ('offline', 'Offline')
        )
    event_name = models.CharField(max_length=200, db_index=True)
    event_slug = AutoSlugField(max_length=300, populate_from="event_name", unique=True, db_index=True)
    event_start_time = models.DateTimeField(blank=True, null=True)
    event_mode = models.CharField(max_length=200, choices=EVENT_MODE)
    event_end_time = models.DateTimeField(blank=True, null=True)
    event_venue = models.CharField(max_length=200, blank=True, null=True)
    event_description = models.CharField(max_length=200, blank=True, null=True)
    max_seats = models.IntegerField(default=0)
    booking_window_start_time = models.DateTimeField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.event_slug


class Booking(Timestamp):
    # Store the booking information of event and users
    ticket_id = models.BigIntegerField(db_index=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, name='booking_event')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ticket_id)


