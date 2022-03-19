import os
import shutil
from socket import timeout
import stat
from git import Repo
from temp import *
#import subprocess
import csv
import json
import pandas as pd

class CK:
    def __init__(self):
        self.local_repo_directory_fork = os.path.join(os.getcwd(), 'repos')
        self.local_repo_directory_ck = os.path.join(os.getcwd(), 'ck_result')
        self.local_repo_directory_ck_script = os.path.join(os.getcwd(), 'ck_script')
        self.local_repo_directory_ck_metric = os.path.join(os.getcwd(), 'csv_ck_metric_repo')
        self.repoFork = ['git@github.com:skylot/jadx.git']

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
        print('########### GERANDO METRICAS DO REPOSITORIO ###########')
        os.chdir(self.local_repo_directory_ck_script) #vai para o diretorio do ck_script, para rodar o script ck
        command = 'java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar ' + self.local_repo_directory_fork + '\\ true 0 true ' + self.local_repo_directory_ck + '\\'
        os.system(command) #abre um cmd separado e roda o comando que vc colocar em command

    def remove_files_ck(self):
        if os.path.isdir(self.local_repo_directory_ck):
            print('########### REMOVENDO METRICAS DO REPOSITORIO ###########')
            self.chdirectory(self.local_repo_directory_ck)
            for file in os.listdir(self.local_repo_directory_ck):
                path = os.path.join(self.local_repo_directory_ck, file)
                try:
                    shutil.rmtree(path)
                except OSError:
                    os.remove(path)
    
    def get_loc_method_csv(self):
        soma_loc = 0
        with open('method.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                soma_loc = soma_loc + int(row['loc'])
        
        return soma_loc
    
    def get_cbo_class(self):
        soma_cbo = 0
        with open('class.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                soma_cbo = soma_cbo + int(row['cbo'])
        
        return soma_cbo

    def get_dit_class(self):
        soma_dit = 0
        with open('class.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                soma_dit = soma_dit + int(row['dit'])
        
        return soma_dit

    def get_lcom_class(self):
        soma_lcom = 0
        with open('class.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                soma_lcom = soma_lcom + int(row['lcom'])
        
        return soma_lcom

    def create_csv_metric(self, repo):
        print('########### OBETENDO METRICAS DO REPOSITORIO ###########')
        os.chdir(self.local_repo_directory_ck)
        loc = self.get_loc_method_csv() #get loc metric
        cbo = self.get_cbo_class() #get cbo metric
        dit = self.get_dit_class() #get dit metric
        lcom = self.get_lcom_class() #get lcom metric

        os.chdir(self.local_repo_directory_ck_metric)
        json_result = [ '', repo, loc, cbo, dit, lcom ]
        with open('metric_repo.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(json_result)

    def call_ck(self):
        for repo in self.repoFork:
            try:
                self.clone_repo_fork(repo, 'master') #Clona repositorio na master
            except:
                self.clone_repo_fork(repo, 'main') #Se der error ao tentar clonar na master, tenta clonar pela main
            
            self.ck_command()
            self.create_csv_metric(repo)
            self.delete_fork_directory(repo)
