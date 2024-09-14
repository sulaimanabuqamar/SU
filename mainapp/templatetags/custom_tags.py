from django import template
from mainapp.models import *
from studentsunion import settings
register = template.Library()

@register.simple_tag
def getUserAttending(email, event_id):
    # return datetime.datetime.now().strftime(format_string)
    event = Event.objects.get(id=event_id)
    if User.objects.get(email=email) in event.attending_Students.all():
        return "checked"
    else:
        return ""
@register.simple_tag
def getVacantUsersClub(type, club_id):
    # return datetime.datetime.now().strftime(format_string)
    club = Club.objects.get(id=club_id)
    listofusers = []
    if type == "members":
        for user in User.objects.all():
            if user.associated_student is not None and user not in club.members.all():
                listofusers.append(user)
    elif type == "heads":
        for user in User.objects.all():
            if user.associated_student is not None and user not in club.heads.all():
                listofusers.append(user)
    elif type == "advisors":
        for user in User.objects.all():
            if user.associated_faculty is not None and user not in club.advisors.all():
                listofusers.append(user)
    elif type == "leadership":
        for user in User.objects.all():
            if user.associated_student is not None and user not in club.leadership.all():
                listofusers.append(user)
    
    return listofusers