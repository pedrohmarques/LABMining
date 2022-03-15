from asyncio import subprocess
import os
import shutil
from socket import timeout
import stat
from git import Repo
from temp import *
import subprocess
import json

local_repo_directory_fork = os.path.join(os.getcwd(), 'repos')
local_repo_directory = os.path.join(os.getcwd(), 'ck')
destination = 'main'

repoFork = ['git@github.com:Snailclimb/JavaGuide.git']
#repoFork = []

def delete_fork_directory():
    print("Deletando diretorio Fork")
    for root, dirs, files in os.walk(local_repo_directory_fork): 
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    shutil.rmtree(local_repo_directory_fork)


def clone_repo_fork(repo, dest):
    if os.path.exists(local_repo_directory_fork):
        print("DirFork Existe")
        delete_fork_directory()
        print("Diretorio não existe, Clonando repo fork") 
        Repo.clone_from(repo, 
            local_repo_directory_fork, branch=dest)
    else:
        print("Diretorio não existe, Clonando repo fork")    
        Repo.clone_from(repo, 
            local_repo_directory_fork, branch=dest) 

def chdirectory(path):
    os.chdir(path)

def read_report_lighthouse():
    print("------------ GET SPEED-INDEX ------------")
    file = open('lhreport.json', encoding="utf8")
    data = json.load(file)
    
    if data["audits"]["speed-index"]["score"] == None:
        file.close()
        return None
    else:
        speed_index_data = data["audits"]["speed-index"]
        speed_index_seconds = speed_index_data["displayValue"]
        speed_index_seconds = speed_index_seconds.replace("Â", "")
        file.close()
        return speed_index_seconds
    
def npm_command():
    os.chdir(local_repo_directory_fork)
    subprocess.check_call('npm install', shell=True)
    file = open('package.json', encoding="utf8")
    data = json.load(file)
    next_command = data['scripts']
    if 'serve' in next_command:
        next_command = 'npm run serve'
    elif 'start' in next_command:
        next_command = 'npm start'
    else:
        next_command = 'npm run dev'
    
    file.close()
    os.system('start cmd /c ' + next_command)
    

        
def main():
    print('main')
main()