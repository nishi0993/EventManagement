from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
import json
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from event_app.models import Event
from event_app.services import (createEvent, createTicket, getAllEvents,
                                getEvent, getEventSummary, getEventTicket,
                                getRegisteredEvents, getTicket, updateEvent)
import logging
logger = logging.getLogger(__name__)


class IsEventOwner(BasePermission):
    message = "You are not the owner of this event"
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='event_admin').exists():
            return True
        return False  
        

class ViewEvent(APIView):
    """View all events"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        logger.info("Calling View Event API")
        user = request.user
        kwargs = {'user': user}
        try:
            events = getRegisteredEvents(**kwargs)
            if not events:
                return HttpResponse("No Event to Display", status=status.HTTP_200_OK)
            return JsonResponse({'data':events}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponse("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookTicket(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """Post request to create a ticket."""
        data = json.loads(request.body)
        event_slug = data.get('event_slug')
        if not event_slug:
            return JsonResponse({"message": "Please provide valid event slug"},status=status.HTTP_400_BAD_REQUEST)

        event = getEvent(event_slug)
        if not event:
            return JsonResponse({"message": "Invalid event slug"},status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        kwargs = {'booking_event': event, 'user': user}

        try:
            ticketcreated = createTicket(**kwargs)
            # ticket created successfully
            if ticketcreated.get("status"):
                return JsonResponse({"message": "Ticket created successfully"}, status=status.HTTP_201_CREATED)
            
            # ticket creation failed
            if ticketcreated.get("error"):
                return JsonResponse({"message": ticketcreated.get("error_message")} , status=status.HTTP_400_BAD_REQUEST)
        except:
            # Internal Error occured
            return JsonResponse({"message": "Internal Server error"}, status=status.HTTP_400_BAD_REQUEST)


class ViewTicket(APIView):
    """View a ticket"""
    
    def get(self, request, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        if not ticket_id:
            return HttpResponse("Please provide valid ticket id",status=status.HTTP_400_BAD_REQUEST)
        booking = getTicket(ticket_id)
        if not booking:
            return HttpResponse("Invalid ticket id",status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket_details = getEventTicket(booking)
            return JsonResponse({'data':ticket_details},status=status.HTTP_200_OK)
        except:
            return HttpResponse("Internal Server Response",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     

class CreateEvent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsEventOwner]

    def post(self, request):
        """Moderator create a new event"""
        data = json.loads(request.body)

        event_name = data.get('event_name')
        if not event_name:
            return JsonResponse({"message": "Please provide valid event name"},status=status.HTTP_400_BAD_REQUEST)
        event_mode = data.get('event_mode')
        if not event_mode:
            return JsonResponse({"message": "Please provide valid event mode (online/offline)"},status=status.HTTP_400_BAD_REQUEST)

        kwargs = {
            'event_name': event_name,
            'event_mode': event_mode,
            'event_start_time': data.get('event_start_time'),
            'event_end_time': data.get('event_end_time'),
            'event_venue': data.get('event_venue'),
            'event_description': data.get('event_description'),
            'max_seats': data.get('max_seats'),
            'booking_window_start_time': data.get('booking_window_start_time'),
            'added_by': request.user
        }

        try:
            eventcreated = createEvent(**kwargs)
            # Event created successfully
            if eventcreated.get("status"):
                return JsonResponse({"message": eventcreated.get("message")}, status=status.HTTP_201_CREATED)
            # Event creation failed
            if eventcreated.get("error"):
                return JsonResponse({"message": "Incorrect data to create the event"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Internal Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

class ListEvent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsEventOwner]
    
    def get(self, request):
        try:
            events = getAllEvents()
            if not events:
                return HttpResponse("No Event to Display", status=status.HTTP_200_OK)
            return JsonResponse({'data':events}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponse("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateEvent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsEventOwner]

    def put(self, request, **kwargs):
        """Upadte the event"""
        event_slug = kwargs.get('slug')
        data = json.loads(request.body)

        # sanity check
        # event_slug = data.get('event_slug')
        if not event_slug:
            return JsonResponse({"message": "Please provide valid event slug"},status=status.HTTP_400_BAD_REQUEST)
        event = getEvent(event_slug)
        if not event:
            return JsonResponse({"message": "Invalid event slug"},status=status.HTTP_400_BAD_REQUEST)
        kwargs = {
            # 'event_name': event.event_name,
            'event_mode': data.get('event_mode'),
            'event_start_time': data.get('event_start_time'),
            'event_end_time': data.get('event_end_time'),
            'event_venue': data.get('event_venue'),
            'event_description': data.get('event_description'),
            'max_seats': data.get('max_seats'),
            'booking_window_start_time': data.get('booking_window_start_time'),
            'added_by': request.user.id
        }
        try:
            eventupdated = updateEvent(event, **kwargs)
            # Event created successfully
            if eventupdated.get("status"):
                return JsonResponse({"message": eventupdated.get("message")}, status=status.HTTP_200_OK)
            # Event creation failed
            if eventupdated.get("error"):
                return JsonResponse({"message": eventupdated.get("error_message")}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logger.error("Error occured while updating the event: %s", str(error))
            return JsonResponse({"message": "Internal Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

class EventSummary(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsEventOwner]

    def get(self, request, **kwargs):
        event_slug = kwargs.get('slug')
        if not event_slug:
            return HttpResponse("Please provide valid event slug",status=status.HTTP_400_BAD_REQUEST)
        event = getEvent(event_slug)
        if not event:
            return HttpResponse("Invalid event slug",status=status.HTTP_400_BAD_REQUEST)
        try:
            event_summary_data = getEventSummary(event)
            return JsonResponse({'data':event_summary_data},status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error occured while getting the event summary: %s", str(e))
            return HttpResponse("Internal Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

