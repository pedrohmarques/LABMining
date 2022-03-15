from repositories import Repository
from repositoryData import RepositoryData
from exportcsv import exportDataToCsv
from ck import CK

print("Options")
print("1 - Atualiza Repositorios")
print("2 - Exporta para CSV")
print("3 - Análise CK")

op = input()
if op == '1':
    repository = Repository("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") #PASSAR SEU TOKEN AQUI
    print("Get Repositories")
    repositoriesJs = repository.get_repositories("JavaScript", 100)
    RepositoryData().update(repositoriesJs)
        
elif op == '2':
    exportDataToCsv()

elif op == '3':
    CK().call_ck()
else:
    print("Invalido")
