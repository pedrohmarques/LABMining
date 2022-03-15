import os
import shutil
from socket import timeout
import stat
from git import Repo
from temp import *
#import subprocess
import json

class CK:
    def __init__(self):
        self.local_repo_directory_fork = os.path.join(os.getcwd(), 'repos')
        self.local_repo_directory_ck = os.path.join(os.getcwd(), 'ck')
        self.repoFork = ['git@github.com:Snailclimb/JavaGuide.git']

    def delete_fork_directory(self, repo):
        print('########### DELETANDO: ' + repo + ' ###########')
        for root, dirs, files in os.walk(self.local_repo_directory_fork): 
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)
        shutil.rmtree(self.local_repo_directory_fork)


    def clone_repo_fork(self, repo, dest):
        print('########### CLONANDO: ' + repo + ' ###########')
        if os.path.exists(self.local_repo_directory_fork):
            self.delete_fork_directory(repo)
            Repo.clone_from(repo, 
                self.local_repo_directory_fork, branch=dest)
        else:
            Repo.clone_from(repo, 
                self.local_repo_directory_fork, branch=dest) 

    def chdirectory(path):
        os.chdir(path)

    def read_report_lighthouse(): #FUNÇÃO DE EXEMPLO DE COMO LER UM JSON
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
        
    def ck_command(self):
        os.chdir(self.local_repo_directory_ck) #vai para o diretorio do ck
        #subprocess.check_call('npm install', shell=True) # roda comando shell diretamente.
        
        command = 'COLOCAR COMANDO QUE CHAMA O CK AQUI'
        os.system('start cmd /c ' + command) #abre um cmd separado e roda o comando que vc colocar em command
    
    def call_ck(self):
        for repo in self.repoFork:
            try:
                self.clone_repo_fork(repo, 'master') #Clona repositorio na master
            except:
                self.clone_repo_fork(repo, 'main') #Se der error ao tentar clonar na master, tenta clonar pela main
            
            self.delete_fork_directory(repo)
