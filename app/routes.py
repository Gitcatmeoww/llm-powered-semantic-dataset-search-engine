from app import app, db
from flask import jsonify, render_template
from sqlalchemy import text
from .profiler import profile_table, profile_all_tables


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
    profiles = profile_all_tables()
    return jsonify(profiles)