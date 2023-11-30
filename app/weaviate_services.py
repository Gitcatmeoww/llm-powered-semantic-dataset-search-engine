import weaviate
import json
from datetime import datetime
from pandas import Timestamp

def insert_profile_data(client, profiles):
    for table_name, profile in profiles.items():
        # print(f"Inserted profile for table: {table_name} with data {profile}",  flush=True)
        try:
            # Convert Timestamps to string
            profile = convert_timestamps(profile)

            profile_data = {
                "tableName": table_name,
                "schema": json.dumps(profile["schema"]),
                "stats": json.dumps(profile["stats"]),
                "entries": json.dumps(profile["truncated_entries"]),
            }
            
            # print(f"Inserted profile for table: {table_name} with data {profile}",  flush=True)
            client.data_object.create(data_object=profile_data, class_name="TableProfile")
            
        except Exception as e:
            print(f"Error inserting data for {table_name}: {e}")

# Test only one table: actor
# def insert_profile_data(client, data):
#     try:
#         # Convert Timestamps to string
#         data = convert_timestamps(data)

#         profile_data = {
#             "tableName": "actor",
#             "schema": json.dumps(data["schema"]),
#             "stats": json.dumps(data["stats"]),
#             "entries": json.dumps(data["truncated_entries"]),
#         }
        
#         print(f"Inserted profile for table: ACTOR with data {data}",  flush=True)
#         client.data_object.create(data_object=profile_data, class_name="TableProfile")
        
#     except Exception as e:
#         print(f"Error inserting data for ACTOR: {e}")

def convert_timestamps(data):
    if isinstance(data, dict):
        return {k: convert_timestamps(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_timestamps(item) for item in data]
    elif isinstance(data, (Timestamp, datetime)):
        return data.isoformat()
    else:
        return data
    
def semantic_search(client, query, collection_name="TableProfile"):
    nearText = {
        "concepts": [query],
        "distance": 0.7,
    }

    properties = [
        "tableName", 
        "schema", 
        "stats",
        "entries",
        "_additional {certainty distance}"
    ]

    result = (
        client.query
        .get(collection_name, properties)
        .with_near_text(nearText)
        .with_limit(10)
        .do()
    )
    
    # Check for errors
    if ("errors" in result):
        raise Exception(result["errors"][0]['message'])
    
    return result["data"]["Get"][collection_name]
    
def keyword_search(client, query, collection_name="TableProfile"):
    properties = [
        "tableName", 
        "schema", 
        "stats",
        "entries",
    ]

    result = (
        client.query
        .get(collection_name, properties)
        .with_bm25(query=query)
        .with_additional("score")
        .with_limit(10)
        .do()
    )
    
    # Check for errors
    if ("errors" in result):
        raise Exception(result["errors"][0]['message'])
    
    return result["data"]["Get"][collection_name]