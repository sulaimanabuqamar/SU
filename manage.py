#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import staticServer
import threading

def start():
    print("STARTING")
    staticServer.startServer()
def stop():
    staticServer.stopServer()

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

    try:
        if 'runserver' in sys.argv:
            print("start")
            server_thread = threading.Thread(target=start)
            server_thread.daemon = True  # This ensures the thread will close when the main program exits
            server_thread.start()
    except Exception as e:
        print(e)
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
    stop()