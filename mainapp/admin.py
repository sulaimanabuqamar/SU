from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Club, Event, News, Varsity, HomePage

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_admin', 'is_staff')
    list_filter = ('is_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),
        ('Account Type', {'fields': ('associated_student', 'associated_faculty', 'associated_club', 'associated_varsity')}),
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
        (None, {'fields': ('year_level', 'section', 'profile_picture')}),
        ('Memberships', {'fields': ('clubs', 'varsities')}),
    )
    search_fields = ('year_level', 'section')
    filter_horizontal = ('clubs', 'varsities')

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')  # Display name and email in the list view
    search_fields = ('name', 'email')  # Allow searching by name and email
    filter_horizontal = ('heads', 'leadership', 'members', 'events')  # Use a horizontal filter for many-to-many fields

    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'about', 'logo', 'color')}),
        ('Membership', {'fields': ('heads', 'leadership', 'members')}),
        ('Events', {'fields': ('events',)}),
    )

class VarsityAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')  # Display name and email in the list view
    search_fields = ('name', 'email')  # Allow searching by name and email
    filter_horizontal = ('members',)  # Use a horizontal filter for many-to-many fields

    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'about', 'logo', 'color')}),
        ('Players', {'fields': ('members',)}),
    )

class EventAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'text', 'summary', 'members_only', 'highlight')
    list_filter = ('members_only', 'highlight')
    search_fields = ('summary',)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('author',  'title', 'text', 'summary', 'highlight', 'group', 'grade', 'published_date')
    list_filter = ('highlight', 'group', 'grade')
    search_fields = ('summary',)
    fieldsets = (
        (None, {'fields': ('author', 'cover', 'title', 'text', 'summary', 'highlight', 'published_date')}),
        ('Visibility', {'fields': ('group', 'grade')}),
    )
    
class HomepageAdmin(admin.ModelAdmin):
    fields = ['event_highlight_1', 'event_highlight_2', 'event_highlight_3', 'news_highlight_1', 'news_highlight_2', 'news_highlight_3', 'officer_highlight_1', 'officer_highlight_2', 'officer_highlight_3', 'officer_highlight_4']

# Register your models here
admin.site.register(HomePage, HomepageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Varsity, VarsityAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(News, NewsAdmin)
