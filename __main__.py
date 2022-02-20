from repositories import Repository
from repositoryData import RepositoryData

repository = Repository("") #PASSAR SEU TOKEN AQUI
print("Get Repositories")
repositoriesJs = repository.get_repositories("JavaScript", 100)
RepositoryData().update(repositoriesJs)