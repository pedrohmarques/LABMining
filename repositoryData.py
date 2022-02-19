import json

class RepositoryData:
    def __init__(self):
        self._fileName = 'repositories.json'

    def get(self):
        with open(self._fileName) as json_file:
            repositories = json.load(json_file)
        return repositories

    def update(self, repositories):
        with open(self._fileName, 'w') as outfile:
            json.dump(repositories, outfile)