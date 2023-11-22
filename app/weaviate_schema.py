import weaviate


def create_schema(client):
    class_obj = {
        "class": "Dataset",
        "description": "A class to represent a dataset with vector embeddings",
        "properties": [
            {
                "name": "name",
                "dataType": ["string"],
                "description": "The name of the dataset",
            },
            {
                "name": "description",
                "dataType": ["text"],
                "description": "A description of the dataset",
            },
            {
                "name": "vector",
                "dataType": ["number[]"],
                "description": "The vector embedding of the dataset",
            },
        ],
    }
    
    schema = {"classes": [class_obj]}
    client.schema.create(schema)


def delete_class_if_exists(client, class_name):
    try:
        client.schema.delete_class(class_name)
    except weaviate.exceptions.UnexpectedStatusCodeException as e:
        if e.status_code != 404:
            raise e
