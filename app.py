from flask import Flask, render_template, request, jsonify
import mysql.connector
from db_config import db_config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-alerts', methods=['POST'])
def get_alerts():
    data = request.get_json()
    input_severity = data.get('severity')
    input_state = data.get('state')
    input_area = data.get('district')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('filter_alerts_with_totals', (input_severity, input_state, input_area))

    results = []
    for result in cursor.stored_results():
        results = result.fetchall()

    cursor.close()
    conn.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
