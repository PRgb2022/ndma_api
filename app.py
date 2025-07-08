from flask import Flask, render_template, request, jsonify
import mysql.connector
from db_config import db_config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-alerts', methods=['POST'])
def get_alerts():
    try:
        data = request.get_json()
        severity = data.get('severity')
        state = data.get('state')
        area = data.get('district')

        print("Received from frontend:", severity, state, area) 

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('filter_alerts_with_totals', [severity, state, area])

        results = []
        for result in cursor.stored_results():
            results = result.fetchall()

        print("RESULTS FROM DB:", results) 

        cursor.close()
        conn.close()
        return jsonify(results)

    except Exception as e:
        print("SERVER ERROR:", e)
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
