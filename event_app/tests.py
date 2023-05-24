from event_app.views import ViewEvent, BookTicket, ViewTicket, CreateEvent, ListEvent, UpdateEvent, EventSummary    
import json
from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token

# Create text cases for ViewEvent api
class EventTesting(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = Group.objects.create(name='event_admin')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.user.groups.add(self.group)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_event(self):
        url = reverse('create-event')
        data = {
            "event_name": "Testing Event",
            "event_mode": "offline",
            "max_seats": 20,
            "event_start_time": "2023-05-25 12:00:00",
            "event_end_time": "2023-07-25 12:00:00",
            "event_venue": "Google Meet",
            "booking_window_start_time": "2023-05-24 12:00:00"
        }
        response_data = self.client.post(
                            url, 
                            data, 
                            format='json'
                        )
        self.assertEqual(response_data.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data.json()['message'], 'Event created successfully')
    
    def test_view_event_list(self):
        url = reverse('list-event')
        response_data = self.client.get(
                            url
                        )
        self.assertEqual(response_data.status_code, status.HTTP_200_OK)


    def test_book_ticket(self):
        url = reverse('book-ticket')
        
        data = {"event_slug": "testing-event"}        
        response_data = self.client.post(
                            url, 
                            data, 
                            format='json'
                        )
        self.assertEqual(response_data.status_code, status.HTTP_201_CREATED)
        