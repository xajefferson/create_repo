#!/usr/bin/env python3.9

import argparse
import requests
import json
#import urllib2 
import sys
import os

github_username = 'xajefferson'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", metavar = 'Name', help="Repository name", required=True)
    parser.add_argument("-p", metavar = 'Privacy', help= "Enter 'public' for a public repository or 'private' for a private one.", required=True)


    args = parser.parse_args()

    repo_name = args.n
    privacy_type = args.p
    privacy_type = privacy_type.lower()
    script_dir = os.getcwd()
    new_git_ignore_path = os.path.join(os.getcwd(),".gitignore")
    print("Path to .gitignore is: %s" % new_git_ignore_path)

    token = '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'
    

    if ((privacy_type != 'public') and (privacy_type != 'private')): 
        print("Invalid repository type")
        exit()
    
    print("Create repo script is located in: %s" % script_dir)
    os.chdir("..")
    os.chdir("..")
    projects_dir = os.getcwd()
    print("New project repository directory is: %s" % projects_dir)

    if (privacy_type == 'public'):
        print("Public was selected")
        pt = 'false'
    else:
        print("Private was selected")
        pt = 'true'

    #Example curl req
    #    var = 'curl -i -H "Authorization: token %s" -d \'{ "name": %s, "auto_init": true, "private": %s, "gitignore_template": "nanoc" }\' https://api.github.com/user/repos' % (token, repo_name, pt)

    var = 'curl -i -H "Authorization: token %s" -d \'{ "name": "%s", "auto_init": false, "private": %s}\' https://api.github.com/user/repos > .git_server_response.log' % (token, repo_name, pt)
    print(var)

    #curl -i -H "Authorization: token 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" -d '{ "name": "test", "auto_init": true, "private": false}' https://api.#github.com/user/repos > .server_response.log

    
    new_repo_dir = projects_dir + '/' +repo_name
    print("Making a new directory: %s" % new_repo_dir)
    os.mkdir(new_repo_dir)

    print("Changing to new directory...")
    os.chdir(new_repo_dir)
    print("The current directory is now: %s" % os.getcwd())
    #Now the program is in the project directory

    print("Creating README.md...")
    # Creates the README
    with open('README.md', 'w') as fp:
        fp.write("#%s" % repo_name)

    print("Creating the .gitignore file")
    os.system('cp %s .gitignore' % new_git_ignore_path)


    
    print("Initializing git repository...")
    print(os.system('git init'))

    os.system('git status')
    os.system('git add .')
    os.system('git status')

    os.system('git commit -m "First commit"')
    os.system('git status')

    #Now to create the remote repo

    payload = json.dumps({'name' : repo_name, 'private' : pt})  
    print("Payload is: " + str(payload))

    url = 'https://api.github.com/user/repos' 
    print("The url being used is: %s" % url)

    response = requests.post(url, headers ={'Authorization': 'token ' + token}, data =payload)

    #response = 201
    if (response.status_code == 201):
       print("Status code: 201 \nRepository created sucessfully! ")
    else:
        print("Status code: 401 \nRemote repository creation was unsucessful.\nExiting program... ")
        #TODO: Add code that cleans up all the files that were created up to this point
        exit()

    
    os.system('git branch develop')
    os.system('git checkout develop')
  
    
    print('Adding origin to Github...')
    link = 'https://github.com/%s/%s.git' % (github_username, repo_name)
    os.system('git remote add origin ' + link)

    os.system('git branch master')
    os.system('git push -u origin master')

    os.system('git checkout develop')
    os.system('git push -u origin develop')

    '''
    os.system('git branch master')
    os.system('git checkout master')


    os.system('git status')
    os.system('git add .')

    os.system('git commit -m "Initial commit"')
    os.system('git status')

    os.system('git branch develop')
    os.system('git checkout develop')
    os.system('git status')



  


    print("Creating git repo...")
    os.system(var) #Command that creates the repo

    

    url = 'https://github.com/xajefferson/' + repo_name + '.git'

    os.system('git remote add origin ' + url)

    os.system('git push -u')

    os.system('git checkout develop')


    '''

    print("Opening new vs code window...")
    os.system('code .')

    print("Before: %s" % os.getcwd())
    os.chdir(script_dir)
    print("After: %s" % os.getcwd())

if __name__ == '__main__':
    main()