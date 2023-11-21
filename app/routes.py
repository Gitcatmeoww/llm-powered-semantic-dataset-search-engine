from app import app, db
from flask import jsonify
from sqlalchemy import text

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
