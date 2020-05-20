"""goodchat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from meetups import views as meetup_views

urlpatterns = [
    path('', meetup_views.meetups, name='meetups'),
    path('edit/<pk>', meetup_views.edit_meetup,
         name='edit-meetup'),
    path('my/', meetup_views.my_meetups,
         name='my-meetups'),
    path('new/', meetup_views.new_meetup,
         name='new-meetup'),
    path('past/', meetup_views.past_meetups,
         name='past-meetups'),
    path('meetup-star/<int:pk>/', meetup_views.meetup_star,
         name='meetup-star'),
    path('starred-meetups/', meetup_views.starred_meetups,
         name='starred-meetups'),
]
