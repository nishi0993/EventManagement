from rest_framework.serializers import ModelSerializer
from event_app.models import Event

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventUpdateSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ('event_name', 'created', 'updated')
    
class TicketSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ('max_seats', 'added_by', 'event_slug', 'booking_window_start_time', 'updated')