import weaviate


def create_class_if_not_exists(client, class_schema):
    try:
        # Check if class already exists
        existing_classes = client.schema.get()
        existing_class_names = [c['class'] for c in existing_classes['classes']]
        class_name = class_schema['class']
        
        if class_name not in existing_class_names:
            client.schema.create_class(class_schema)
            print(f"Class {class_name} created.")
        else:
            print(f"Class {class_name} already exists.")
    except weaviate.exceptions.UnexpectedStatusCodeException as e:
        print(f"An error occurred: {str(e)}")


def create_schema(client):
    schema = {
        "class": "TableProfile",
        "description": "Profile of a database table",
        "vectorizer": "text2vec-openai",
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
        ]
    }

    create_class_if_not_exists(client, schema)