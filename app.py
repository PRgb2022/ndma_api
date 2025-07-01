from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",       # Replace with Railway DB host if deploying
        user="root",            # Your MySQL username
        password="yourpass",    # Your MySQL password
        database="ndma_alerts"
    )

@app.route('/filter_alerts', methods=['GET'])
def filter_alerts():
    severity = request.args.get('severity') or None
    state = request.args.get('state') or None
    area = request.args.get('area') or None

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.callproc('filter_alerts_with_totals', [severity, state, area])
        results = []
        for result in cursor.stored_results():
            columns = result.column_names
            for row in result.fetchall():
                results.append(dict(zip(columns, row)))
        return jsonify(results)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
