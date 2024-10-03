## Important
Make sure that the port 81 is also able to be run on ss.amb.sch.ae, this server is important to allow the main server to get static and media files.

Make sure that the server is currently set to the `data` branch. Make sure to run `git checkout data` to switch to the `data` branch.
This makes sure that the server can automatically update.
# Switching from Debug enabled to disabled
1. In `settings.py` change `Debug` to `False`
2. In `settings.py` comment out `STATIC_URL = "http://localhost:81/static/"`
And uncomment `# STATIC_URL = "https://ss.amb.sch.ae:81/static/"`
3. In `settings.py` comment out `MEDIA_URL = 'http://localhost:81/media/'`
And uncomment `# MEDIA_URL = 'https://ss.amb.sch.ae:81/media/'`
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

# Declaring accounts as Admin (When assigning relevant people and SS officers)
To declare a user as an admin for any reason, you must set the following to true:
- `is_staff`
- `is_admin`
- `is_superuser`

If you did things correctly, your main profile (student/faculty) page will show a new button that reads "Admin Page", pressing on this button redirects to the admin page where you can modify any part of the site. 

> If you need to give someone access to only specific portions of the site, create a group in the admin page and assign the relevant permissions and add the user(s) to it

> Make sure that the chosen SS officers are prepared to handle issues with the server, see below for common issues

# Approving and Denying News Posts
## Approving Posts
To approve a post, go into the admin portal and find the post and open it, Uncheck the box that says Awaiting Approval and check the Approved box and save. It should now be live.
## Denying Posts
To deny a post, go into the admin portal and find the post and open it, Uncheck the Awaiting Approval, make sure the Approved box is unchecked and optionally specify the reason for taking down the post in the denied reason box and then press save. 

# Adding Links (When supported)
In the text box you can add your links in this format: [Display Text]![URL]

Example: Putting `Google!https://google.com` in the box will result in a link similar to this one: [Google](https://google.com)

You can add multiple links by separating them into new lines. 

Example: 
```
AMIC Member Applications!https://docs.google.com/forms
AMIC Website!https://amic.amb.sch.ae
```
Result: [AMIC Member Applications](https://docs.google.com/forms), [AMIC Website](https://amic.amb.sch.ae)

# Updating The Server Post Production
To Update the server, follow these steps:
1. Go to the profile page and press on the **prepare** system update button
2. Then on your code, pull the code from the `data` branch and make your changes
3. Push your changes to the `prod` branch
4. Go to the profile page and press on the **perform** system update button and it should automatically update and finish

#  Common Issues and their solutions
## 1. "I Can't Access my profile page!" or "There is nothing in my profile page!"
Check if the user has any associated clubs/varsities/student/faculty to their account, if there is none do this:
1. Tell them to logout and log back in, the site should automatically ask the user to associated their student id with their account, if not manually create/find the student object and attach it to the associated_student field.
2. If they are complaining about this issue in regards to a club or varsity, check if they have the respective club/varsity in their associated_clubs/varsities field and add it, if there is already one or more selected, cmd/ctrl click the new one to add it to the list and press save.

## 2. "The site says 500 in big letters and it said to contact an SS Officer"
When someone contacts you about the 500 page, it means that they have experienced an _Internal Server Error_ meaning that the user did something in the site that caused the server to abort the request and crash, there is more information that the user should send to you, if they haven't ask them to open the exception details expandable and to send you the contents of the gray box, here are common 500 errors and solutions:
1. **Any error related to** `AnonymousUser`: The user probably tried to access part of the site that requires you to be logged in but they are not logged in, if they _are_ logged in then that means that they have no associated accounts attached to their account, **see the common issue  #1 for help**
2. `x is Not Found`: This error occurs when the user tries to access an event/club/varsity/news/scouts that may have been deleted, ask the user to double check the link (if they were sent the link to it) or to make sure that it hasn't been deleted by an SS Officer or admin.
3. `UNIQUE Constraint failed` **error**: this error might occur when the user is trying to create an event/news if it happens notify one of the admins or anyone who created the site with the exception info to help repair the issue. If this issue happens when they are trying to sign in, check if they have an associated_student/faculty attached to their account, if they do and they are still getting this error, first detach the student object from the user account, then delete the student object, then ask the user to try to login again and they should get a popup asking them to fill in their details again.
4. **Any other issues**: If the error is clear enough and you think you know how to solve the issue, feel free to attempt but keep in mind not to delete anything, if you don't feel comfortable to attempt repair yourself or you don't know the reason for the error, pass the exception data on to an admin or developer of the SS website.
## 3. "The site says 404 in big letters and it said to contact an SS Officer"
This issue simply means the page they tried to visit does not exist on the site, ask them to double check the url or link if they were sent one. 
## 4. "I just created my news post and I can't see it on the news page"
Check if the news post is still pending approval or denied and inform the user about their news status, if it is already approved, make sure that section/grade filter is not active/or set to the correct target demographic and inform the user.

# GitHub Branches, Pushing Code, and More (ADMINS/DEVS ONLY)
## Branches and Their Uses
The GitHub repo has 3 branches: `main`, `prod`, and `data`. The `main` branch is used for the pre-release code, this code should usually be the most unstable and only used when a bug fix is being worked on for the main site or a new feature, etc. The `prod` branch is used for the production ready code, this is the code that is gonna go on the production server, it is usually the most stable and error free and should not be edited on. This is also the branch that the server will the system update from. The `data` branch is used only for the live server, this branch is where the server dumps its version of the code for bugfixes or whenever you have a new feature you want to work on, its used get the current save data from the server as it is.

## Pushing Code
The first thing you must do is prepare for a system update by pressing the prepare for system update button in the profile page, it will dump the server code on the `data` branch which then you pull and merge to the `main` branch to start working on the bug fix, if you took a long time to implement the feature/fix, do the prepare for system update process again and merge with `main` to sync then push your changes to `prod` once its ready, bug-checked and ready for production. Once the push is complete, go to the profile page and press on the perform system update button to start updating, the server will pull the latest code from the `prod` branch and automatically reboot to apply. 

## Pushing Code To The Live Server
If you are tasked with pushing the code to the server for the first time but you don't know which branch you must pull from, pull from the `prod` branch then use the command `git checkout data` to switch to the `data` branch to be able to receive updates. 