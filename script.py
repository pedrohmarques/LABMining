from textwrap import indent
import requests

gitlabURI = 'https://gitlab.com/api/graphql'
gitlabToken = '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'
gitlabHeaders = {"Authorization": "Bearer " + gitlabToken}
gitlabStatusCode = 200

def run_query(uri, query, statusCode, headers): 
    request = requests.post(uri, json={'query': query}, headers=headers)
    if request.status_code == statusCode:
        return request.json()
    else:
        raise Exception(f"Unexpected status code returned: {request.status_code}")



query = """query {
    characters {
    results {
      name
      status
      species
      type
      gender
    }
  }
}"""

result = run_query(gitlabURI, query, gitlabStatusCode, gitlabHeaders)
print(result)