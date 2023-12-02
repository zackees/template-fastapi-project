"""
  To enter the environment run:
    source activate.sh


  Notes:
    This script is tested to work using python2 and python3 from a fresh install. The only side effect
    of running this script is that virtualenv will be globally installed if it isn't already.
"""


import argparse
import os
import shutil
import subprocess
import sys
import warnings
from shutil import which as find_executable

# This activation script adds the ability to run it from any path and also
# aliasing pip3 and python3 to pip/python so that this works across devices.
_ACTIVATE_SH = """
#!/bin/bash

# Function that computes absolute path of a file
abs_path() {
  dir=$(dirname "$1")
  (cd "$dir" &>/dev/null && printf "%s/%s" "$PWD" "${1##*/}")
}

# Navigate to the directory where the current script resides
bashfile=$(abs_path "${BASH_SOURCE[0]}")
selfdir=$(dirname "$bashfile")
cd "$selfdir"

if [[ "$IN_ACTIVATED_ENV" == "1" ]]; then
  IN_ACTIVATED_ENV=1
else
  IN_ACTIVATED_ENV=0
fi

if [[ "$IN_ACTIVATED_ENV" == "1" ]]; then
  # If it is, set the variable 'IN_ACTIVATED_ENV' to true
  IN_ACTIVATED_ENV=1
else
  # Otherwise, set 'IN_ACTIVATED_ENV' to false
  IN_ACTIVATED_ENV=1
fi

# If the 'venv' directory doesn't exist, print a message and exit.
if [[ ! -d "venv" ]]; then
  echo "The 'venv' directory does not exist, creating..."
  if [[ "$IN_ACTIVATED_ENV" == "1" ]]; then
    echo "Cannot install a new environment while in an activated environment. Please launch a new shell and try again."
    exit 1
  fi
  # Check the operating system type.
  # If it is macOS or Linux, then create an alias 'python' for 'python3'
  # and an alias 'pip' for 'pip3'. This is helpful if python2 is the default python in the system.
  echo "OSTYPE: $OSTYPE"
  if [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu"* ]]; then
    python3 install.py
  else
    python install.py
  fi

  . ./venv/bin/activate
  export IN_ACTIVATED_ENV=1
  echo "Environment created."
  pip install -e .
  exit 0
fi

. ./venv/bin/activate
"""
HERE = os.path.dirname(__file__)
os.chdir(os.path.abspath(HERE))
HERE = os.path.dirname(__file__)
WWW = os.path.join(HERE, "www")


def _exe(cmd: str, check: bool = True, cwd: str | None = None) -> None:
    msg = (
        "########################################\n"
        f"# Executing '{cmd}'\n"
        "########################################\n"
    )
    print(msg)
    sys.stdout.flush()
    sys.stderr.flush()
    # os.system(cmd)
    subprocess.run(cmd, shell=True, check=check, cwd=cwd)


def is_tool(name):
    """Check whether `name` is on PATH."""

    return find_executable(name) is not None

def get_pip() -> str:
    if sys.platform == "win32":
        return "pip"
    return "pip3"


def get_python() -> str:
    return sys.executable


def create_virtual_environment() -> None:
    try:
        _exe(f"{get_python()} -m venv venv")
    except subprocess.CalledProcessError as exc:
        warnings.warn(f"couldn't make virtual environment because of {exc}")
        raise exc

    # _exe('python3 -m venv venv')
    # Linux/MacOS uses bin and Windows uses Script, so create
    # a soft link in order to always refer to bin for all
    # platforms.
    if sys.platform == "win32":
        target = os.path.join(HERE, "venv", "Scripts")
        link = os.path.join(HERE, "venv", "bin")
        if not os.path.exists(link):
            _exe(f'mklink /J "{link}" "{target}"', check=False)
    with open("activate.sh", encoding="utf-8", mode="w") as fd:
        fd.write(_ACTIVATE_SH)
    if sys.platform != "win32":
        _exe("chmod +x activate.sh")


def check_platform() -> None:
    if sys.platform == "win32":
        is_git_bash = os.environ.get("ComSpec", "").endswith("bash.exe")
        if not is_git_bash:
            print("This script only works with git bash on windows.")
            sys.exit(1)


def modify_activate_script() -> None:
    path = os.path.join(HERE, "venv", "bin", "activate")
    text_to_add = '\nPATH="./:$PATH"\n' + "export PATH"
    with open(path, encoding="utf-8", mode="a") as fd:
        fd.write(text_to_add)


def main() -> int:
    in_activated_env = os.environ.get("IN_ACTIVATED_ENV", "0") == "1"
    if in_activated_env:
        print(
            "Cannot install a new environment while in an activated environment. Please launch a new shell and try again."
        )
        return 1
    parser = argparse.ArgumentParser(description="Install the project.")
    parser.add_argument(
        "--remove", action="store_true", help="Remove the virtual environment"
    )
    args = parser.parse_args()
    if args.remove:
        print("Removing virtual environment")
        shutil.rmtree("venv", ignore_errors=True)
        return 0
    if not os.path.exists("venv"):
        create_virtual_environment()
    else:
        print(f'{os.path.abspath("venv")} already exists')
    assert os.path.exists("activate.sh"), "activate.sh does not exist"
    modify_activate_script()
    # Note that we can now just use pip instead of pip3 because
    # we are now in the virtual environment.
    try:
        _exe("./activate.sh && pip install -e .")  # Why does this fail on windows git-bash?
        print(
            'Now use ". ./activate.sh" (at the project root dir) to enter into the environment.'
        )
        return 0
    except subprocess.CalledProcessError:
        print(
            "\n###########\n# WARNING - INSTALL NOT COMPLETE!\n"
            "Please finish install by typing in `. ./activate.sh && pip install -e .`\n"
            "then use `. ./activate.sh` to enter into the environment.\n"
            " (And always use `. ./activate.sh` to enter into the environment.)\n"
        )
        return 0


if __name__ == "__main__":
    sys.exit(main())
