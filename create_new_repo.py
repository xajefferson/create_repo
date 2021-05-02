#!/usr/bin/env python3.9

import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", metavar = 'Name', help="Repository name", required=True)
    parser.add_argument("-p", metavar = 'Privacy', help= "Enter 'public' for a public repository or 'private' for a private one.", required=True)


    args = parser.parse_args()

    repo_name = args.n
    privacy_type = args.p
    privacy_type = privacy_type.lower()
    script_dir = os.getcwd()

    token = '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'
    

    if ((privacy_type != 'public') and (privacy_type != 'private')): 
        print("Invalid repository type")
        exit()
    
    print("Script directory is: %s" % script_dir)
    os.chdir("..")
    os.chdir("..")
    projects_dir = os.getcwd()
    print("Project directory is: %s" % projects_dir)

    '''TODO: 1) We need to make a dir for the new repo
            2) Change into that dir
            3) initialize the new project dir
            4) show git status
            5) git add .
            6) show status
            7) 
    '''

    if (privacy_type == 'public'):
        print("Public was selected")
        pt = 'false'
    else:
        print("Private was selected")
        pt = 'true'

    #Example curl req
    #    var = 'curl -i -H "Authorization: token %s" -d \'{ "name": %s, "auto_init": true, "private": %s, "gitignore_template": "nanoc" }\' https://api.github.com/user/repos' % (token, repo_name, pt)

    var = 'curl -i -H "Authorization: token %s" -d \'{ "name": "%s", "auto_init": true, "private": %s}\' https://api.github.com/user/repos > .server_response.log' % (token, repo_name, pt)
    print(var)

    
    new_repo_dir = projects_dir + '/' +repo_name
    print("Making a new directory: %s" % new_repo_dir)
    os.mkdir(new_repo_dir)

    print("Changing to new directory...")
    os.chdir(new_repo_dir)
    print("The current directory is now: %s" % os.getcwd())

    print("Initializing git repository...")
    os.system('git init')

    print("Creating the .gitignore file")
    os.system('cp ~/Documents/Projects/.gitignore .gitignore')

    print("Creating README.txt..")
    os.system('touch README.txt')

    
    print("Creating git repo...")
    os.system(var) #Command that creates the repo


    os.system('git status')
    os.system('add .')

    os.system('git commit -m "Initial commit"')
    os.system('git status')

    os.system('git branch develop')
    os.system('git checkout master')
    os.system('git checkout develop')
    

    url = 'https://github.com/xajefferson/' + repo_name + '.git'

    os.system('git remote add origin ' + url)
    os.system('git push -u origin master')
    os.system('git push -u origin develop')


    print("Opening new vs code window...")
    os.system('code .')

    os.chdir(script_dir)
    



    


    

if __name__ == '__main__':
    main()