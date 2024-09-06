from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django import template
import studentsunion.settings as settings
import json
import random
import os
import datetime
# Create your views here.

register = template.Library()


@register.simple_tag
def getUserAttending(email, event_id):
    # return datetime.datetime.now().strftime(format_string)
    event = Event.objects.get(id=event_id)
    if User.objects.get(email=email) in event.attending_Students.all():
        return "checked"
    else:
        return ""


def getUserType(user):
    try:
        userType = ""
        if user.associated_student is not None:
            userType = "student"
        elif user.associated_faculty is not None:
            userType = "faculty"
        elif user.associated_club is not None:
            userType = "club"
        elif user.associated_varsity is not None:
            userType = "varsity"
        return userType
    except:
        return ""
def getVarsities(user):
    varsities = []
    for varsity in Varsity.objects.all():
        if user in varsity.members.all():
            varsities.append(varsity)
    return varsities
def getClubs(user):
    clubs = []
    for club in Club.objects.all():
        if user in club.members.all():
            clubs.append(club)
    return clubs

def Home(request, invalid_login = False):
    home_page = HomePage.objects.first()  # Assuming you have one HomePage instance
    if invalid_login:
        return render(request, "home.html", {'userType':getUserType(request.user),'home_page': home_page,"login_failed":"true"})
    else:
        return render(request, "home.html", {'userType':getUserType(request.user),'home_page': home_page,"login_failed":"false"})

def Events(request):
    events = Event.objects.all()  
    return render(request, "events.html", {'userType':getUserType(request.user),'events': events, 'user': request.user})

def Event_Detail(request, event_id):
    event = Event.objects.get(id=event_id)
    links = event.links.all()
    allUsers = []
    for member in event.author.members.all():
        if member not in event.attending_Students.all():
            allUsers.append(member)
    return render(request, "event_detail.html", {'userType':getUserType(request.user),'event': event, 'links': links, 'allUsers': allUsers, 'user': request.user})

def News_View(request):
    news = News.objects.all()
    if request.user.associated_student is not None:
        grlevel = str(request.user.associated_student.year_level)
        return render(request, "news.html", {'userType':getUserType(request.user),'news': news, 'gradelevel': grlevel})
    else:
        return render(request, "news.html", {'userType':getUserType(request.user),'news': news})  

def News_Detail(request, news_id):
    news = News.objects.get(id=news_id)
    links = news.links.all()
    return render(request, "news_detail.html", {'userType':getUserType(request.user),'news': news, 'links': links})

def Clubs(request):
    clubs = Club.objects.all() 
    return render(request, "clubs.html", {'userType':getUserType(request.user),'clubs': clubs}) 

def Club_Detail(request, club_id):
    club = get_object_or_404(Club, id=club_id) 
    events = Event.objects.filter(author=club) 
    heads = club.heads.all()  
    leadership = club.leadership.all()  
    members = club.members.all()  
    advisors = club.advisors.all()
    links = club.links.all() 

    return render(request, "club_detail.html", {
        'club': club,
        'events': events,
        'heads': heads, 
        'leadership': leadership,
        'members': members, 
        'advisors': advisors,
        'links': links,
        'userType':getUserType(request.user),
    })

def Varsity_View(request):
    varsities = Varsity.objects.all()  
    return render(request, "varsity.html", {'userType':getUserType(request.user),'varsities': varsities})

def Varsity_Detail(request, varsity_id):
    varsity = get_object_or_404(Varsity, id=varsity_id) 
    captains = varsity.captains.all()
    players = varsity.members.all()  
    coaches = varsity.coaches.all()
    links = varsity.links.all()
    return render(request, "varsity_detail.html", {'userType':getUserType(request.user),'varsity': varsity, 'players': players, 'captains': captains, 'coaches': coaches, 'links':links}) 

def Student_Detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, "student_detail.html", {'userType':getUserType(request.user),'student': student})

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
        return render(request, "home.html", {'userType':getUserType(request.user),'home_page': home_page,"login_failed":"false"})
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
            if "almawakeb" in body["username"]: 
                string = ""
                for i in range(10):
                    string += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
                fac = Faculty.objects.create(faculty_db_id=string)
                fac.save()
                user.associated_faculty = fac
                user.save()
                return HttpResponse("{\"message\":\"faculty created successfully\"}")
            if "amb" in body["username"]: 
                return HttpResponse("{\"message\":\"user created successfully complete student setup\"}")
