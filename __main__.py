from repositories import Repository
from repositoryData import RepositoryData
from exportcsv import exportDataToCsv

print("Options")
print("1 - Atualiza Repositorios")
print("2 - Exporta para CSV")

op = input()
if op == '1':
    repository = Repository("") #PASSAR SEU TOKEN AQUI
    print("Get Repositories")
    repositoriesJs = repository.get_repositories("JavaScript", 100)
    RepositoryData().update(repositoriesJs)
elif op == '2':
    exportDataToCsv()
else:
    print("Invalido")
