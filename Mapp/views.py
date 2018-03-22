from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from .forms import UserRegistrationForm
from .models import Album_table, Songs_table, Rating_table
from django.db.models import Avg, Max, Min, Count
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'home.html')

def login_request(request):

    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('home')
        else:
            error = True
            return render(request,'login.html',{'error':error})
    else:
        return render(request,'login.html')

def registrationpage(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username'].strip()
            email = userObj['email'].strip()
            password = userObj['password'].strip()
            if not (User.objects.filter(username=username).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('login')
            else:
                registrationerror = True
                form = UserRegistrationForm()
                return render(request,'registration.html',{'form': form,'registrationerror':registrationerror})
    else:
        form = UserRegistrationForm()
        return render(request, 'registration.html', {'form': form})

def logout_function(request):
    logout(request)
    return HttpResponseRedirect('home')

def album(request):
    Album_Instance = Album_table()
    Album_Instance.Album_Name = re.sub(' +',' ',request.POST['Album_name']).strip()
    Album_Instance.Album_Name = Album_Instance.Album_Name[:1].upper() + Album_Instance.Album_Name[1:]
    Album_Instance.Album_Year = request.POST['Year']
    Album_Instance.save()

@login_required
def createalbum(request):
    if request.user.is_authenticated:
        albumerror = False
        if request.method == 'POST':
            Album_Exists = Album_table.objects.filter(Album_Name=request.POST.get('Album_name'))
            if not Album_Exists:
                album(request)
                return render(request,'createalbum.html')
            else:
                albumerror = True
                return render(request,'createalbum.html',{'albumerror':albumerror})
        else:
            return render(request,'createalbum.html')
    else:
        return HttpResponseRedirect('/login')

@login_required
def createsongs(request):
        songerror = False
        createlist = Album_table.objects.all()
        createalbumlist = sorted(createlist, key = lambda Album_table:Album_table.Album_Name)

        duplicatealbum = Album_table.objects.values('Album_Name').annotate(Count('Album_Name')).filter(Album_Name__count__gt=1)

        artistlist = Songs_table.objects.all()
        artistlistinstance = sorted(artistlist, key = lambda Songs_table:Songs_table.Artist_Name)

        if request.method == 'POST':
            form_action = request.POST['form_action']

            if form_action == 'create_song':

                songexists = Songs_table.objects.filter(Q(Album_ID=request.POST.get('album')) & Q(Song_Name=request.POST.get('Song_name')))

                if songexists:
                    songexistserror = True
                    return render(request,'createsongs.html',{'createalbumlist':createalbumlist,'artistlistinstance':artistlistinstance,
                                                              'songexistserror':songexistserror,'duplicatealbum':duplicatealbum})
                else:
                    songinstance = Songs_table()
                    songinstance.Song_Name = re.sub(' +',' ',request.POST['Song_name']).strip()
                    songinstance.Song_Name = songinstance.Song_Name[:1].upper() + songinstance.Song_Name[1:]
                    songinstance.Artist_Name = re.sub(' +',' ',request.POST.get('Artist_name')).strip()
                    songinstance.Artist_Name = songinstance.Artist_Name[:1].upper() + songinstance.Artist_Name[1:]
                    Album_ID_instance = Album_table.objects.get(Album_ID=request.POST.get('album'))
                    Album_ID_instance.save()
                    songinstance.Album_ID = Album_ID_instance
                    songinstance.save()

                    return render(request,'createsongs.html',{'createalbumlist':createalbumlist,'artistlistinstance':artistlistinstance,
                                                              'duplicatealbum':duplicatealbum})

            elif form_action == 'create_album':

                Album_Exists=Album_table.objects.filter(Q(Album_Name=request.POST.get('Album_name')) & Q(Album_Year = request.POST.get('Year')))

                if Album_Exists:
                    songerror = True
                    #return HttpResponse(songerror)
                    return render(request,'createsongs.html',{'createalbumlist':createalbumlist,'artistlistinstance':artistlistinstance,
                                                              'duplicatealbum':duplicatealbum})
                else:
                    album(request)
                    createlist = Album_table.objects.all()
                    createalbumlist = sorted(createlist, key = lambda Album_table:Album_table.Album_Name)
                    return render(request,'createsongs.html',{'createalbumlist':createalbumlist,'artistlistinstance':artistlistinstance,
                                                              'duplicatealbum':duplicatealbum})

        else:

                return render(request,'createsongs.html',{'createalbumlist':createalbumlist,'duplicatealbum':duplicatealbum})


@login_required
def songdetails(request, Song_ID):

        songinfo = Songs_table.objects.get(Song_ID=Song_ID)
        userinstance = User.objects.get(username = request.user.username)
        ratingexists = Rating_table.objects.filter(Song_ID=Song_ID,User_ID=userinstance)

        if ratingexists:
            ratingvalue = ratingexists[0].Ratings
        else:
            ratingvalue = None

        if request.method == 'POST':
            if not ratingexists:
                ratinginstance = Rating_table()
                ratingsonginstance = Songs_table.objects.get(Song_ID=Song_ID)
                userinstance = User.objects.get(username = request.user.username)

                ratinginstance.Song_ID = ratingsonginstance
                ratinginstance.User_ID = userinstance
                ratinginstance.Ratings = request.POST.get('rating')
                ratinginstance.save()
                ratingvalue = ratinginstance.Ratings
                return render(request,'songdetails.html',{'songinfo':songinfo,'ratingexists':int(ratingvalue),
                                                           'range_list':range(1,6)})
            else:
                ratinginstance = Rating_table.objects.get(Rating_ID=ratingexists[0].Rating_ID)
                ratinginstance.Ratings=request.POST.get('rating')
                ratinginstance.save()
                ratingvalue = ratinginstance.Ratings
                return render(request,'songdetails.html',{'songinfo': songinfo,'ratingexists':int(ratingvalue),
                                                          'range_list': range(1,6)})
        else:
            songinfo.Views_No=songinfo.Views_No+ 1
            songinfo.save()
            return render(request, 'songdetails.html',{'songinfo':songinfo,'ratingexists':ratingvalue,
                                                        'range_list':range(1,6)})

@login_required
def viewalbum(request):
    list =Album_table.objects.all()
    albumlist = sorted(list, key = lambda Album_table:Album_table.Album_Name)
    '''
    paginator = Paginator(albumlistsort, 10)

    page = request.GET.get('page')
    albumlist = paginator.get_page(page)'''
    return render(request, 'viewalbum.html', {'albumlist': albumlist})


@login_required
def viewsong(request,Album_ID):
    slist = Songs_table.objects.filter(Album_ID=Album_ID)
    songslist = sorted(slist, key = lambda Songs_table:Songs_table.Song_Name)
    return render(request, 'viewsong.html',{'songslist': songslist})

@login_required
def topviewedsongs(request):
    '''
    viewed = Songs_table.objects.all()
    topviewed = sorted(viewed, key = lambda Songs_table:Songs_table.Views_No, reverse= True)
    return render(request,'topviewedsongs.html',{'topviewed':topviewed})'''

    viewed = Rating_table.objects.values('Song_ID','Song_ID__Song_Name','Song_ID__Artist_Name',
                                         'Song_ID__Views_No','Song_ID__Album_ID__Album_Name').\
        annotate(avg_rating=Avg('Ratings')).order_by('-avg_rating')

    topviewed =viewed.order_by('Song_ID__Views_No').reverse()
    '''
    paginator = Paginator(topviewedlist, 10)
    page = request.GET.get('page')
    topviewed = paginator.get_page(page)
    '''
    return render(request,'topviewedsongs.html',{'topviewed':topviewed})


@login_required
def topratedsongs(request):
        toprated = Rating_table.objects.values('Song_ID','Song_ID__Song_Name','Song_ID__Artist_Name',
                                               'Song_ID__Views_No','Song_ID__Album_ID__Album_Name').\
            annotate(avg_rating=Avg('Ratings')).order_by('-avg_rating')
        '''
        paginator = Paginator(topratedlist, 10)
        page = request.GET.get('page')
        toprated = paginator.get_page(page)'''

        return render(request,'topratedsongs.html',{'toprated':toprated})

def get_places(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    album = Album_table.objects.filter(Album_Name__icontains=q)
    results = []
    for pl in album:
      album_json = {}
      album_json = pl.Album_Name + "," + pl.Album_Year
      results.append(album_json)
    data = JsonResponse.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)