import os
import shutil
from socket import timeout
import stat
from git import Repo
from temp import *
#import subprocess
from tempfile import NamedTemporaryFile
import csv
import json
import pandas as pd
import math

class CK:
    def __init__(self):
        self.local_repo_directory_fork = os.path.join(os.getcwd(), 'repos')
        self.local_repo_directory_ck = os.path.join(os.getcwd(), 'ck_result')
        self.local_repo_directory_ck_script = os.path.join(os.getcwd(), 'ck_script')
        self.local_repo_directory_ck_metric = os.path.join(os.getcwd(), 'csv_ck_metric_repo')
        self.repoFork = []
        self.repo_ignorados = 0

    def get_repo_to_analyze(self, name):
       with open('repositories_java.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if(row['responsible'] == name and row["analysed"] == 'no'):
                    self.repoFork.append(row)

    def delete_fork_directory(self, repo):
        print('########### DELETANDO: ' + repo + ' ###########')
        if os.path.exists(self.local_repo_directory_fork):
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
            
        try:
            Repo.clone_from(repo, 
                self.local_repo_directory_fork, branch=dest) 
        except Exception:
            pass

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
    
    def get_cbo_class(self, length_csv):
        mediana_cbo = 0
        with open('class.csv', 'r') as file:
            reader = csv.DictReader(file)
            row = list(reader)[length_csv]
            mediana_cbo = row['cbo'] 
        
        return mediana_cbo

    def get_dit_class(self):
        max_dit = 0
        with open('class.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if(max_dit < int(row['dit'])):
                    max_dit = int(row['dit'])
        
        return max_dit

    def get_lcom_class(self, length_csv):
        mediana_lcom = 0
        with open('class.csv', 'rt') as file:
            reader = csv.DictReader(file)
            row = list(reader)[length_csv]
            mediana_lcom = row['lcom'] 
        return mediana_lcom

    def get_length_csv(self):
        length_csv = 0
        med = 0.5
        with open('class.csv', 'r') as file:
            value = len(file.readlines()) / 2
            whole, frac = math.modf(value)
            print(frac)
            print(med)
            if(frac < med):
                length_csv = math.floor(value)
            else:
                length_csv = math.ceil(value)

        return length_csv

    def create_csv_metric(self, repo):
        print('########### OBTENDO METRICAS DO REPOSITORIO ###########')
        os.chdir(self.local_repo_directory_ck)
        length_csv = self.get_length_csv()
        if(length_csv > 0):
            loc = self.get_loc_method_csv() #get loc metric
            cbo = self.get_cbo_class(length_csv) #get cbo metric
            dit = self.get_dit_class() #get dit metric
            lcom = self.get_lcom_class(length_csv) #get lcom metric
            params = { 'LCOM': int(lcom), 'DIT': int(dit), 'CBO': int(cbo), 'LOC': int(loc) }
            self.update_repo_analyzed(repo, params)
        else:
            print('########### REPOSITORIO: ' + repo['sshUrl'] + ' IGNORADO ###########')
            os.chdir('..')
            repos = pd.read_csv('repositories_java.csv')
            repos.loc[repos["sshUrl"] == repo['sshUrl'], "analysed"] = 'yes'
            repos.to_csv('repositories_java.csv', index=False)
            self.repo_ignorados = self.repo_ignorados + 1
    
    def update_repo_analyzed(self, repo, params):
        os.chdir('..')
        repos = pd.read_csv('repositories_java.csv')
        repos.loc[repos["sshUrl"] == repo['sshUrl'], "analysed"] = 'yes'
        repos.loc[repos["sshUrl"] == repo['sshUrl'], "LOC"] = int(params['LOC'])
        repos.loc[repos["sshUrl"] == repo['sshUrl'], "LCOM"] = params['LCOM']
        repos.loc[repos["sshUrl"] == repo['sshUrl'], "DIT"] = params['DIT']
        repos.loc[repos["sshUrl"] == repo['sshUrl'], "CBO"] = params['CBO']
        repos.to_csv('repositories_java.csv', index=False)

    def call_ck(self):
        self.get_repo_to_analyze('Henrique') #Pass the name of the responsible
        for repo in self.repoFork:
            try:
                self.clone_repo_fork(repo['sshUrl'], 'master') #Clona repositorio na master
            except:
                self.clone_repo_fork(repo['sshUrl'], 'main') #Se der error ao tentar clonar na master, tenta clonar pela main
            
            self.ck_command()
            self.create_csv_metric(repo)
            self.delete_fork_directory(repo['sshUrl'])
        
        print('########### SCRIPT FINALIZADO COM ' + self.repo_ignorados + ' REPOSITORIOS IGNORADOS ###########')
            
