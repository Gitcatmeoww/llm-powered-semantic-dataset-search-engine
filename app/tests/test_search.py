import pytest
import requests

# Define test queries
TEST_QUERIES = [
    # Below queries are curated for location-related tables
    {"query": "address"},
    {"query": "location"},
    {"query": "district"},
    {"query": "neighborhood"},
    {"query": "What table should I use if I want to count the number of all addresses"},
    # Below queries are curated for product-related tables
    {"query": "film"},
    {"query": "movie"},
    {"query": "length"},
    {"query": "timespan"},
    {"query": "What table should I use if I want to compare the stock across different shops"},
    # Below queries are curated for transaction-related tables
    {"query": "rental"},
    {"query": "lease"},
    {"query": "payment_date"},
    {"query": "transaction_time"},
    {"query": "partitioned table"},
    {"query": "What table should I use if I want to calculate the average customer rental length"},
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