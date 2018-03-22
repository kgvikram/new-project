from django.urls import path, include
from .import views
from django.contrib.auth.views import LoginView

app_name = 'Mapp'

urlpatterns = [

    path('home', views.home, name='home'),
    path('login', views.login_request, name='login'),
    path('registrationpage', views.registrationpage, name='registrationpage'),
    path('signout', views.logout_function, name='signout'),

    path('createalbum', views.createalbum, name='createalbum'),
    path('createsongs', views.createsongs, name='createsongs'),

    path('viewalbum',views.viewalbum, name='viewalbum'),
    path('viewsong/<int:Album_ID>',views.viewsong, name='viewsong'),

    path('songdetails/<int:Song_ID>', views.songdetails,name='songdetails'),

    path('topviewedsongs', views.topviewedsongs, name='topviewedsongs'),
    path('topratedsongs', views.topratedsongs, name='topratedsongs'),


    path('get_places', views.get_places, name='get_places'),



]
