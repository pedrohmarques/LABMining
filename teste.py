import requests

url = 'https://api.github.com/graphql'
json = { 'query' : ' search(query:"stars:>100", type:REPOSITORY, first:100){nodes {... on Repository {nameWithOwnerdiskUsage}}} ' }
api_token = "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"
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)
print (r.text)

