import requests

class Repository:
    def __init__(self, token):
        self.token = token
    
    def __get_query(self, primaryLanguage, after = 'null'):
        query = f"""
        {{
            search(query:"stars:>100 ", type:REPOSITORY, first:100, after:{{after}}){{
                nodes{{
                    ... on Repository {{
                        nameWithOwner
                            closedIssues: issues(states: CLOSED){{
                                totalCount
                            }}
                        issues{{
                            totalCount
                        }}
                    }}
                }}
            }}
        }}
        """
        return query

    def get_repositories(self, primaryLanguage, num_repositories):
        headers = headers = {'Authorization': f'Bearer {self.token}'}
        after = 'null'
        repositories = list
        for i in range(10):
            print("get repositories: ", i)
            query = self.__get_query(primaryLanguage, after)
            result = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)

            if result.status_code == 200:
                data = result.json()['data']['search']
                after = data['pageInfo']['endCursor']
                repositories.__add__(list(map(lambda x: x, data['nodes'])))

       print(f"\rRetrieve {len(repositories)} repositories")
       return repositories

