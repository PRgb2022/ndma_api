from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",  # Important: avoid 'localhost'
        user="root",
        password="Prajwal.sql@25",
        database="alerts.db"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        severity = request.form.get('severity') or None
        state = request.form.get('state') or None
        area = request.form.get('area') or None

        conn = get_connection()
        cursor = conn.cursor()
        cursor.callproc('filter_alerts_with_totals', [severity, state, area])

        for result in cursor.stored_results():
            results = result.fetchall()

        cursor.close()
        conn.close()

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