def Student_Faculty_logout(request: WSGIRequest):
    logout(request)
    return redirect("/")
@csrf_exempt
def Finish_Setup_Student(request: WSGIRequest):
    if request.method == "POST":
        student = Student.objects.create(student_db_id=request.POST.get("student_id"),year_level=int(request.POST.get("yearlevel")),section=request.POST.get("sectionletter"))
        student.save()
        request.user.associated_student = student
        request.user.save()
        return redirect("/")
    else:
        return HttpResponse("{\"message\":\"ONLY POST ALLOWED\"}")
def UserProfile(request: WSGIRequest):
    if request.user is None:
        return redirect("/")
    else:
        userType = ""
        memberCount = 0
        clubSlashMembers = None
        if request.user.associated_student is not None:
            userType = "student"
            clubSlashMembers = {"clubs":getClubs(request.user),"varsities":getVarsities(request.user)}
        elif request.user.associated_faculty is not None:
            userType = "faculty"
        elif request.user.associated_club is not None:
            userType = "club"
            memberCount = request.user.associated_club.members.all().count()
            clubSlashMembers = request.user.associated_club.members.all()
        elif request.user.associated_varsity is not None:
            userType = "varsity"
            memberCount = request.user.associated_varsity.members.all().count()
            clubSlashMembers = request.user.associated_varsity.members.all()
        allUsers = User.objects.all()
        events = []
        for event in Event.objects.all():
            if request.user in event.attending_Students.all():
                events.append(event)
        return render(request, "profile.html", {'userType':getUserType(request.user),'url':request.build_absolute_uri(), 'user': request.user, 'userType': userType, 'memberCount': memberCount,"clubSlashMembers": clubSlashMembers, 'allUsers': allUsers, 'attendingEvents':events})

def CreateEvent(request:WSGIRequest):
    if request.user.associated_club is None:
        return HttpResponse("<h1>CLUB ENDPOINT ONLY</h1>")
    if request.method == "GET":
        students = []
        for user in User.objects.all():
            if user.associated_student is not None:
                students.append(user)
        faculty = []
        for user in User.objects.all():
            if user.associated_faculty is not None:
                faculty.append(user)
        return render(request, "create_event.html", {'userType':getUserType(request.user),'user': request.user, 'members': students,  'faculties': faculty}) 
    elif request.method == "POST":
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"event_covers", str(random.randint(11111111,999999999)) + file.name)
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            event = Event.objects.create(author=request.user.associated_club, significant_event=(request.POST.get("significant") is not None), cover=filename.removeprefix(str(settings.BASE_DIR)).replace("/media", ""), title=request.POST.get("title"), text=request.POST.get("content"), summary=request.POST.get("summary"), date=request.POST.get("date"), location=request.POST.get("location"), color=request.user.associated_club, members_only=(request.POST.get("membersonly") is not None), highlight=(request.POST.get("highlight") is not None), group=request.POST.get("gradefilter"), grade=request.POST.get("sectionfilter"))
        else: 
            event = Event.objects.create(author=request.user.associated_club, significant_event=(request.POST.get("significant") is not None), title=request.POST.get("title"), text=request.POST.get("content"), summary=request.POST.get("summary"), date=request.POST.get("date"), location=request.POST.get("location"), color=request.user.associated_club, members_only=(request.POST.get("membersonly") is not None), highlight=(request.POST.get("highlight") is not None), group=request.POST.get("gradefilter"), grade=request.POST.get("sectionfilter"))
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find(" ")], link=link[link.find(" "):])
                event.links.add(linkobj)
        if request.POST.get("membersonly") is not None:
            listofemails = []
            for member in User.objects.all():
                if request.POST.get(member.email) is not None:
                    event.attending_Students.add(member)
                    print("student")
                    print(member)
                    listofemails.append(str(member.email))
            print(listofemails)
            if request.POST.get("significant") is not None:
                if len(listofemails) > 0:
                    send_mail("New Event", "this is a test email from the server", None, listofemails, False)  
                hosemails = []
                if request.GET.get("rania") is not None:
                    hosemails.append("rania.makarem@almawakeb.sch.ae")
                if request.GET.get("rita") is not None:
                    hosemails.append("rita.moussa@almawakeb.sch.ae")
                if request.GET.get("amer") is not None:
                    hosemails.append("amer.alameddine@almawakeb.sch.ae")
                if len(hosemails) > 0:
                    send_mail("New Event", "this is a test email from the server", None, hosemails, False)
        event.save()
        return redirect("/Event/Detail/" + str(event.pk)) 
