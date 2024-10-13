
from typing import Iterable
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core import exceptions
from django.core.mail import send_mail
# Custom user model manager for Students and Faculty

class Links(models.Model):
    name = models.CharField(max_length=10000)
    link = models.URLField()
    def __str__(self) -> str:
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    associated_student = models.ForeignKey("Student",null=True, blank=True, on_delete=models.CASCADE)
    associated_faculty = models.ForeignKey("Faculty",null=True, blank=True, on_delete=models.CASCADE)
    associated_clubs = models.ManyToManyField("Club", blank=True,related_name="associated_clubs")
    associated_varsities = models.ManyToManyField("Varsity", blank=True,related_name="associated_varsity")
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    student_db_id = models.CharField(max_length=20, primary_key=True,help_text="Student ID")
    YEAR_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    ]
    SECTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
    ]
    year_level = models.IntegerField(blank=True, null=True)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    # clubs = models.ManyToManyField('Club', related_name='students', blank=True)
    # varsities = models.ManyToManyField('Varsity', related_name='students', blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True, default='default-pfp.png')
    about = models.TextField(blank=True,null=True)
    year_level_title = models.CharField(max_length=10, blank=True)
    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)
        print(self.year_level)
        # print(type(self.year_level))
        if int(self.year_level) == 9:
            self.year_level_title = "Freshman"
        elif int(self.year_level) == 10:
            self.year_level_title = "Sophomore"
        elif int(self.year_level) == 11:
            self.year_level_title = "Junior"
        elif int(self.year_level) == 12:
            self.year_level_title = "Senior"
        else:
            print("error not hs")
            self.year_level_title = "Underage" 
        print(self.year_level_title)
        
        return super().save(*args, **kwargs)
class Faculty(models.Model):
    faculty_db_id = models.CharField(max_length=20, primary_key=True,help_text="Faculty ID")
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True, default='default-pfp.png')

class Club(models.Model):
    name = models.CharField(max_length=255)
    heads = models.ManyToManyField(User, related_name='head_clubs', blank=True)
    leadership = models.ManyToManyField(User, related_name='leadership_roles', blank=True)
    members = models.ManyToManyField(User, related_name='membership_clubs', blank=True)
    advisors = models.ManyToManyField(User, related_name='advisor_clubs', blank=True)
    events = models.ManyToManyField('Event', related_name='events', blank=True)
    about = models.TextField()
    logo = models.ImageField(upload_to='clubs_logos/')
    color = models.CharField(max_length=7)  # Hex color code
    links = models.ManyToManyField(Links, related_name='club_links', blank=True)
    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    GROUP_CHOICES = [
        ('ngr', 'All Year Levels'),
        ('12', 'Senior'),
        ('11', 'Junior'),
        ('10', 'Sophomore'),
        ('9', 'Freshman'),
    ]
    GRADE_CHOICES = [
        ('nosec', 'All Sections'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
    ]
    author = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='authored_events')
    cover = models.ImageField(upload_to='event_covers/', blank=True, null=True)  # Remove default and allow blank/null
    title = models.CharField(max_length=100)
    text = models.TextField()
    summary = models.CharField(max_length=150)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    published_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=150, blank=True)
    color = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='club_color', blank=True, null=True)
    group = models.CharField(max_length=3, choices=GROUP_CHOICES,default="ngr")
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES,default="nosec")
    members_only = models.BooleanField(default=False)
    highlight = models.BooleanField(default=False)
    significant_event = models.BooleanField(default=False)
    attending_Students = models.ManyToManyField(User, related_name='attending_students', blank=True)
    confirmed_Students = models.ManyToManyField(User, related_name='confirm_students', blank=True)
    links = models.ManyToManyField(Links, related_name='events_links', blank=True)
    def __str__(self) -> str:
        return self.title
    typeitem = "event"
    def save(self, *args, **kwargs):
        if not self.cover:  # Check if cover is not provided
            if self.author and self.author.logo:  # Ensure the author and their logo exist
                self.cover = self.author.logo  # Set the default cover to the author's logo
        super().save(*args, **kwargs)  # Call the super class's save method
        
class News(models.Model):
    GROUP_CHOICES = [
        ('ngr', 'All Year Levels'),
        ('12', 'Senior'),
        ('11', 'Junior'),
        ('10', 'Sophomore'),
        ('9', 'Freshman'),
    ]
    GRADE_CHOICES = [
        ('nosec', 'All Sections'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='news_covers/')
    title =  models.CharField(max_length=100)
    text = models.TextField()
    published_date = models.DateTimeField(null=True, blank=True)
    summary = models.CharField(max_length=150)
    group = models.CharField(max_length=3, choices=GROUP_CHOICES,default="ngr")
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES,default="nosec")
    highlight = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    awaiting_approval = models.BooleanField(default=True)
    denied_reason = models.CharField(max_length=150, blank=True, null=True)
    links = models.ManyToManyField(Links, related_name='news_links', blank=True)
    typeitem = "news"
    def __str__(self):
        return self.title

class Varsity(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='varsity_players', blank=True)
    captains = models.ManyToManyField(User, related_name='varsity_captains', blank=True)
    coaches = models.ManyToManyField(User, related_name='varsity_coaches', blank=True)
    events = models.ForeignKey('Event', on_delete=models.CASCADE, blank=True, null=True)
    about = models.TextField()
    logo = models.ImageField(upload_to='varsities_logos/')
    color = models.CharField(max_length=7)  # Hex color code
    links = models.ManyToManyField(Links, related_name='varsity_links', blank=True)
    def __str__(self) -> str:
        return self.name
class HomePage(models.Model):
    event_highlight_1 = models.ForeignKey(Event, related_name='home_event_highlight_1', on_delete=models.CASCADE, null=True, blank=True)
    event_highlight_2 = models.ForeignKey(Event, related_name='home_event_highlight_2', on_delete=models.CASCADE, null=True, blank=True)
    event_highlight_3 = models.ForeignKey(Event, related_name='home_event_highlight_3', on_delete=models.CASCADE, null=True, blank=True)
    news_highlight_1 = models.ForeignKey(News, related_name='home_news_highlight_1', on_delete=models.CASCADE, null=True, blank=True)
    news_highlight_2 = models.ForeignKey(News, related_name='home_news_highlight_2', on_delete=models.CASCADE, null=True, blank=True)
    news_highlight_3 = models.ForeignKey(News, related_name='home_news_highlight_3', on_delete=models.CASCADE, null=True, blank=True)
    officer_highlight_1 = models.ForeignKey(User, related_name='home_officer_highlight_1', on_delete=models.CASCADE, null=True, blank=True)
    officer_highlight_2 = models.ForeignKey(User, related_name='home_officer_highlight_2', on_delete=models.CASCADE, null=True, blank=True)
    officer_highlight_3 = models.ForeignKey(User, related_name='home_officer_highlight_3', on_delete=models.CASCADE, null=True, blank=True)
    officer_highlight_4 = models.ForeignKey(User, related_name='home_officer_highlight_4', on_delete=models.CASCADE, null=True, blank=True)
    carousel_scroll_duration = models.IntegerField(default=2000, help_text="Time Before Carousel Autoscrolls (ms)")
    