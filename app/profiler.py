from app import db
import pandas as pd
from sqlalchemy import text
import base64

# Specify the number of truncated entries in the database
NUM_TRUNCATED_ENTRIES = 2

# Profiling aspect 1: table schema
def get_table_schema(table_name):
    query = text("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = :table_name;
    """)

    with db.engine.connect() as conn:
        result = conn.execute(query, {"table_name": table_name})
        schema = []
        for row in result:
            column_info = {
                'column_name': row[0],
                'data_type': row[1],
                'is_nullable': row[2],
            }
            schema.append(column_info)
    return schema

# Profiling aspect 2: column statistical data
def get_column_stats(table_name):
    with db.engine.connect() as conn:
        df = pd.read_sql_table(table_name, conn)

    # Exclude columns with dtype 'object' which may include binary data
    non_binary_df = df.select_dtypes(exclude=['object'])

    stats = non_binary_df.describe(include='all').transpose().fillna('')
    return stats.to_dict()

# Profiling aspect 3: truncated N entries
def get_truncated_entries(table_name):
    with db.engine.connect() as conn:
        query = f"SELECT * FROM {table_name} LIMIT {NUM_TRUNCATED_ENTRIES};"
        df = pd.read_sql(query, conn)
    
    # Apply the conversion to each cell in the DataFrame
    df = df.applymap(convert_memoryview)

    return df.to_dict(orient='records')

# Helper function to convert memoryview objects to a string format
# Note: the picture column in staff table is a binary type
def convert_memoryview(item):
    if isinstance(item, memoryview):
        return base64.b64encode(item.tobytes()).decode('utf-8')
    return item

# Aggregate metadata for a given table
def profile_table(table_name):
    schema = get_table_schema(table_name)
    stats = get_column_stats(table_name)
    truncated_entries = get_truncated_entries(table_name)
    
    # Combine all metadata into a single dictionary
    metadata = {
        'schema': schema,
        'stats': stats,
        'truncated_entries': truncated_entries,
    }
    
    return metadata

# Profile all tables in the dataset
def profile_all_tables():
    # Exclude the partition tables from profiling
    table_query = text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        AND table_name NOT LIKE 'payment_p%%';
    """)

    with db.engine.connect() as conn:
        result = conn.execute(table_query)
        tables = [row[0] for row in result]

    profiles = {}
    for table_name in tables:
        profiles[table_name] = profile_table(table_name)

    return profiles