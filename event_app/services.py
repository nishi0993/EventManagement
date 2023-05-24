from event_app.models import Booking, Event
from event_app.serializers import EventSerializer, TicketSerializer, EventUpdateSerializer
import datetime
import logging
logger = logging.getLogger(__name__)

def getEvent(event_slug):
    logger.info("Calling service getEvent")
    return Event.objects.get(event_slug=event_slug)

def getRegisteredEvents(**kwargs):
    logger.info("Calling service getRegisteredEvents")
    events = list(Booking.objects.filter(user=kwargs.get('user')).values_list('booking_event__event_slug'))
    return events

def generateTicketId():
    logger.info("Calling service generateTicketId")
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def createTicket(**kwargs):
    logger.info("Calling service createTicket")
    ticket_id = generateTicketId()
    kwargs["ticket_id"] = ticket_id
    try:
        ticket_obj = Booking.objects.create(**kwargs)
        return {"status": True, "message": "Ticket created successfully", "error": False, "data": ticket_obj}
    except Exception as e:
        return {"status": False, "message": "Ticket not created", "error": True, "error_message": str(e)}

def getTicket(ticket_id):
    logger.info("Calling service getTicket")
    return Booking.objects.get(ticket_id=ticket_id)

def getEventTicket(booking):
    logger.info("Calling service getEventTicket")
    event = booking.booking_event
    event_data = TicketSerializer(event).data
    event_data["ticket_id"] = booking.ticket_id
    return event_data

def getAllEvents():
    logger.info("Calling service getAllEvents")
    events = Event.objects.all()
    event_data = EventSerializer(events, many=True).data
    return event_data


def createEvent(**kwargs):
    logger.info("Calling service createEvent")
    event_obj = Event.objects.create(**kwargs)
    if event_obj:
        return {"status": True, "message": "Event created successfully", "error": False, "data": event_obj}
    return {"status": False, "message": "Event not created", "error": True}

def getEventSummary(event):
    logger.info("Calling service getEventSummary")
    event_data = EventSerializer(event).data
    bookings_count = Booking.objects.filter(booking_event=event).count()
    event_data["bookings_count"] = bookings_count
    return event_data

def updateEvent(event, **kwargs):
    logger.info("Calling service updateEvent")
    try:
        event_serializer = EventUpdateSerializer(event, data=kwargs, partial=True)
        if event_serializer.is_valid():
            event_serializer.save()
            return {"status": True, "message": "Event updated successfully", "error": False}
        return {"status": False, "message": "Event not updated", "error": True, "error_message": event_serializer.errors}
    except Exception as error:
        print(error)
        return {"status": False, "message": "Event not updated", "error": True, "error_message": str(error)}