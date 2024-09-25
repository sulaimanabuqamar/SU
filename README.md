## Important
Make sure that the port 81 is also able to be run on su.amb.sch.ae, this server is important to allow the main server to get static and media files
# Switching from Debug enabled to disabled
1. In `settings.py` change `Debug` to `False`
2. In `settings.py` comment out `STATIC_URL = "http://localhost:81/static/"`
And uncomment `# STATIC_URL = "https://su.amb.sch.ae:81/static/"`
3. In `settings.py` comment out `MEDIA_URL = 'http://localhost:81/media/'`
And uncomment `# MEDIA_URL = 'https://su.amb.sch.ae:81/media/'`
## To switch back to Debug enabled do the opposite for the steps above