def ModifyEvent(request: WSGIRequest, event_id):
    event = Event.objects.get(id=event_id)
    if request.user is not event.author:
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS EVENT, OPERATION FAILED</h1>")
    students = []
    for user in User.objects.all():
        if user.associated_student is not None:
            students.append(user)
    faculty = []
    for user in User.objects.all():
        if user.associated_faculty is not None:
            faculty.append(user)
    links = ""
    for link in event.links.all():
        links += link.name + " " + link.link + "\n"
    links = links[:-1]
    membersonly = ""
    if event.members_only:
        membersonly = "checked"
    else:
        membersonly = ""
    if request.method == "GET":
        return render(request, "modify_event.html", {'event':event, 'allUsers': students, 'faculties': faculty, 'links': links, 'membersonly': membersonly})
    elif request.method == "POST":
        event.title = request.POST.get("title")
        event.text = request.POST.get("content")
        event.summary = request.POST.get("summary")
        event.date = request.POST.get("date")
        event.location = request.POST.get("location")
        event.group = request.POST.get("gradefilter")
        event.grade = request.POST.get("sectionfilter")
        event.members_only = request.POST.get("membersonly") is not None
        event.highlight = request.POST.get("highlight") is not None
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"event_covers", str(random.randint(11111111,999999999)) + file.name)
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            event.cover = filename.removeprefix(str(settings.BASE_DIR)).replace("/media", "")
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find(" ")], link=link[link.find(" "):])
                event.links.add(linkobj)
        listofemails = []
        for member in User.objects.all():
            if request.POST.get(member.email) is not None:
                event.attending_Students.add(member)
                print("student")
                print(member)
                listofemails.append(str(member.email))
            else:
                event.attending_Students.remove(member)
                try:
                    listofemails.remove(str(member.email))
                except:
                    pass 
        print(listofemails)
        if request.POST.get("emailstudent") is not None:
            if len(listofemails) > 0:
                send_mail("New Event", "this is a test email from the server", None, listofemails, False)  

        if request.POST.get("emailhos") is not None:
            hosemails = []
            if request.GET.get("rania") is not None:
                hosemails.append("rania.makarem@almawakeb.sch.ae")
            if request.GET.get("rita") is not None:
                hosemails.append("rita.moussa@almawakeb.sch.ae")
            if request.GET.get("amer") is not None:
                hosemails.append("amer.alameddine@almawakeb.sch.ae")
            if len(hosemails) > 0:
                send_mail("New Event", "this is a test email from the server", None, hosemails, False)
        event.save()
        return redirect("/Event/Detail/" + str(event.pk))
def CreateNews(request: WSGIRequest):
    if request.method == "GET":
        return render(request, "create_news.html", {'userType':getUserType(request.user),'user': request.user})
    elif request.method == "POST":
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"news_covers", str(random.randint(11111111,999999999)) + file.name)
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            event = News.objects.create(author=request.user, cover=filename.removeprefix(str(settings.BASE_DIR)).replace("/media", ""), title=request.POST.get("title"), text=request.POST.get("content"), published_date=datetime.datetime.now(), summary=request.POST.get("summary"), highlight=(request.POST.get("highlight") is not None), group=request.POST.get("gradefilter"), grade=request.POST.get("sectionfilter"))  
        else: 
            event = News.objects.create(author=request.user, title=request.POST.get("title"), text=request.POST.get("content"), published_date=datetime.datetime.now(), summary=request.POST.get("summary"), highlight=(request.POST.get("highlight") is not None), group=request.POST.get("gradefilter"), grade=request.POST.get("sectionfilter"))  
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        if linkstr is not None and linkstr != "": 
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find(" ")], link=link[link.find(" "):])
                event.links.add(linkobj)
        event.save()
        return redirect("/News/Detail/" + str(event.pk)) 

