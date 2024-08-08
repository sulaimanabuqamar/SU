from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, News, Club, Student, Varsity, HomePage, User, UserManager
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def Home(request, invalid_login = False):
    home_page = HomePage.objects.first()  # Assuming you have one HomePage instance
    if invalid_login:
        return render(request, "home.html", {'home_page': home_page,"login_failed":"true"})
    else:
        return render(request, "home.html", {'home_page': home_page,"login_failed":"false"})

def Events(request):
    events = Event.objects.all()  
    return render(request, "events.html", {'events': events})

def Event_Detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, "event_detail.html", {'event': event})

def News_View(request):
    news = News.objects.all()
    return render(request, "news.html", {'news': news}) 

def News_Detail(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, "news_detail.html", {'news': news})

def Clubs(request):
    clubs = Club.objects.all() 
    return render(request, "clubs.html", {'clubs': clubs}) 

def Club_Detail(request, club_id):
    club = get_object_or_404(Club, id=club_id) 
    events = Event.objects.filter(author=club) 
    heads = club.heads.all()  
    leadership = club.leadership.all()  
    members = club.members.all()  

    return render(request, "club_detail.html", {
        'club': club,
        'events': events,
        'heads': heads, 
        'leadership': leadership,
        'members': members  
    })

def Varsity_View(request):
    varsities = Varsity.objects.all()  
    return render(request, "varsity.html", {'varsities': varsities})

def Varsity_Detail(request, varsity_id):
    varsity = get_object_or_404(Varsity, id=varsity_id) 
    players = varsity.members.all()  
    return render(request, "varsity_detail.html", {'varsity': varsity, 'players': players})

def Student_Detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, "student_detail.html", {'student': student})

def Club_Varsity_login(request: WSGIRequest):
    user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
    if user is not None:
        try:
            print(user.associated_student.color)
            print(user.associated_faculty.color)
            print(user.associated_club.color)
            print(user.associated_varsity.color)
        except:
            pass
        if(user.associated_club is not None or user.associated_varsity is not None):
            login(request, user)
            return redirect("/")
        else:
            print("user exists but is student or faculty")
            return Home(request, True)
    else:
        print("user does not exist")
        return Home(request, True)

@csrf_exempt
def Student_Faculty_login(request: WSGIRequest):
    if request.method == "GET":
        home_page = HomePage.objects.first()  # Assuming you have one HomePage instance
        return render(request, "home.html", {'home_page': home_page,"login_failed":"false"})
    else:
        body = json.loads(request.body.decode('utf-8'))
        print(body)
        try:
            user = User.objects.get(email=body["username"])
            user.set_password(body["password"])
            user.save()
            authuser = authenticate(username=body["username"],password=body["password"])
            login(request, authuser)
            return HttpResponse("{\"message\":\"logged in successfully\"}")
        except Exception as e:
            print(e)
            if "amk" in body["username"] or "amg" in body["username"]:
                return HttpResponse("{\"message\":\"only amb allowed on site\"}")
            user = UserManager.create_user(User.objects, body["username"], body["name"], body["password"])
            user.save()
            authuser = authenticate(username=body["username"],password=body["password"])
            login(request, authuser)
            return HttpResponse("{\"message\":\"logged in successfully\"}")
def Student_Faculty_logout(request: WSGIRequest):
    logout(request)
    return redirect("/")