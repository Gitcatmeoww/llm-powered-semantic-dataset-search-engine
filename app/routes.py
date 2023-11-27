from app import app, db, weaviate_client
from flask import jsonify, render_template, request
from sqlalchemy import text
from .profiler import profile_all_tables, profile_table
from .weaviate_services import insert_profile_data, search_dataset
import openai


@app.route('/')
def index():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """))
            tables = [row[0] for row in result]
        return render_template('index.html', tables=tables)
    except Exception as e:
        return render_template('error.html')

@app.route('/insert_data_to_weaviate')
def insert_profiles():
    # Get the profiled data
    # data = profile_table("actor")
    data = profile_all_tables()

    # Insert the profiled data into Weaviate
    try:
        insert_profile_data(weaviate_client, data)
        return jsonify({"message": "Data insertion into Weaviate successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.json['query']
        result = search_dataset(weaviate_client, query)

        return jsonify({"results": result}), 200
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Below are routes for testing purposes
@app.route('/testdb')
def testdb():
    try:
        # Execute the query using SQLAlchemy session
        result = db.session.execute(text('SELECT * FROM actor LIMIT 1'))
        first_row = result.fetchone()

        # Ensure the row data is serializable
        first_row_data = {column: str(value) for column, value in first_row.items()}

        return jsonify({
            'success': True,
            'first_row': first_row_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/test_profiling')
def test_profiling():
    profiles = profile_table("actor")
    # profiles = profile_all_tables()
    return jsonify(profiles)

@app.route('/weaviate_status')
def weaviate_status():
    try:
        status = weaviate_client.is_ready()
        return f"Weaviate is ready: {status}", 200
    except Exception as e:
        return f"Error checking Weaviate status: {str(e)}", 500

@app.route('/insert_hardcoded_data')
def insert_hardcoded_data():
    try:
        # Hardcoded data
        data = {
            "tableName": "test_table",
            "schema": "Column1: int, Column2: string",
            "stats": "Count: 100, Mean: 50",
            "entries": "Entry1, Entry2"
        }

        # Insert data into Weaviate
        weaviate_client.data_object.create(data_object=data, class_name="TableProfile")
        return jsonify({"message": "Hardcoded data inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verify_weaviate_data')
def verify_weaviate_data():
    query = """
    {
      Get {
        TableProfile {
          _additional { id }
          tableName
          schema
          stats
          entries
        }
      }
    }
    """

    try:
        result = weaviate_client.query.raw(query)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_weaviate_data', methods=['POST'])
def delete_weaviate_data():
    data = request.get_json()
    ids = data.get('ids', [])
    
    try:
        for id in ids:
            weaviate_client.data_object.delete(id, "TableProfile")
            print(f"Deleted object with id: {id}")

        return jsonify({"message": "Deletion successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test-openai-api')
def test_openai_api():
    try:
        openai.api_key = app.config["OPENAI_APIKEY"]

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="This is a test.",
            max_tokens=5
        )

        return jsonify({"message": "OpenAI API key is working", "response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500