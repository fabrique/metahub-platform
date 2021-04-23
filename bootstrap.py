#!/usr/bin/env python3
import argparse
import contextlib
import itertools
import os
import re
import shlex
import subprocess
import sys
from os import getcwd
from string import digits, ascii_letters, punctuation
from threading import Event, Thread

IS_PY2 = sys.version_info < (3, 0)

if not IS_PY2:
    from venv import EnvBuilder
    from secrets import choice
else:
    from random import choice


def error(message):
    sys.stderr.write('\033[91m{message}\033[0m\n'.format(message=message))


def warning(message):
    sys.stdout.write('\033[93m{message}\033[0m\n'.format(message=message))


def success():
    sys.stdout.write('[\033[92mok\033[0m]\n')


def highlight(message):
    return '\033[94m{message}\033[0m'.format(message=message)


@contextlib.contextmanager
def print_spinner(show=True):
    if not show:
        yield
        return

    # use this to print a spinner while a command is running

    done = Event()
    spinner_chars = itertools.cycle(['-', '\\', '|', '/'])

    def spin():
        while not done.wait(.1):
            sys.stdout.write(next(spinner_chars))  # write the next character
            sys.stdout.flush()  # flush stdout buffer (actual character display)
            sys.stdout.write('\b')  # erase the last written char
        sys.stdout.flush()

    spinner = Thread(target=spin)
    spinner.start()
    try:
        yield
    except:
        done.set()
        if spinner.is_alive():
            spinner.join()
        raise
    else:
        done.set()
        if spinner.is_alive():
            spinner.join()


def call(command, show_spinner=True, input=None, suppress_output=False, **kwargs):
    """
    Run the process and only print when it errors

    :param command: The command (list) to run
    :param show_spinner: Whether to show the spinner while the command is running
    :param input: String of input to pipe into command.
    :param suppress_output: suppress output will not print anything but return True (success) or False depending on error
    :return:
    """

    with print_spinner(show_spinner):
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE if input else None,
                                   **kwargs)
        try:
            stdout, stderr = process.communicate(input=input or subprocess.PIPE)
        except:
            process.kill()
            process.wait()
            raise
        retcode = process.poll()

        if stderr or retcode:
            if suppress_output:
                return False
            for line in stdout.decode('utf8').split('\n'):
                warning(line)
            for line in stderr.decode('utf8').split('\n'):
                error(line)
    return True


def check_requirement(command, message, hash_command=True):
    run_command = ['hash'] + shlex.split(command) if hash_command else shlex.split(command)
    try:
        subprocess.check_call(run_command, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
        return True
    except subprocess.CalledProcessError:
        error(message)


def check_if_venv():
    """
                      py2  py3  py2env py3envX py3envY
    sys.prefix         A    A    A      A        A
    sys.real_prefix    -    -    B      B        -
    sys.base_prefix    -    A    -      A        B

    There seem to be two versions of the py3 env, with different settings
    (depending on how the environment wat created).
    :return:
    """

    prefix = sys.prefix
    real_prefix = getattr(sys, 'real_prefix', None)
    base_prefix = getattr(sys, 'base_prefix', None)

    # Make sure we are not in an env
    if IS_PY2:
        # simple test
        is_venv = bool(real_prefix)
    else:
        # same simple test, but if it fails, check if prefix and base_prefix are the same.
        is_venv = bool(real_prefix) or prefix != base_prefix

    if is_venv:
        sys.exit('It seems like you have an environment on. Please first deactivate it (call `deactivate`)')

    return not is_venv


def check_requirements():
    requirements = [
        check_requirement('python3', 'Python3 is required. Try `brew install python3`.'),
    ]

    return all(requirements)


def install_venv(location, clean=False):
    sys.stdout.write('Installing virtual environment at {} '.format(highlight(location)))
    sys.stdout.flush()
    venv_exists = os.path.exists(location)
    if IS_PY2:
        if clean:
            call(['python3', '-m', 'venv', location, '--clear', '--prompt=metahub', ])
        elif not venv_exists:
            call(['python3', '-m', 'venv', location, '--prompt=metahub', ])
    else:
        builder = EnvBuilder(
            clear=clean,
            upgrade=venv_exists and not clean,
            with_pip=True,
            prompt='metahub'
        )
        builder.create(location)

    if venv_exists and not clean:
        warning('Virtual environment already exists, not created.')

    success()


def install_python_requirements(pip):
    sys.stdout.write('Installing python requirements ')
    sys.stdout.flush()

    call([pip, 'install', '-U', 'pip', ])
    call([
        pip, 'install',
        '-r', 'requirements/development.txt'])

    success()


def write_env_file(clean=False):
    contents = ''

    # Read existing env example file if it exists
    env_example = os.path.join(os.getcwd(), 'env.example')
    if os.path.exists(env_example):
        contents += '{}\n'.format(open(env_example, 'r').read())

    # Auto-generate a secret key
    allowed_chars = digits + ascii_letters + punctuation
    contents += 'DJANGO_SECRET_KEY="{}"'.format(''.join([choice(allowed_chars) for k in range(64)]))

    # Write the env file
    with open(os.path.join(os.getcwd(), os.path.pardir, '.env'), 'w' if clean else 'a') as f:
        f.write(contents)


def run(venv_location, clean=False):
    pip = os.path.join(venv_location, 'bin', 'pip')

    if check_if_venv() and check_requirements():
        install_venv(venv_location, clean=clean)
        install_python_requirements(pip)
        write_env_file(clean=clean)
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bootstrap metahub')

    parser.add_argument(
        '--ignore-workon-home',
        action='store_true',
        default=False,
        help='Ignore virtualenvwrapper WORKON_HOME to determine virtual environment location'
    )

    parser.add_argument(
        '--clean',
        action='store_true',
        dest='clean',
        help='Create clean environment',
        default=False,
    )

    args = parser.parse_args()

    venv_location = os.path.abspath(os.path.join(getcwd(), os.path.pardir, 'venv'))
    workon_home = os.environ.get('WORKON_HOME')
    if not args.ignore_workon_home and workon_home:
        venv_location = os.path.join(os.path.expanduser(workon_home), 'metahub')

    if run(
        venv_location,
        clean=args.clean,
    ):
        activate_command = '. venv/bin/activate'
        if not args.ignore_workon_home and workon_home:
            activate_command = 'workon metahub'

        update_command = 'src/manage.py update --initial'

        sys.stdout.write('\nDone! \n\nRun the following commands:\n\n')
        sys.stdout.write('\t{} to go up to project directory.\n'.format(highlight('cd ..')))
        sys.stdout.write('\t{} to activate the virtual environment.\n'.format(highlight(activate_command)))
        sys.stdout.write('\t{} to bring everything up to date.\n'.format(highlight(update_command)))
        sys.stdout.write(
            '\t{} to update yarn, compile sass and js, and watch for changes.\n'.format(
                highlight('src/manage.py webpack')))
        sys.stdout.write('\t{} simultaneously to serve your website locally.\n\n'.format(
            highlight('src/manage.py runserver 0.0.0.0:8000')))
