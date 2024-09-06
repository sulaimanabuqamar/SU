from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.Home, name="home"),
    path("Events/", views.Events, name="events"),
    path("Event/Detail/<int:event_id>/", views.Event_Detail, name="event_detail"),
    path("Event/Remove/", views.removeAttendee, name="remove_attendee"),
    path("Event/Add/", views.addAttendee, name="add_attendee"),
    path("Event/Modify/<int:event_id>", views.ModifyEvent, name="modify_event"),
    path("News/", views.News_View, name="news"),
    path("News/Detail/<int:news_id>/", views.News_Detail, name="news_detail"),
    path("News/Modify/<int:news_id>", views.ModifyNews, name="modify_news"),
    path("Create/Event", views.CreateEvent, name="create_event"),
    path("Create/News", views.CreateNews, name="create_news"),
    path("Clubs/", views.Clubs, name="clubs"),
    path("Club/Detail/<int:club_id>/", views.Club_Detail, name="club_detail"),
    path("Club/Remove/<str:sector>/", views.removeClubMember, name="remove_club_member"),
    path("Club/Add/<str:sector>/", views.addClubMember, name="add_club_member"),
    path("Varsity/", views.Varsity_View, name="varsity"),
    path('Varsity/Detail/<int:varsity_id>/', views.Varsity_Detail, name='varsity_detail'),
    path("Varsity/Remove/<str:sector>", views.removeVarsityPlayer, name="remove_varsity_player"),
    path("Varsity/Add/<str:sector>", views.addVarsityPlayer, name="add_varsity_player"),
    path("Student/Detail/<str:student_id>/", views.Student_Detail, name="student_detail"),
    path("profile/", views.UserProfile, name="user_profile"),
    path("clublogin/", views.Club_Varsity_login, name="club_varisty_login"),
    path("singlelogin/", views.Student_Faculty_login, name="student_faculty_login"),
    path("singlelogout/", views.Student_Faculty_logout, name="student_faculty_logout"),
    path("finishSetup/Student/", views.Finish_Setup_Student, name="finish_setup_student"),
    path("AttendeesList/Printable/<int:event_id>/", views.AttendeesListPrintable, name="attendees_list_printable"), 
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 