import pytest
import requests

# Sample test data
TEST_QUERIES = [
    {"query": "film"},
    {"query": "actor"},
]


@pytest.mark.parametrize("test_data", TEST_QUERIES)
def test_keyword_search(test_data):
    response = requests.post(
        "http://127.0.0.1:5000/keyword_search",
        json={"query": "film"}
    )
    assert response.status_code == 200

    data = response.json()
    table_names = [result["tableName"] for result in data["results"]]
    print(f"Query: {test_data['query']}, Response: {table_names}")

    
@pytest.mark.parametrize("test_data", TEST_QUERIES)
def test_semantic_search(test_data):
    response = requests.post(
        "http://127.0.0.1:5000/semantic_search",
        json={"query": test_data['query']}
    )
    assert response.status_code == 200
    
    data = response.json()
    table_names = [result["tableName"] for result in data["results"]]
    print(f"Query: {test_data['query']}, Response: {table_names}")