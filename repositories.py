import requests

class Repository:
    def __init__(self, token):
        self.token = token
    
    def __get_query(self, primaryLanguage, after):
        if after == None:
            query = f"""
            {{
                search(query:"stars:>100  ", type:REPOSITORY, first:100){{
				pageInfo{{
					startCursor
					hasNextPage
					endCursor
				}}
				nodes{{
					... on Repository {{
						nameWithOwner
						createdAt
					}}
				}}
			    }}
            }}
            """
        else:
            query = f"""
            {{
                search(first:100, after:"{after}", query:"stars:>100  ", type:REPOSITORY){{
				pageInfo{{
					startCursor
					hasNextPage
					endCursor
				}}
				nodes{{
					... on Repository {{
						nameWithOwner
						createdAt
					}}
				}}
			    }}
            }}
            """
        return query

    def get_repositories(self, primaryLanguage, num_repositories):
        headers = headers = {'Authorization': f'Bearer {self.token}'}
        after = None
        res = []
        for i in range(10):
            query = self.__get_query(primaryLanguage, after)
            result = requests.post("https://api.github.com/graphql", json={'query': query}, headers=headers)
            if result.status_code == 200:
                data = result.json()['data']['search']
                after = data['pageInfo']['endCursor']
                repositories = list(map(lambda x: x, data['nodes']))
                res = res + repositories
        return res          
        #[{"nameWithOwner": "GAGA", "createdAt": "2017-04-18T10:33:05Z"}]
            
