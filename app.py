import sqlite3
from datetime import datetime
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('operations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emp_master (
            emp_id TEXT PRIMARY KEY,
            emp_name TEXT,
            emp_mobile TEXT,
            drop_location TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cab_master (
            cab_no TEXT PRIMARY KEY,
            driver_name TEXT,
            driver_mobile TEXT,
            seater_capacity TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cab_drop_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cab_no TEXT,
            seater_capacity TEXT,
            driver_name TEXT,
            driver_mobile TEXT,
            guard_name TEXT,
            pickup_time TEXT,
            staff_details TEXT,
            date_added TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get_emp/<emp_id>', methods=['GET'])
def get_emp(emp_id):
    conn = sqlite3.connect('operations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT emp_name, emp_mobile, drop_location FROM emp_master WHERE emp_id = ?", (emp_id.upper().strip(),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"found": True, "name": row[0], "mobile": row[1], "location": row[2]})
    return jsonify({"found": False})

@app.route('/api/get_cab/<cab_no>', methods=['GET'])
def get_cab(cab_no):
    conn = sqlite3.connect('operations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT driver_name, driver_mobile, seater_capacity FROM cab_master WHERE cab_no = ?", (cab_no.upper().strip(),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"found": True, "driver_name": row[0], "driver_mobile": row[1], "seater_capacity": row[2]})
    return jsonify({"found": False})

@app.route('/api/add_cab_log', methods=['POST'])
def add_cab_log():
    data = request.json
    cab_no = data.get('cab_no', '').upper().strip()
    seater = data.get('seater_capacity', '4-Seater')
    driver_name = data.get('driver_name', '').strip()
    driver_mobile = data.get('driver_mobile', '').strip()
    guard_name = data.get('guard_name', '').strip()
    pickup_time = data.get('pickup_time', '').strip()
    staff_list = data.get('staff_list', [])
    today_date = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect('operations.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO cab_master (cab_no, driver_name, driver_mobile, seater_capacity)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(cab_no) DO UPDATE SET driver_name=?, driver_mobile=?, seater_capacity=?
    ''', (cab_no, driver_name, driver_mobile, seater, driver_name, driver_mobile, seater))

    for emp in staff_list:
        if emp.get('id'):
            cursor.execute('''
                INSERT INTO emp_master (emp_id, emp_name, emp_mobile, drop_location)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(emp_id) DO UPDATE SET emp_name=?, emp_mobile=?, drop_location=?
            ''', (emp['id'].upper().strip(), emp['name'], emp['mobile'], emp['location'], emp['name'], emp['mobile'], emp['location']))

    staff_str = " | ".join([f"[{e['id']}] {e['name']} ({e['mobile']}) -> {e['location']}" for e in staff_list if e.get('id')])

    cursor.execute('''
        INSERT INTO cab_drop_logs (cab_no, seater_capacity, driver_name, driver_mobile, guard_name, pickup_time, staff_details, date_added)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (cab_no, seater, driver_name, driver_mobile, guard_name, pickup_time, staff_str, today_date))
    
    conn.commit()

    cursor.execute("SELECT date_added, cab_no, seater_capacity, driver_name, driver_mobile, guard_name, pickup_time, staff_details FROM cab_drop_logs WHERE date_added = ? ORDER BY id DESC", (today_date,))
    logs = cursor.fetchall()
    conn.close()

    return jsonify({"status": "success", "logs": logs})

@app.route('/api/search_cab_logs', methods=['GET'])
def search_cab_logs():
    search_date = request.args.get('date', '')
    conn = sqlite3.connect('operations.db')
    cursor = conn.cursor()
    if search_date:
        cursor.execute("SELECT date_added, cab_no, seater_capacity, driver_name, driver_mobile, guard_name, pickup_time, staff_details FROM cab_drop_logs WHERE date_added = ? ORDER BY id DESC", (search_date,))
    else:
        cursor.execute("SELECT date_added, cab_no, seater_capacity, driver_name, driver_mobile, guard_name, pickup_time, staff_details FROM cab_drop_logs ORDER BY id DESC LIMIT 100")
    logs = cursor.fetchall()
    conn.close()
    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
