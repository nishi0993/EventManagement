"""
URL configuration for event_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from event_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/event/view', ViewEvent.as_view()),
    path('api/event', CreateEvent.as_view(), name='create-event'),
    path('api/event/<slug:slug>', UpdateEvent.as_view()),
    path('api/ticket/book', BookTicket.as_view(), name='book-ticket'),
    path('api/ticket/<int:ticket_id>', ViewTicket.as_view()),
    path('api/events', ListEvent.as_view(), name='list-event'),
    path('api/event/summary/<slug:slug>', EventSummary.as_view())
]
