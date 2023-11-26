import weaviate
from .weaviate_schema import create_schema, delete_class_if_exists

def initialize_weaviate_client(url):
    client = weaviate.Client(url)
    delete_class_if_exists(client, "TableProfile")
    create_schema(client)
    return client

# def search_datasets(query_vector):
#     return client.query.get("Dataset", ["name", "description"]).with_vector(query_vector).with_limit(5).do()
