from django.contrib import admin
from .views import bulk_grade_update_logic

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django.db.models.query  import QuerySet

def cleanup_corrupted_m2m_data():
    """
    Remove non-User objects from ALL User M2M fields across all models.
    This comprehensively cleans corrupted data where Student objects were
    accidentally stored in fields that should only contain User objects.
    """
    cleaned_count = 0
    errors = []
    
    # List of all (model_class, field_name) tuples that should only contain User instances
    user_m2m_fields = [
        (PLC, 'attended_Students'),
        (Club, 'heads'),
        (Club, 'leadership'),
        (Club, 'members'),
        (Club, 'advisors'),
        (Event, 'attending_Students'),
        (Event, 'confirmed_Students'),
        (Meeting, 'attending_Members'),
        (Varsity, 'members'),
        (Varsity, 'captains'),
        (Varsity, 'coaches'),
    ]
    
    # Also handle reverse relations from User
    user_reverse_m2m_fields = [
        (User, 'associated_clubs'),
        (User, 'associated_varsities'),
    ]
    
    # Process direct M2M fields
    for model_class, field_name in user_m2m_fields:
        try:
            for obj in model_class.objects.all():
                try:
                    m2m_manager = getattr(obj, field_name)
                    if m2m_manager is None:
                        continue
                    
                    # Get all items in the M2M field
                    try:
                        items = list(m2m_manager.all())
                    except Exception as e:
                        errors.append(f"Error reading {model_class.__name__}.{field_name}: {str(e)}")
                        continue
                    
                    # Remove any non-User items
                    for item in items:
                        try:
                            if not isinstance(item, User):
                                try:
                                    m2m_manager.remove(item)
                                    cleaned_count += 1
                                except Exception as e:
                                    errors.append(f"Error removing from {model_class.__name__}.{field_name}: {str(e)}")
                        except Exception as e:
                            errors.append(f"Error checking item in {model_class.__name__}.{field_name}: {str(e)}")
                            
                except Exception as e:
                    errors.append(f"Error processing {model_class.__name__}.{field_name}: {str(e)}")
        except Exception as e:
            errors.append(f"Error iterating {model_class.__name__}: {str(e)}")
    
    # Process reverse M2M fields
    for model_class, field_name in user_reverse_m2m_fields:
        try:
            for obj in model_class.objects.all():
                try:
                    m2m_manager = getattr(obj, field_name)
                    if m2m_manager is None:
                        continue
                    
                    # Get all items in the M2M field
                    try:
                        items = list(m2m_manager.all())
                    except Exception as e:
                        errors.append(f"Error reading {model_class.__name__}.{field_name}: {str(e)}")
                        continue
                    
                    # Remove any non-User items (for associated_clubs/varsities this should remove non-Club/non-Varsity)
                    for item in items:
                        try:
                            if field_name == 'associated_clubs' and not isinstance(item, Club):
                                try:
                                    m2m_manager.remove(item)
                                    cleaned_count += 1
                                except Exception as e:
                                    errors.append(f"Error removing from {model_class.__name__}.{field_name}: {str(e)}")
                            elif field_name == 'associated_varsities' and not isinstance(item, Varsity):
                                try:
                                    m2m_manager.remove(item)
                                    cleaned_count += 1
                                except Exception as e:
                                    errors.append(f"Error removing from {model_class.__name__}.{field_name}: {str(e)}")
                        except Exception as e:
                            errors.append(f"Error checking item in {model_class.__name__}.{field_name}: {str(e)}")
                            
                except Exception as e:
                    errors.append(f"Error processing {model_class.__name__}.{field_name}: {str(e)}")
        except Exception as e:
            errors.append(f"Error iterating {model_class.__name__}: {str(e)}")
    
    return cleaned_count, errors

def cleanup_action(modeladmin, request, queryset):
    """Admin action to clean up corrupted M2M data"""
    cleaned, errors = cleanup_corrupted_m2m_data()
    message = f"Cleaned up {cleaned} corrupted M2M records."
    if errors:
        message += f" ({len(errors)} errors occurred, check logs)"
    modeladmin.message_user(request, message)

cleanup_action.short_description = "Clean up corrupted data (remove Student objects from User fields)"

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_admin', 'associated_student', 'associated_faculty', 'is_superuser') 
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

from .views import get_academic_year_for_date

def archive_graduates_action(modeladmin, request, queryset):
    """Admin action: increment selected students' year_level; if they graduate, mark alumni and set graduation_year."""
    updated = 0
    archived = 0
    acad_year = get_academic_year_for_date()
    for student in queryset:
        try:
            if student.year_level is not None:
                student.year_level += 1
                if student.year_level > 12:
                    if not student.is_alumni:
                        student.is_alumni = True
                        if not student.graduation_year:
                            student.graduation_year = acad_year
                        archived += 1
                        # Archive news authored by user (if any)
                        try:
                            user_obj = User.objects.get(associated_student=student)
                        except Exception:
                            user_obj = None
                        if user_obj:
                            try:
                                for n in News.objects.filter(author=user_obj, archived_year__isnull=True):
                                    n.archived_year = student.graduation_year
                                    n.save()
                            except Exception:
                                pass
                            try:
                                # Archive events where the student attended or was confirmed
                                e_qs = Event.objects.filter(attending_Students=user_obj, archived_year__isnull=True) | Event.objects.filter(confirmed_Students=user_obj, archived_year__isnull=True)
                                for e in e_qs.distinct():
                                    if not e.archived_year:
                                        e.archived_year = student.graduation_year
                                        e.save()
                            except Exception:
                                pass
            try:
                student.save()
            except Exception:
                pass
            updated += 1
        except Exception:
            pass
    modeladmin.message_user(request, f"Updated {updated} students, archived {archived} graduates.")

