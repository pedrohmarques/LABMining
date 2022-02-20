import requests

class Repository:
    def __init__(self, token):
        self.token = token
    
    def __get_query(self, primaryLanguage):
        query = f"""
        {{
            search(query:"stars:>100 ", type:REPOSITORY, first:100){{
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
        query = self.__get_query(primaryLanguage)
        result = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)
        print(result)
        if result.status_code == 200:
            data = result.json()['data']['search']
            repositories = list(map(lambda x: x, data['nodes']))
            print(f"\rRetrieve {len(repositories)} repositories")
            return repositories
            
