#!/usr/bin/env python
import os
import sys

from environ import environ

if __name__ == "__main__":
    env = environ.Env()
    try:
        # try to load the env file if there is one
        env.read_env((environ.Path(__file__) - 2).file('.env'))
    except FileNotFoundError:
        # no biggy, just use development settings
        # on the server, there should always be an .env file
        pass

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metahub.settings.development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