def ModifyNews(request: WSGIRequest, news_id):
    news = News.objects.get(id=news_id)
    if request.user is not news.author:
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS NEWS POST, OPERATION FAILED</h1>")
    students = []
    for user in User.objects.all():
        if user.associated_student is not None:
            students.append(user)
    faculty = []
    for user in User.objects.all():
        if user.associated_faculty is not None:
            faculty.append(user)
    links = ""
    for link in news.links.all():
        links += link.name + " " + link.link + "\n"
    links = links[:-1]
    if request.method == "GET":
        return render(request, "modify_news.html", {'news':news, 'allUsers': students, 'faculties': faculty, 'links': links})
    elif request.method == "POST":
        news.title = request.POST.get("title")
        news.text = request.POST.get("content")
        news.summary = request.POST.get("summary")
        news.group = request.POST.get("gradefilter")
        news.grade = request.POST.get("sectionfilter")
        news.highlight = request.POST.get("highlight") is not None
        file = request.FILES.get("coverPhoto")
        if file is not None:
            filename = os.path.join(settings.MEDIA_ROOT,"event_covers", str(random.randint(11111111,999999999)) + file.name)
            with open(filename, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            news.cover = filename.removeprefix(str(settings.BASE_DIR)).replace("/media", "")
        linkstr = request.POST.get("links")
        print("(" + linkstr + ")")
        if linkstr is not None and linkstr != "":
            for link in linkstr.split("\n"):
                linkobj = Links.objects.create(name=link[:link.find(" ")], link=link[link.find(" "):])
                news.links.add(linkobj)
        news.save()
        return redirect("/News/Detail/" + str(news.pk))

def AttendeesListPrintable(request: WSGIRequest, event_id: int):
    event = Event.objects.get(id=event_id)
    return render(request, "printable_attendees_list.html", {'attendees': event.attending_Students.all(), 'event': event})

def removeAttendee(request: WSGIRequest):
    event = Event.objects.get(id=int(request.GET.get("id")))
    if request.user is not event.author:
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS EVENT, OPERATION FAILED</h1>")
    event.attending_Students.remove(request.user.associated_club.members.get(email=request.GET.get("email")))
    return HttpResponse("{\"message\":\"competed\"}")
def addAttendee(request: WSGIRequest):
    event = Event.objects.get(id=int(request.GET.get("id")))
    if request.user is not event.author:
        return HttpResponse("<h1>YOU ARE NOT THE AUTHOR OF THIS EVENT, OPERATION FAILED</h1>")
    event.attending_Students.add(request.user.associated_club.members.get(email=request.GET.get("email")))
    return HttpResponse("{\"message\":\"competed\"}")

def removeClubMember(request: WSGIRequest, sector: str):
    if request.user.associated_club is None:
        return HttpResponse("<h1>YOU ARE NOT A CLUB, OPERATION FAILED</h1>")
    club: Club = request.user.associated_club
    if sector == "Member":
        club.members.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Head":
        club.heads.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Advisor":
        club.advisors.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Leadership":
        club.leadership.remove(User.objects.get(email=request.GET.get("email")))
    else:
        return HttpResponse("{\"message\":\"invalid sector\"}")
    return HttpResponse("{\"message\":\"competed\"}")
def addClubMember(request: WSGIRequest, sector: str):
    if request.user.associated_club is None:
        return HttpResponse("<h1>YOU ARE NOT A CLUB, OPERATION FAILED</h1>")
    club: Club = request.user.associated_club
    if sector == "Member":
        club.members.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Head":
        club.heads.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Advisor":
        club.advisors.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Leadership":
        club.leadership.add(User.objects.get(email=request.GET.get("email")))
    
    return HttpResponse("{\"message\":\"competed\"}")

def removeVarsityPlayer(request: WSGIRequest, sector: str):
    if request.user.associated_varsity is None:
        return HttpResponse("<h1>YOU ARE NOT A VARSITY, OPERATION FAILED</h1>")
    varsity: Varsity = request.user.associated_varsity
    if sector == "Member":
        varsity.members.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Captain":
        varsity.captains.remove(User.objects.get(email=request.GET.get("email")))
    elif sector == "Coach":
        varsity.coaches.remove(User.objects.get(email=request.GET.get("email")))
    varsity.save() 
    return HttpResponse("{\"message\":\"competed\"}")
def addVarsityPlayer(request: WSGIRequest, sector: str):
    if request.user.associated_varsity is None:
        return HttpResponse("<h1>YOU ARE NOT A VARSITY, OPERATION FAILED</h1>")
    varsity: Varsity = request.user.associated_varsity
    if sector == "Member":
        varsity.members.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Captain":
        varsity.captains.add(User.objects.get(email=request.GET.get("email")))
    elif sector == "Coach":
        varsity.coaches.add(User.objects.get(email=request.GET.get("email")))
    varsity.save()
    return HttpResponse("{\"message\":\"competed\"}")
