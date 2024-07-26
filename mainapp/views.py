from django.shortcuts import render, get_object_or_404

from .models import Event, News, Club, Student, Varsity, HomePage

# Create your views here.

def Home(request):
    home_page = HomePage.objects.first()  # Assuming you have one HomePage instance
    return render(request, "home.html", {'home_page': home_page})

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