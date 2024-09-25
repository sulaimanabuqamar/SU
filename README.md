## Important
Make sure that the port 81 is also able to be run on su.amb.sch.ae, this server is important to allow the main server to get static and media files
# Switching from Debug enabled to disabled
1. In `settings.py` change `Debug` to `False`
2. In `settings.py` comment out `STATIC_URL = "http://localhost:81/static/"`
And uncomment `# STATIC_URL = "https://su.amb.sch.ae:81/static/"`
3. In `settings.py` comment out `MEDIA_URL = 'http://localhost:81/media/'`
And uncomment `# MEDIA_URL = 'https://su.amb.sch.ae:81/media/'`
## To switch back to Debug enabled do the opposite for the steps above

# Creating Clubs/Varsities/Scouts
## Creating Clubs
- Complete all the information fields such as the name, about, logo, color, and links (optional)
- You can optionally also add the students/faculty to your club at creation time but it is recommended to be done from the normal site instead of the admin page

> IMPORTANT: Make sure that you add the club to the appropriate users' associated_clubs field to ensure that they have access to modify the club

> Avoid writing the word `Scouts` in your club description to prevent it from being classified as scouts, if you want to mention scouts in your about text, keep it all lower case (`scouts`) to avoid being incorrectly classified as scouts.
## Creating Varsities
The process for creating varsities is the same as clubs, except use the dedicated varsities section for this task, also the scouts classification does not apply here so if needed you can capitalize the word `Scouts`
## Creating Scouts
To create a scouts, you must create a new club like normal but you MUST add the word `Scouts` (capitalization matters!) anywhere in the about section, you can disguise it in the about text, Example: `The x Scouts consists of our Senior Members aswell as our Juniors`

# Declaring accounts as Admin (When assigning relevant people and SU officers)
To declare a user as an admin for any reason, you must set the following to true:
- `is_staff`
- `is_admin`
- `is_superuser`

If you did things correctly, your main profile (student/faculty) page will show a new button that reads "Admin Page", pressing on this button redirects to the admin page where you can modify any part of the site. 

> If you need to give someone access to only specific portions of the site, create a group in the admin page and assign the relevant permissions and add the user(s) to it

> Make sure that the chosen SU officers are prepared to handle issues with the server, see below for common issues

#  Common Issues and their solutions
## 1. "I Can't Access my profile page!" or "There is nothing in my profile page!"
Check if the user has any associated clubs/varsities/student/faculty to their account, if there is none do this:
1. Tell them to logout and log back in, the site should automatically ask the user to associated their student id with their account, if not manually create/find the student object and attach it to the associated_student field.
2. If they are complaining about this issue in regards to a club or varsity, check if they have the respective club/varsity in their associated_clubs/varsities field and add it, if there is already one or more selected, cmd/ctrl click the new one to add it to the list and press save.

## 2. "The site says 500 in big letters and 