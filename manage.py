#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import staticServer

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studentsunion.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if 'runserver' in sys.argv:
    print("Static Media Server Initializing...")
    thread = threading.Thread(target=staticServer.startServer)
    print("Second Thread Starting...")
    thread.start()
    print("Starting Django Server...")
if __name__ == "__main__":
    main()
    if 'runserver' in sys.argv:
        print("Django Shutdown\nShutting Down Static Media Server...")
        staticServer.stopServer()
        print("Aborting Second Thread...")
        thread.join()
        print("Exit")