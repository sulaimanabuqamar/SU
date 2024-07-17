from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.Home, name="home"),
    path("Events/", views.Events, name="events"),
    path("Event/Detail/<int:event_id>/", views.Event_Detail, name="event_detail"),
    path("News/", views.News_View, name="news"),
    path("News/Detail/<int:news_id>/", views.News_Detail, name="news_detail"),
    path("Clubs/", views.Clubs, name="clubs"),
    path("Club/Detail/<int:club_id>/", views.Club_Detail, name="club_detail"),
    path("Varsity/", views.Varsity_View, name="varsity"),
    path('Varsity/Detail/<int:varsity_id>/', views.Varsity_Detail, name='varsity_detail'),
    path("Student/Detail/<int:student_id>/", views.Student_Detail, name="student_detail"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)