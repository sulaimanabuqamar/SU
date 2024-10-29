from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_admin', 'associated_student',  'is_superuser') 
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser')}),
        ('Account Type', {'fields': ('associated_student', 'associated_faculty', 'associated_clubs', 'associated_varsities')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ()

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_db_id', 'year_level', 'section')
    list_filter = ('year_level', 'section')
    fieldsets = (
        (None, {'fields': ('student_db_id',)}),
        (None, {'fields': ('year_level', 'section', 'profile_picture', 'about', 'year_level_title', 'gender')}),
        # ('Memberships', {'fields': ('clubs', 'varsities')}),
    )
    search_fields = ('year_level', 'section', 'student_db_id')
    # filter_horizontal = ('clubs', 'varsities')
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_db_id', 'profile_picture')
    list_filter = ('faculty_db_id',)
    fieldsets = (
        (None, {'fields': ('faculty_db_id', 'profile_picture')}), 
    )
    search_fields = ('faculty_db_id',)

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')  # Display name and email in the list view
    search_fields = ('name', )  # Allow searching by name and email
    filter_horizontal = ('heads', 'leadership', 'members', 'advisors', 'events')  # Use a horizontal filter for many-to-many fields

    fieldsets = (
        (None, {'fields': ('name', 'about', 'logo', 'color', 'links', 'type')}),
        ('Membership', {'fields': ('heads', 'leadership', 'members', 'advisors')}),
        ('Events', {'fields': ('events', )}),
    )

class VarsityAdmin(admin.ModelAdmin):
    list_display = ('name', 'about')  # Display name and email in the list view
    search_fields = ('name', 'about')  # Allow searching by name and email
    filter_horizontal = ('captains', 'members', 'coaches')  # Use a horizontal filter for many-to-many fields

    fieldsets = (
        (None, {'fields': ('name', 'about', 'logo', 'color', 'links')}),
        ('Captains', {'fields': ('captains',)}),
        ('Players', {'fields': ('members',)}), 
        ('Coaches', {'fields': ('coaches',)}),
        ('Events (DO NOT USE)', {'fields': ('events',)}),

    )

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'summary', 'members_only', 'highlight', 'group', 'grade', 'draft')
    list_filter = ('members_only', 'highlight')
    search_fields = ('summary',)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pk', 'published_date','date','start_time','end_time', 'draft')
    search_fields = ('summary','title', 'text') 

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title',  'author', 'summary','awaiting_approval', 'approved', 'group', 'grade', 'published_date', 'draft')
    list_filter = ('highlight', 'group', 'grade')
    search_fields = ('summary',)
    
class HomepageAdmin(admin.ModelAdmin):
    fields = ['event_highlight_1', 'event_highlight_2', 'event_highlight_3', 'news_highlight_1', 'news_highlight_2', 'news_highlight_3', 'officer_highlight_1', 'officer_highlight_2', 'officer_highlight_3', 'officer_highlight_4','carousel_scroll_duration']
class LinksAdmin(admin.ModelAdmin):
    list_display = ('name',  'link')
    list_filter = ('name', 'link')
    search_fields = ('name','link')
    
# Register your models here
admin.site.register(HomePage, HomepageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Varsity, VarsityAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Links, LinksAdmin) 
admin.site.register(News, NewsAdmin)
admin.site.register(Meeting, MeetingAdmin)