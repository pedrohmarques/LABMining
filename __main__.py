from repositories import Repository
from repositoryData import RepositoryData

repository = Repository("") #PASSAR SEU TOKEN AQUI
print("Get Java Repositories")
repositoriesJava = repository.get_repositories("java", 100)
RepositoryData().update(repositoriesJava)