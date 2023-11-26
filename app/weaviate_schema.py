# weaviate_schema.py
import weaviate

def create_schema(client):
    schema = {
        "classes": [
            {
                "class": "TableProfile",
                "description": "Profile of a database table",
                "properties": [
                    {
                        "name": "tableName",
                        "dataType": ["string"],
                        "description": "The name of the table",
                    },
                    {
                        "name": "schema",
                        "dataType": ["text"],
                        "description": "Schema of the table",
                    },
                    {
                        "name": "stats",
                        "dataType": ["text"],
                        "description": "Statistical summary of the table",
                    },
                    {
                        "name": "entries",
                        "dataType": ["text"],
                        "description": "Sample entries from the table",
                    },
                ],
            },
        ]
    }
    client.schema.create(schema)

def delete_class_if_exists(client, class_name):
    try:
        client.schema.delete_class(class_name)
    except weaviate.exceptions.UnexpectedStatusCodeException as e:
        if e.status_code != 404:
            raise e