archive_graduates_action.short_description = "Increment grade and archive graduates"

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_db_id', 'year_level_title', 'year_level', 'section', 'gender', 'profile_picture')
    list_filter = ('year_level', 'section', 'gender')
    fieldsets = (
        (None, {'fields': ('student_db_id',)}),
        (None, {'fields': ('year_level', 'section', 'profile_picture', 'about', 'year_level_title', 'gender')}),
        # ('Memberships', {'fields': ('clubs', 'varsities')}),
    )
    search_fields = ('year_level', 'section', 'student_db_id')
    # filter_horizontal = ('clubs', 'varsities')
    actions = [archive_graduates_action, cleanup_action]

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_db_id', 'profile_picture')
    list_filter = ('faculty_db_id',)
    fieldsets = (
        (None, {'fields': ('faculty_db_id', 'profile_picture')}), 
    )
    search_fields = ('faculty_db_id',)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name','type', 'pk')  # Display name and email in the list view
    search_fields = ('name', )  # Allow searching by name and email
    filter_horizontal = ('heads', 'leadership', 'members', 'advisors', 'events')  # Use a horizontal filter for many-to-many fields

    fieldsets = (
        (None, {'fields': ('name', 'about', 'logo', 'color', 'links', 'type')}),
        ('Membership', {'fields': ('heads', 'leadership', 'members', 'advisors')}),
        ('Events', {'fields': ('bylaws', 'events')}), 
    )
    def get_queryset(self, request):
        clubs = []
        for club in self.model.objects.all():
            if "Scouts" not in club.about:
                clubs.append(club.pk)
        return Club.objects.filter(pk__in=clubs)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'advisors':  # Replace with your field name
            kwargs['queryset'] = User.objects.filter(associated_faculty__isnull=False)
        if db_field.name == 'members':  # Replace with your field name
            kwargs['queryset'] = User.objects.filter(associated_student__isnull=False)
        if db_field.name == 'leadership':  # Replace with your field name
            kwargs['queryset'] = User.objects.filter(associated_student__isnull=False)
        if db_field.name == 'heads':  # Replace with your field name
            kwargs['queryset'] = User.objects.filter(associated_student__isnull=False)
        
        return super().formfield_for_manytomany(db_field, request, **kwargs)
class Scout(Club):
    class Meta:
        proxy = True
class ScoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')  # Display name and email in the list view
    search_fields = ('name', )  # Allow searching by name and email
    filter_horizontal = ('heads', 'leadership', 'members', 'advisors', 'events')  # Use a horizontal filter for many-to-many fields

    fieldsets = (
        (None, {'fields': ('name', 'about', 'logo', 'color', 'links', 'type')}),
        ('Membership', {'fields': ('heads', 'leadership', 'members', 'advisors')}),
        ('Events', {'fields': ('events', )}),
    )
    def get_queryset(self, request):
        scouts = []
        for club in self.model.objects.all():
            if "Scouts" in club.about:
                scouts.append(club.pk)
        return Club.objects.filter(pk__in=scouts)
    

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
    list_display = ('title', 'author', 'published_date', 'summary', 'members_only', 'highlight', 'group', 'grade', 'draft', 'hos_approved')
    list_filter = ('members_only', 'highlight')
    search_fields = ('summary',)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pk', 'published_date','date','start_time','end_time', 'draft', 'hos_approved')
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
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',  'type', 'pk')
    list_filter = ('type',)
    search_fields = ('question','answer', 'type')

class ResourcesAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'link', 'file')
    list_filter = ('name', 'link')
    search_fields = ('name','link')
class BylawsAdmin(admin.ModelAdmin):
    list_display = ('title', 'pk')
    list_filter = ('title',)
    search_fields = ('title',)

class AddByLinkAdmin(admin.ModelAdmin):
    list_display = ('club', 'pk')
    list_filter = ('club',)
    search_fields = ('club',)

class PLCAdmin(admin.ModelAdmin):
    list_display = ('pk','facilitator', 'recorder', 'timekeeper')
class PLCTopicAdmin(admin.ModelAdmin):
    list_display = ('pk','author', 'topic')
class PLCActionAdmin(admin.ModelAdmin):
    list_display = ('pk','author', 'action')


# Register your models here
admin.site.register(HomePage, HomepageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Scout, ScoutAdmin)
admin.site.register(Varsity, VarsityAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Links, LinksAdmin) 
admin.site.register(News, NewsAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Resource, ResourcesAdmin)
admin.site.register(Bylaw, BylawsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(AddByLink, AddByLinkAdmin) 
admin.site.register(PLC, PLCAdmin) 
admin.site.register(PLCTopic, PLCTopicAdmin) 
admin.site.register(PLCAction, PLCActionAdmin)