from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.Home, name="home"),
    path("FAQs/", views.Faqs_View, name="faqs"),
    path("Events/", views.Events, name="events"),
    path("Event/Detail/<int:event_id>/", views.Event_Detail, name="event_detail"),
    path("Event/Remove/", views.removeAttendee, name="remove_attendee"),
    path("Event/Add/", views.addAttendee, name="add_attendee"),
    path("Event/Confirm/", views.setConfirmed, name="confirm_attendee"),
    path("Event/Unconfirm/", views.setUnconfirmed, name="unconfirm_attendee"),
    path("Event/Modify/<int:event_id>", views.ModifyEvent, name="modify_event"),
    path("Event/Lock/<int:event_id>", views.ToggleLockEvent, name="modify_event"),
    path("Event/Draft/<int:club_id>/<int:event_id>/", views.DraftEvent, name="draft_event"),
    path("Event/Delete/<int:event_id>/", views.DeleteEvent, name="delete_event"),
    path("News/", views.News_View, name="news"),
    path("News/Detail/<int:news_id>/", views.News_Detail, name="news_detail"),
    path("News/Modify/<int:news_id>", views.ModifyNews, name="modify_news"),
    path("News/Draft/<int:news_id>/", views.DraftNews, name="draft_news"),
    path("News/Delete/<int:news_id>/", views.DeleteNews, name="delete_news"),
    path("Create/Meeting/<int:club_id>", views.CreateMeeting, name="create_meeting"), 
    path("Create/Event/<int:club_id>", views.CreateEvent, name="create_event"), 
    path("Create/News", views.CreateNews, name="create_news"),
    path("Clubs/", views.Clubs, name="clubs"),
    path("Club/Detail/<int:club_id>/", views.Club_Detail, name="club_detail"),
    path("Club/Remove/<int:club_id>/<str:sector>/", views.removeClubMember, name="remove_club_member"),
    path("Club/Add/<int:club_id>/<str:sector>/", views.addClubMember, name="add_club_member"),
    path("Club/AddByLink/request/<int:club_id>/", views.requestAddMemberByLink, name="request_add_club_member_by_link"),
    path("Club/Join/<int:hash>/", views.addMemberByLink, name="add_club_member_by_link"),
    path("Club/SendEmails/<int:club_id>/", views.clubSendEmails, name="send_club_emails"),
    path("Club/Bylaws/<int:club_id>/", views.Club_Bylaws_Detail, name="club_bylaws"),
    path("Club/EditBylaws/view/<int:club_id>/", views.viewBylaw, name="club_edit_bylaws"),  
    path("Club/EditBylaws/edit/<int:bylaw_id>/<int:club_id>/", views.editBylaw, name="edit_bylaw"),
    path("Club/EditBylaws/create/<int:club_id>/", views.createBylaw, name="club_create_bylaw"), 
    path("Club/EditBylaws/delete/<int:club_id>/<int:bylaw_id>/", views.deleteBylaw, name="club_create_bylaw"),  
    path("Club/EditBylaws/json/<int:bylaw_id>/", views.jsonBylaw, name="bylaw_json"),  
    path("Club/EditBylaws/down/<int:club_id>/<int:bylaw_id>/", views.moveBylawDown, name="bylaw_down"),  
    path("Club/EditBylaws/up/<int:club_id>/<int:bylaw_id>/", views.moveBylawUp, name="bylaw_up"),  
    path("Bylaw/Resources/add/<int:bylaw_id>/<int:club_id>/", views.createResource, name="add_resource"),  
    path("Bylaw/Resources/delete/<int:resource_id>/", views.deleteResource, name="add_resource"),  
    path("Varsity/", views.Varsity_View, name="varsity"),
    path('Varsity/Detail/<int:varsity_id>/', views.Varsity_Detail, name='varsity_detail'),
    path("Varsity/Remove/<int:varsity_id>/<str:sector>", views.removeVarsityPlayer, name="remove_varsity_player"),
    path("Varsity/Add/<int:varsity_id>/<str:sector>", views.addVarsityPlayer, name="add_varsity_player"),
    path("Student/Detail/<str:student_id>/", views.Student_Detail, name="student_detail"),
    path("Faculty/Detail/<str:faculty_id>/", views.Faculty_Detail, name="faculty_detail"),
    path("Scouts/", views.Scouts_View, name="scouts"),
    path("Scouts/Detail/<int:scouts_id>/", views.Scouts_Detail, name="scouts_detail"),
    path("Meetings/", views.Meetings, name="meetings"),
    path('Meetings/Detail/<int:meeting_id>/', views.Meeting_Details, name='meeting_detail'),
    path("Meetings/Modify/<int:meeting_id>", views.ModifyMeeting, name="modify_meeting"),
    path("Meetings/Remove/", views.removeAttendeeMeeting, name="remove_attendee_meeting"),
    path("Meetings/Add/", views.addAttendeeMeeting, name="add_attendee_meeting"),
    path("Meetings/Draft/<int:club_id>/<int:meeting_id>/", views.DraftMeeting, name="draft_meeting"),
    path("Meetings/Delete/<int:meeting_id>/", views.DeleteMeeting, name="delete_meeting"),
    path("profile/User", views.UserProfile, name="user_profile"),
    path("profile/Club/<int:club_id>", views.ClubProfile, name="user_profile"),
    path("profile/Varsity/<int:varsity_id>", views.VarsityProfile, name="user_profile"),
    path("profile/Edit/", views.editProfile, name="edit_user_profile"),
    path("profile/Edit/Club/<int:club_id>", views.editClub, name="edit_club_profile"),
    path("profile/Edit/Varsity/<int:varsity_id>", views.editVarsity, name="edit_varsity_profile"), 
    path("clublogin/", views.Club_Varsity_login, name="club_varisty_login"),
    path("singlelogin/", views.Student_Faculty_login, name="student_faculty_login"),
    path("singlelogout/", views.Student_Faculty_logout, name="student_faculty_logout"),
    path("finishSetup/Student/", views.Finish_Setup_Student, name="finish_setup_student"),
    path("AttendeesList/Printable/<str:type>/<int:id>/", views.AttendeesListPrintable, name="attendees_list_printable"), 
    path("AttendeesList/Permissions/<str:type>/<int:id>/", views.MeetingAttendeePermissionSlips, name="attendees_permission_slips"), 
    path("SystemUpdate/Update/", views.ActivateSystemUpdate, name="activate_system_update"),
    path("SystemUpdate/Prepare/", views.PrepareSystemUpdate, name="prepare_system_update"),
    path("Upload/Media/About", views.uploadImage, name="upload_image_about"), 
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 