from django.urls import path, re_path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),

    path('home', views.home, name='home'),
    path('admindash', views.adminDash, name='admindash'),

    path('addsite', views.add_websites, name='add_websites'),
    path('updatesite', views.update_websites, name='update_websites'),

    path('ask', views.ask_query, name='ask_query'),
    path('chat/new', views.new_chat, name='new_chat'),
    path('getnewsession', views.getnewsession, name='get_session'),
    path('chat/session/<str:session_id>', views.chat_session, name='chat_session'),

    path('delete-session', views.delete_session, name='delete_session'),

    path('test', views.test, name='test'),
    re_path(r'^.*$', lambda request: redirect('/login', permanent=False)),
]