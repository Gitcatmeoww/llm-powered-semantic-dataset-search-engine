import weaviate

client = weaviate.Client("http://localhost:8080")

def insert_dataset(name, description, vector):
    data_object = {
        "name": name,
        "description": description,
        "vector": vector,
    }
    client.data_object.create(data_object, "Dataset")

def search_datasets(query_vector):
    return client.query.get("Dataset", ["name", "description"]).with_vector(query_vector).with_limit(5).do()
