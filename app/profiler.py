from app import db
import pandas as pd
from sqlalchemy import text


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

# Aggregate metadata for a given table
def profile_table(table_name):
    schema = get_table_schema(table_name)
    stats = get_column_stats(table_name)
    
    # Combine all metadata into a single dictionary
    metadata = {
        'schema': schema,
        'stats': stats,
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