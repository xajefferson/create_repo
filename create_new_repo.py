#!/usr/bin/env python3.9

import argparse
import os



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", metavar = 'Name', help="Repository name", required=True)
    parser.add_argument("-p", metavar = 'Privacy', help= "Enter 'public' for a public repository. The default is private", required=True)
    #parser.add_argument_group()
    
    args = parser.parse_args()

    repo_name = args.n
    privacy_type = args.p
    privacy_type = privacy_type.lower()
    
    if ((privacy_type != 'public') and (privacy_type != 'private')): 
        print("Invalid repository type")
        exit()

    


    

if __name__ == '__main__':
    main()