import os
import sqlite3
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- DATABASE SETUP ---
DB_FILE = 'operations.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Daily Headcount Table
    c.execute('''CREATE TABLE IF NOT EXISTS daily_reports 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, on_roll INT, off_roll INT, 
                  sec INT, hk INT, tech INT, cafe INT, total INT, updated_by TEXT)''')
    
    # Parking Table
    c.execute('''CREATE TABLE IF NOT EXISTS parking_logs 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, car_number TEXT, owner TEXT, slot TEXT, photo TEXT, created_at TEXT)''')
    
    # Team Members Table
    c.execute('''CREATE TABLE IF NOT EXISTS team_members 
                 (id INTEGER PRIMARY KEY, name TEXT, role TEXT, status TEXT)''')
    
    # Insert Initial 10 Team Members if empty
    c.execute("SELECT COUNT(*) FROM team_members")
    if c.fetchone()[0] == 0:
        members = [
            (1, "Jaysing Lande", "Supervisor", "On Duty"),
            (2, "Ramesh Kumar", "Security Lead", "On Duty"),
            (3, "Suresh Patil", "HK Supervisor", "On Duty"),
            (4, "Priya Sharma", "Admin Assistant", "Off Duty"),
            (5, "Amit Verma", "Technical Lead", "On Duty"),
            (6, "Vikram Singh", "Security Guard", "On Duty"),
            (7, "Rahul Deshmukh", "HK Staff", "On Duty"),
            (8, "Sneha Kulkarni", "Cafeteria Lead", "On Duty"),
            (9, "Aniket Shinde", "Security Guard", "On Duty"),
            (10, "Pooja Jadhav", "Front Desk", "Off Duty")
        ]
        c.executemany("INSERT INTO team_members VALUES (?,?,?,?)", members)

    conn.commit()
    conn.close()

init_db()

