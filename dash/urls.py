"""friendli URL Configuration

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

from dash import views as dash_views

urlpatterns = [
    path('', dash_views.dash, name='dash'),
    path('add-conference', dash_views.add_conference,
         name='add-conference'),
    path('blocking', dash_views.blocking,
         name='blocking'),
    path('conference', dash_views.conference,
         name='conference'),
    path('edit-conference', dash_views.edit_conference,
         name='edit-conference'),
    path('edit-language/<pk>', dash_views.edit_language,
         name='edit-language'),
    path('edit-looking-for/<pk>', dash_views.edit_looking_for,
         name='edit-looking-for'),
    path('edit-personal_interest/<pk>',
         dash_views.edit_personal_interest,
         name='edit-personal-interest'),
    path('edit-prof-interest/<pk>', dash_views.edit_prof_interest,
         name='edit-prof-interest'),
    path('languages/', dash_views.languages, name='languages'),
    path('looking-for/', dash_views.looking_for, name='looking-for'),
    path('prof-interests/', dash_views.prof_interests,
         name='prof-interests'),
    path('personal-interests/', dash_views.personal_interests,
         name='personal-interests'),
    path('reports/', dash_views.reports, name='reports'),
    path('update-report/<pk>', dash_views.update_report,
         name='update-report'),
    path('user-list/', dash_views.user_list, name='user-list'),
]
