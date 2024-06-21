import os
from dotenv import load_dotenv
from algoliasearch.search_client import SearchClient



# Algolia search client
ALGOLIA_APP_ID = os.getenv('ALGOLIA_APP_ID')
ALGOLIA_API_KEY = os.getenv('ALGOLIA_API_KEY')
ALGOLIA_INDEX_NAME = os.getenv('ALGOLIA_INDEX_NAME')

client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
index = client.init_index(ALGOLIA_INDEX_NAME)

res = index.save_objects([
    {'firstname': 'Jimmie', 'lastname': 'Barninger'},
    {'firstname': 'Warren', 'lastname': 'Speach'}
], {'autoGenerateObjectIDIfNotExist': True})

print("added items.")
print(res)