# --- HTML / MOBILE RESPONSIVE UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Airoli Gigaplex - Mobile Operations</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .navbar { background: #075e54; color: white; padding: 12px; font-weight: bold; }
        .card { border-radius: 12px; border: none; box-shadow: 0 2px 6px rgba(0,0,0,0.08); margin-bottom: 15px; }
        .whatsapp-preview { background-color: #efeae2; border-radius: 10px; padding: 12px; font-size: 14px; white-space: pre-wrap; border-left: 4px solid #25d366; }
        .btn-whatsapp { background-color: #25d366; color: white; font-weight: bold; width: 100%; border-radius: 8px; padding: 10px; }
        .nav-pills .nav-link { color: #075e54; font-weight: 600; border-radius: 8px; font-size: 13px; padding: 8px 12px; }
        .nav-pills .nav-link.active { background-color: #075e54; color: white; }
        .status-badge { font-size: 11px; padding: 4px 8px; border-radius: 12px; }
    </style>
</head>
<body>

<div class="navbar sticky-top shadow-sm">
    <i class="fa-solid fa-building-user me-2"></i> IDFC FIRST - Airoli B-09
</div>

<div class="container p-2">
    <!-- Bottom/Top Mobile Navigation Tabs -->
    <ul class="nav nav-pills mb-3 nav-justified bg-white p-1 rounded shadow-sm" id="pills-tab">
        <li class="nav-item"><button class="nav-link active" data-bs-toggle="pill" data-bs-target="#tab-report"><i class="fa-brands fa-whatsapp"></i> Report</button></li>
        <li class="nav-item"><button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-team"><i class="fa-solid fa-users"></i> Team (10)</button></li>
        <li class="nav-item"><button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-parking"><i class="fa-solid fa-car"></i> Parking</button></li>
        <li class="nav-item"><button class="nav-link" data-bs-toggle="pill" data-bs-target="#tab-monthly"><i class="fa-solid fa-list"></i> History</button></li>
    </ul>

    <div class="tab-content">
        <!-- 1. DAILY REPORT -->
        <div class="tab-pane fade show active" id="tab-report">
            <div class="card p-3">
                <h6 class="text-success fw-bold"><i class="fa-solid fa-pen-to-square me-1"></i> Update Headcount</h6>
                <div class="row g-2">
                    <div class="col-6"><label class="small">Date</label><input type="text" id="repDate" class="form-control form-control-sm" value="{{ current_date }}"></div>
                    <div class="col-6"><label class="small">Updated By</label><input type="text" id="updatedBy" class="form-control form-control-sm" placeholder="Your Name"></div>
                    <div class="col-6"><label class="small">On-Roll</label><input type="number" id="onRoll" class="form-control form-control-sm" value="461" oninput="updatePreview()"></div>
                    <div class="col-6"><label class="small">Off-Roll</label><input type="number" id="offRoll" class="form-control form-control-sm" value="30" oninput="updatePreview()"></div>
                    <div class="col-6"><label class="small">Security</label><input type="number" id="secDuty" class="form-control form-control-sm" value="4" oninput="updatePreview()"></div>
                    <div class="col-6"><label class="small">HK Staff</label><input type="number" id="hkDuty" class="form-control form-control-sm" value="9" oninput="updatePreview()"></div>
                    <div class="col-6"><label class="small">Technical</label><input type="number" id="techStaff" class="form-control form-control-sm" value="1" oninput="updatePreview()"></div>
                    <div class="col-6"><label class="small">Cafeteria</label><input type="number" id="cafeStaff" class="form-control form-control-sm" value="7" oninput="updatePreview()"></div>
                </div>
                <button type="button" onclick="saveRecord()" class="btn btn-primary btn-sm mt-3 fw-bold"><i class="fa-solid fa-cloud-arrow-up me-1"></i> Save & Sync to All Mobiles</button>
            </div>

            <div class="card p-3">
                <h6 class="text-success fw-bold"><i class="fa-brands fa-whatsapp me-1"></i> WhatsApp Message Preview</h6>
                <div class="whatsapp-preview" id="whatsappMsg"></div>
                <button onclick="copyToClipboard()" class="btn btn-whatsapp mt-2"><i class="fa-regular fa-copy me-1"></i> Copy WhatsApp Message</button>
            </div>
        </div>

        <!-- 2. TEAM MANAGEMENT -->
        <div class="tab-pane fade" id="tab-team">
            <div class="card p-3">
                <h6 class="fw-bold"><i class="fa-solid fa-users me-1"></i> Operations Team Status</h6>
                <div id="teamList" class="list-group list-group-flush small">
                    <!-- Live Sync Team Data -->
                </div>
            </div>
        </div>

        <!-- 3. CAR PARKING LOG -->
        <div class="tab-pane fade" id="tab-parking">
            <div class="card p-3">
                <h6 class="fw-bold"><i class="fa-solid fa-square-parking me-1"></i> Add Parking Log</h6>
                <form action="/api/add_parking" method="POST" enctype="multipart/form-data">
                    <input type="text" name="car_number" placeholder="Car Number (MH 04 AB 1234)" class="form-control form-control-sm mb-2" required>
                    <input type="text" name="owner" placeholder="Owner Name / Emp ID" class="form-control form-control-sm mb-2" required>
                    <input type="text" name="slot" placeholder="Slot No (e.g. P-12)" class="form-control form-control-sm mb-2" required>
                    <label class="small text-muted">Take or Choose Car Photo:</label>
                    <input type="file" name="car_photo" class="form-control form-control-sm mb-2" accept="image/*" capture="environment" required>
                    <button type="submit" class="btn btn-success btn-sm w-100 fw-bold">Upload & Save Parking</button>
                </form>
            </div>
            <div class="card p-3">
                <h6 class="fw-bold"><i class="fa-solid fa-list me-1"></i> Today's Parked Cars</h6>
                <div id="parkingList"></div>
            </div>
        </div>

        <!-- 4. MONTHLY RECORDS -->
        <div class="tab-pane fade" id="tab-monthly">
            <div class="card p-2">
                <h6 class="fw-bold p-2"><i class="fa-solid fa-database me-1"></i> Saved Monthly Logs</h6>
                <div class="table-responsive">
                    <table class="table table-sm table-striped small">
                        <thead class="table-dark">
                            <tr><th>Date</th><th>By</th><th>Total</th></tr>
                        </thead>
                        <tbody id="historyTable"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    function updatePreview() {
        let dt = document.getElementById('repDate').value;
        let by = document.getElementById('updatedBy').value || 'Jaysing Lande';
        let on = parseInt(document.getElementById('onRoll').value) || 0;
        let off = parseInt(document.getElementById('offRoll').value) || 0;
        let sec = parseInt(document.getElementById('secDuty').value) || 0;
        let hk = parseInt(document.getElementById('hkDuty').value) || 0;
        let tech = parseInt(document.getElementById('techStaff').value) || 0;
        let cafe = parseInt(document.getElementById('cafeStaff').value) || 0;
        let total = on + off + sec + hk + tech + cafe;

        let msg = `📅 *Date:* ${dt}\n📍 *Location:* IDFC FIRST Bank, Airoli Gigaplex B-09\n\n📊 *DAILY HEADCOUNT REPORT*\n\n1️⃣ *On roll Employee:* ${on}\n2️⃣ *Off roll Employee:* ${off}\n3️⃣ *Security duty on:* ${sec.toString().padStart(2, '0')}\n4️⃣ *H K staff on duty:* ${hk.toString().padStart(2, '0')}\n5️⃣ *Technical staff:* ${tech.toString().padStart(2, '0')}\n6️⃣ *Cafeteria staff:* ${cafe.toString().padStart(2, '0')}\n\n📈 *Total headcount:* *${total}*\n\n_Regards,_\n*IDFC FIRST Bank*\nAiroli Gigaplex Building NO-09\n*(${by})*`;

        document.getElementById('whatsappMsg').innerText = msg;
    }

    function copyToClipboard() {
        let text = document.getElementById('whatsappMsg').innerText;
        navigator.clipboard.writeText(text);
        alert('Copied! WhatsApp par paste karein.');
    }

    function saveRecord() {
        let payload = {
            dt: document.getElementById('repDate').value,
            by: document.getElementById('updatedBy').value || 'Jaysing Lande',
            on: parseInt(document.getElementById('onRoll').value) || 0,
            off: parseInt(document.getElementById('offRoll').value) || 0,
            sec: parseInt(document.getElementById('secDuty').value) || 0,
            hk: parseInt(document.getElementById('hkDuty').value) || 0,
            tech: parseInt(document.getElementById('techStaff').value) || 0,
            cafe: parseInt(document.getElementById('cafeStaff').value) || 0,
            total: (parseInt(document.getElementById('onRoll').value)||0) + (parseInt(document.getElementById('offRoll').value)||0) + (parseInt(document.getElementById('secDuty').value)||0) + (parseInt(document.getElementById('hkDuty').value)||0) + (parseInt(document.getElementById('techStaff').value)||0) + (parseInt(document.getElementById('cafeStaff').value)||0)
        };

        fetch('/api/save_report', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        }).then(r => r.json()).then(data => {
            alert('Saved & Sync Successful!');
            fetchData();
        });
    }

    function fetchData() {
        fetch('/api/get_data').then(r => r.json()).then(data => {
            // Render History
            let hHtml = '';
            data.reports.forEach(r => {
                hHtml += `<tr><td>${r[1]}</td><td>${r[9]}</td><td><strong>${r[8]}</strong></td></tr>`;
            });
            document.getElementById('historyTable').innerHTML = hHtml;

            // Render Team
            let tHtml = '';
            data.team.forEach(t => {
                let badgeClass = t[3] === 'On Duty' ? 'bg-success' : 'bg-secondary';
                tHtml += `<div class="list-group-item d-flex justify-content-between align-items-center">
                    <div><strong>${t[1]}</strong><br><span class="text-muted small">${t[2]}</span></div>
                    <span class="badge ${badgeClass} status-badge">${t[3]}</span>
                </div>`;
            });
            document.getElementById('teamList').innerHTML = tHtml;

            // Render Parking
            let pHtml = '';
            data.parking.forEach(p => {
                pHtml += `<div class="d-flex align-items-center mb-2 p-2 border rounded">
                    <img src="${p[4]}" width="60" height="45" style="object-fit:cover;" class="rounded me-2">
                    <div>
                        <strong class="text-primary">${p[1]}</strong> (${p[3]})<br>
                        <small class="text-muted">${p[2]}</small>
                    </div>
                </div>`;
            });
            document.getElementById('parkingList').innerHTML = pHtml || '<small class="text-muted">No Parking Logged</small>';
        });
    }

    // Auto Refresh Every 4 Seconds for Real-time Team Sync
    setInterval(fetchData, 4000);
    fetchData();
    updatePreview();
</script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/")
def home():
    curr_date = datetime.now().strftime("%d/%m/%Y")
    return render_template_string(HTML_TEMPLATE, current_date=curr_date)

@app.route("/api/save_report", methods=["POST"])
def save_report():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO daily_reports (dt, on_roll, off_roll, sec, hk, tech, cafe, total, updated_by) VALUES (?,?,?,?,?,?,?,?,?)",
              (data['dt'], data['on'], data['off'], data['sec'], data['hk'], data['tech'], data['cafe'], data['total'], data['by']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/api/get_data", methods=["GET"])
def get_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM daily_reports ORDER BY id DESC")
    reports = c.fetchall()
    c.execute("SELECT * FROM team_members")
    team = c.fetchall()
    c.execute("SELECT * FROM parking_logs ORDER BY id DESC")
    parking = c.fetchall()
    conn.close()
    return jsonify({"reports": reports, "team": team, "parking": parking})

@app.route("/api/add_parking", methods=["POST"])
def add_parking():
    car_num = request.form.get("car_number")
    owner = request.form.get("owner")
    slot = request.form.get("slot")
    photo = request.files.get("car_photo")

    if photo:
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)
        photo_url = f"/static/uploads/{filename}"
    else:
        photo_url = ""

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO parking_logs (car_number, owner, slot, photo, created_at) VALUES (?,?,?,?,?)",
              (car_num, owner, slot, photo_url, datetime.now().strftime("%d/%m/%Y %H:%M")))
    conn.commit()
    conn.close()
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)