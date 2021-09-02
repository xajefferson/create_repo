#!/usr/bin/env python3
import os
import sys
import argparse
import requests
import json
from pathlib import Path
from tkinter import filedialog
from colorama import Fore, Back, Style

# Add your personal acess token here
# This was a token used for testing. It no longer works :)

# TODO: Create new token
# TODO: Add file dir structure from serious python


def read_cfg():

    try:

        with open("test.cfg") as confFile:  # TODO: Change this to setup
            str1 = confFile.readline()
            # str1 = str1.replace(" ", "")
            str1_arr = str1.split("=")
            to_return1 = str1_arr[1]

            str2 = confFile.readline()
            str2_arr = str2.split("=")
            to_return2 = str2_arr[1]

        return to_return1, to_return2

    except IOError:
        print("Could not read from file", file=sys.stderr)
        sys.exit(1)


def main():

    github_username, token = read_cfg()

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", metavar='Name',
                        help="Repository name",
                        required=True)

    parser.add_argument("-p", metavar='Privacy',
                        help="Enter 'public' for a public repository " +
                        "or 'private' for a private one.",
                        required=True)

    args = parser.parse_args()

    repo_name = args.n
    privacy_type = args.p
    privacy_type = privacy_type.lower()

    # Checks if user requested a private or public repository
    if ((privacy_type != 'public') and (privacy_type != 'private')):
        print("Invalid repository privacy type", file=sys.stderr)
        sys.exit(1)

    template_git_ignore_path = os.path.join(os.getcwd(), "gitignore.cfg")
    print("Path to gitignore.cfg is: %s" % template_git_ignore_path)

    # Stores main dir in a var
    main_dir = os.getcwd()
    print("Path to create_repo.py's directory is: {}".format(main_dir))

    # Window for repo selection is opened
    print(Fore.BLACK + Back.GREEN + "Selection window opeing")
    print("Choose a directory for the new repository...")
    print(Style.RESET_ALL)
    desired_repo_path = filedialog.askdirectory(mustexist=True)
    desired_repo_path = os.path.join(desired_repo_path, repo_name)
    print("The repository will be created in: {} ".format(desired_repo_path))

    # Create repo dir and change to it
    Path(desired_repo_path).mkdir(parents=True, exist_ok=True)
    os.chdir(desired_repo_path)

    if (privacy_type == 'public'):
        print("Public was selected")
        pt = False
    else:
        print("Private was selected")
        pt = True

    # Create README
    print("Creating README.md...")
    with open('README.md', 'w') as fp:
        fp.write("# %s" % repo_name)

    # Create gitignore
    print("Creating the .gitignore file")
    with open(template_git_ignore_path, 'r') as firstfile,\
            open('.gitignore', 'a') as secondfile:
        for line in firstfile:
            secondfile.write(line)

    # Initialize repo
    print("Initializing git repository...")
    print(os.system('git init'))

    os.system('git status')
    os.system('git add .')
    os.system('git status')

    os.system('git commit -m "First commit"')
    os.system('git status')

    # Create the remote repo
    payload = json.dumps({'name': repo_name, 'private': pt})
    print("Payload is: " + str(payload))

    url = 'https://api.github.com/user/repos'
    print("The url being used is: %s" % url)

    response = requests.post(url,
                             headers={'Authorization': 'token ' + token},
                             data=payload)

    if (response.status_code == 201):
        print("Status code: 201 \nRepository created successfully! ")
    else:
        print("Status code: 401 \nRemote repository creation was unsuccessful.\
            \nExiting program... ")
        # TODO: Add code that cleans up all the files that were created
        # up to this point
        exit()

    os.system('git branch develop')
    os.system('git checkout develop')

    print('Adding origin to Github...')
    link = 'https://github.com/%s/%s.git' % (github_username, repo_name)
    os.system('git remote add origin ' + link)

    # Pushing to remote repos
    os.system('git push -u origin master')
    os.system('git push -u origin develop')

    print("Opening new vs code window...")
    os.system('code .')


if __name__ == '__main__':
    main()
