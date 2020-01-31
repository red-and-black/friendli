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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from channels import views as channels_views
from conversations import views as conversations_views
from dash import views as dash_views
from pages import views as pages_views
from profiles import views as profiles_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Channels
    path('channels/<str:name>/', channels_views.channel, name='channel'),
    path('channels/', channels_views.channels, name='channels'),

    # Conversations
    path('conversation/<int:pk>/', conversations_views.conversation,
         name='conversation'),
    path('conversations/', conversations_views.conversations,
         name='conversations'),
    path('start-conversation/<int:pk>/',
         conversations_views.start_conversation,
         name='start-conversation'),
    path('unread-messages/', conversations_views.unread_messages,
         name='unread-messages'),

    # Dash
    path('dash/', dash_views.dash, name='dash'),
    path('dash/add-channel', dash_views.add_channel, name='add-channel'),
    path('dash/add-conference', dash_views.add_conference,
         name='add-conference'),
    path('dash/conference', dash_views.conference,
         name='conference'),
    path('dash/edit-channel', dash_views.edit_channel, name='edit-channel'),
    path('dash/edit-conference', dash_views.edit_conference,
         name='edit-conference'),
    path('dash/edit-language/<pk>', dash_views.edit_language,
         name='edit-language'),
    path('dash/edit-looking-for/<pk>', dash_views.edit_looking_for,
         name='edit-looking-for'),
    path('dash/edit-personal_interest/<pk>',
         dash_views.edit_personal_interest,
         name='edit-personal-interest'),
    path('dash/edit-prof-interest/<pk>', dash_views.edit_prof_interest,
         name='edit-prof-interest'),
    path('dash/languages/', dash_views.languages, name='languages'),
    path('dash/looking-for/', dash_views.looking_for, name='looking-for'),
    path('dash/prof-interests/', dash_views.prof_interests,
         name='prof-interests'),
    path('dash/personal-interests/', dash_views.personal_interests,
         name='personal-interests'),
    path('user-list/', dash_views.user_list, name='user-list'),

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
]
