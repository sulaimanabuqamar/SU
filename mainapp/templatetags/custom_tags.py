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
def getUserAttendingMeeting(email, meeting_id):
    # return datetime.datetime.now().strftime(format_string)
    meeting = Meeting.objects.get(id=meeting_id)
    if User.objects.get(email=email) in meeting.attending_Members.all():
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


@register.simple_tag
def student_grade_display(obj):
    """Return a compact display for a student's year/graduate state.

    Accepts either a User (with associated_student) or a Student instance.
    - If the student is an alumni and has graduation_year, returns the last two digits
      of the graduation end year (e.g. '25').
    - If the student is alumni but no graduation_year, returns 'Graduated'.
    - Otherwise returns the year_level+section (e.g. '11A').
    """
    # tolerate being passed User or Student
    student = None
    try:
        # User-like
        if hasattr(obj, 'associated_student') and obj.associated_student is not None:
            student = obj.associated_student
        else:
            student = obj
    except Exception:
        student = obj

    if student is None:
        return ""

    try:
        if getattr(student, 'is_alumni', False):
            gy = getattr(student, 'graduation_year', None)
            if gy:
                try:
                    end = gy.split('-')[1]
                    return "'" + end[-2:]
                except Exception:
                    return 'Graduated'
            return 'Graduated'
        else:
            y = getattr(student, 'year_level', '')
            s = getattr(student, 'section', '') or ''
            return f"{y}{s}"
    except Exception:
        return ""