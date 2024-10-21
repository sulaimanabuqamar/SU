from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_admin', 'is_staff',  'is_superuser')
    list_filter = ('is_admin', 'is_staff')
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
        (None, {'fields': ('year_level', 'section', 'profile_picture', 'about')}),
        # ('Memberships', {'fields': ('clubs', 'varsities')}),
    )
    search_fields = ('year_level', 'section')
    # filter_horizontal = ('clubs', 'varsities')
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_db_id',)
    list_filter = ('faculty_db_id',)
    fieldsets = (
        (None, {'fields': ('faculty_db_id',)}),
    )
    search_fields = ('faculty_db_id',)

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')  # Display name and email in the list view
    search_fields = ('name', )  # Allow searching by name and email
    filter_horizontal = ('heads', 'leadership', 'members', 'advisors', 'events')  # Use a horizontal filter for many-to-many fields

    fieldsets = (
        (None, {'fields': ('name', 'about', 'logo', 'color', 'links')}),
        ('Membership', {'fields': ('heads', 'leadership', 'members', 'advisors')}),
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

    )

class EventAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'published_date', 'summary', 'members_only', 'highlight', 'group', 'grade')
    list_filter = ('members_only', 'highlight')
    search_fields = ('summary',)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('author',  'title', 'summary','awaiting_approval', 'approved', 'group', 'grade', 'published_date')
    list_filter = ('highlight', 'group', 'grade')
    search_fields = ('summary',)
    fieldsets = (
        (None, {'fields': ('author', 'cover', 'title', 'text', 'summary', 'highlight', 'published_date', 'links')}),
        ('Visibility', {'fields': ('group', 'grade','approved','awaiting_approval','denied_reason')}), 
    )
    
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