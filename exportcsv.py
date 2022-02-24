import pandas as pd
from repositoryData import RepositoryData
def exportDataToCsv():
    repositories = RepositoryData().get()
    df = pd.json_normalize(repositories)
    csvText = df.to_csv().replace("\r", "")
    filename = f"repositories.csv"
    print(f"Export repositories on file {filename}")
    file = open(filename, "w")
    file.write(csvText)
    file.close()
    print("Finished export")