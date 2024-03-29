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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import (
    include,
    path
)

from common import views as common_views
from conversations import views as conversations_views
from pages import views as pages_views
from profiles import views as profiles_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Behaviour
    path('reports/', include('behaviour.urls')),

    # Conversations
    path('conversation/<int:pk>/', conversations_views.conversation,
         name='conversation'),
    path('conversations/', conversations_views.conversations,
         name='conversations'),
    path('start-conversation/<int:pk>/',
         conversations_views.start_conversation,
         name='start-conversation'),

    # Dash
    path('dash/', include('dash.urls')),

    # Meetups
    path('meetups/', include('meetups.urls')),

    # Pages
    path('faqs/', pages_views.faqs, name='faqs'),
    path('', pages_views.landing, name='landing'),

    # Profiles
    path('blocked-list/', profiles_views.blocked_list, name='blocked-list'),
    path('change-password/',
         auth_views.PasswordChangeView.as_view(
             template_name='change_password.html',
             success_url='/change-password/done/'),
         name='change-password'),
    path('change-password/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='change_password_done.html'
         )),
    path('reset-password/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html',
             success_url='/reset-password/done/'),
         name='reset-password'),
    path('reset-password/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html',
         )),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',
             success_url='/reset/done/'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         )),
    path('login/', profiles_views.login, name='login'),
    path('logout/', profiles_views.logout, name='logout'),
    path('profile-block/<int:pk>/', profiles_views.profile_block,
         name='profile-block'),
    path('profile-edit/', profiles_views.profile_edit, name='profile-edit'),
    path('profile-star/<int:pk>/', profiles_views.profile_star,
         name='profile-star'),
    path('search/', profiles_views.search, name='search'),
    path('search/clear/profiles/', profiles_views.clear_search,
         name='clear-search'),
    path('search/clear/username/', profiles_views.clear_username_search,
         name='clear-username-search'),
    path('signup/', profiles_views.signup, name='signup'),
    path('starred-list/', profiles_views.starred_list, name='starred-list'),
    path('username-search/', profiles_views.username_search,
         name='username-search'),
    path('user/<username>/', profiles_views.profile_detail,
         name='profile-detail'),

    # Service worker.
    path('sw.js', common_views.serve_serviceworker_file),
]
