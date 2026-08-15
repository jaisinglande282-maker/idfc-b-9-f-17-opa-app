<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IDFC FIRST Bank - Operations Dashboard</title>
  <style>
    :root {
      --primary-color: #9c27b0;
      --secondary-color: #673ab7;
      --bg-color: #f4f6f9;
      --card-bg: #ffffff;
      --text-color: #333;
      --border-color: #e0e0e0;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    body { background-color: var(--bg-color); color: var(--text-color); padding: 20px; }

    .dashboard-container { max-width: 900px; margin: 0 auto; }
    
    /* Header Styling */
    .header-card {
      background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
      color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .header-card h1 { font-size: 1.6rem; margin-bottom: 5px; }
    .header-card p { opacity: 0.9; font-size: 0.9rem; }

    /* Layout Cards */
    .card { background: var(--card-bg); padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); }
    .card-title { font-size: 1.1rem; color: var(--primary-color); margin-bottom: 15px; border-bottom: 2px solid var(--bg-color); padding-bottom: 8px; }

    /* Form Grids */
    .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }

    .form-group { display: flex; flex-direction: column; margin-bottom: 10px; }
    .form-group label { font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; color: #555; }
    .form-group input, .form-group select {
      padding: 10px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.95rem; outline: none; transition: 0.3s;
    }
    .form-group input:focus, .form-group select:focus { border-color: var(--primary-color); }
    .form-group input[readonly] { background-color: #eef2f5; font-weight: bold; }

    /* Buttons */
    .btn-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 10px; }
    .btn {
      padding: 12px 15px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s; font-size: 0.9rem;
    }
    .btn-save { background-color: #28a745; color: white; }
    .btn-save:hover { background-color: #218838; }
    .btn-copy { background-color: #007bff; color: white; }
    .btn-copy:hover { background-color: #0069d9; }

    /* Output Section */
    .preview-box {
      background: #272c34; color: #abb2bf; padding: 15px; border-radius: 8px; font-family: 'Courier New', Courier, monospace;
      white-space: pre-wrap; font-size: 0.9rem; margin-top: 15px; line-height: 1.4; border-left: 4px solid var(--primary-color);
    }
  </style>
</head>
<body>

<div class="dashboard-container">
  
  <!-- App Header -->
  <div class="header-card">
    <h1>IDFC FIRST Bank Operations Dashboard</h1>
    <p>Airoli Gigaplex Building NO-09 | Daily Shift Management System</p>
  </div>

  <!-- Section 1: Control Panel -->
  <div class="card">
    <div class="card-title">General Info</div>
    <div class="grid-3">
      <div class="form-group">
        <label>Date</label>
        <input type="text" id="date" value="13/08/2026">
      </div>
      <div class="form-group">
        <label>Time</label>
        <input type="text" id="time" value="01:30 PM">
      </div>
      <div class="form-group">
        <label>Shift Selection</label>
        <select id="shift">
          <option value="1st Shift">1st Shift</option>
          <option value="2nd Shift">2nd Shift</option>
          <option value="3rd Shift">3rd Shift</option>
          <option value="General Shift">General Shift</option>
          <option value="PTL Shift">PTL Shift</option>
        </select>
      </div>
    </div>
  </div>

  <!-- Section 2: Headcount Details -->
  <div class="card">
    <div class="card-title">1. Headcount Details</div>
    <div class="grid-3">
      <div class="form-group"><label>On Roll Employee</label><input type="number" id="onRoll" value="461" oninput="calcTotal()"></div>
      <div class="form-group"><label>Off Roll Employee</label><input type="number" id="offRoll" value="30" oninput="calcTotal()"></div>
      <div class="form-group"><label>Security Duty</label><input type="number" id="security" value="04" oninput="calcTotal()"></div>
      <div class="form-group"><label>HK Staff Duty</label><input type="number" id="hkStaff" value="09" oninput="calcTotal()"></div>
      <div class="form-group"><label>Technical Staff</label><input type="number" id="technical" value="01" oninput="calcTotal()"></div>
      <div class="form-group"><label>Cafeteria Staff</label><input type="number" id="cafeteria" value="07" oninput="calcTotal()"></div>
    </div>
    <div class="form-group" style="margin-top: 10px;">
      <label>Total Head Count</label>
      <input type="number" id="total" value="512" readonly>
    </div>
  </div>

  <!-- Section 3: Security & Postings -->
  <div class="card">
    <div class="card-title">2. Security & Postings Allocation</div>
    <div class="grid-2">
      <div class="form-group"><label>Reception 01</label><input type="text" id="reception01" value="Pooja J."></div>
      <div class="form-group"><label>Reception 02</label><input type="text" id="reception02" value="Priya S."></div>
      <div class="form-group"><label>PTL Duty</label><input type="text" id="ptlDuty" value="Rahul D."></div>
      <div class="form-group"><label>BMS Operator</label><input type="text" id="bmsOperator" value="Jaysing lande"></div>
    </div>
  </div>

  <!-- Section 4: Parking Duty -->
  <div class="card">
    <div class="card-title">3. Parking Duty Details</div>
    <div class="grid-3">
      <div class="form-group"><label>Parking Duty Staff</label><input type="text" id="parkingStaff" value="Vikram Singh"></div>
      <div class="form-group"><label>Total Vehicles Parked</label><input type="number" id="totalVehicles" value="45"></div>
      <div class="form-group"><label>Available Parking Slots</label><input type="number" id="availableSlots" value="15"></div>
    </div>
    <div class="form-group" style="margin-top: 10px;">
      <label>Updated By</label>
      <input type="text" id="updatedBy" value="Jaysing lande">
    </div>
  </div>

  <!-- Action Bar -->
  <div class="card">
    <div class="card-title">Action & Reports Export</div>
    <div class="btn-grid">
      <button class="btn btn-save" onclick="saveToStorage()">Save Backup (30 Days)</button>
      <button class="btn btn-copy" onclick="copyHeadcount()">Copy Headcount Report</button>
      <button class="btn btn-copy" onclick="copySecurity()">Copy Security Report</button>
      <button class="btn btn-copy" onclick="copyParking()">Copy Parking Report</button>
    </div>
    <div class="preview-box" id="previewArea">Select a report button to view preview...</div>
  </div>

</div>

<script>
  const formatNum = (num) => String(num).padStart(2, '0');

  // Headcount calculation
  function calcTotal() {
    const fields = ['onRoll', 'offRoll', 'security', 'hkStaff', 'technical', 'cafeteria'];
    let total = fields.reduce((sum, id) => sum + (parseInt(document.getElementById(id).value) || 0), 0);
    document.getElementById('total').value = total;
  }

  // Copy Clipboard Logic
  function copyText(msg) {
    navigator.clipboard.writeText(msg);
    document.getElementById('previewArea').innerText = msg;
    alert("Copied to Clipboard!");
  }

  // 1. Headcount Report (Simple Clean Format)
  function copyHeadcount() {
    const msg = `Date:-${document.getElementById('date').value}
Airoli Gigaplex Building NO-09

1] On roll Employee:-${document.getElementById('onRoll').value}
2] Off roll Employee:-${document.getElementById('offRoll').value}
3] Security duty on:-${formatNum(document.getElementById('security').value)}
4] H K staff on duty:-${formatNum(document.getElementById('hkStaff').value)}
5] Technical staff:-${formatNum(document.getElementById('technical').value)}
6] Cafeteria staff:-${formatNum(document.getElementById('cafeteria').value)}
Total head count:-${document.getElementById('total').value}

Regards,
IDFC First bank
Airoli Gigaplex Building NO-09
(${document.getElementById('updatedBy').value})`;

    copyText(msg);
  }

  // 2. Security Duty Report
  function copySecurity() {
    const msg = `Date:-${document.getElementById('date').value}
Time:-${document.getElementById('time').value}
Shift:-${document.getElementById('shift').value}
Airoli Gigaplex Building NO-09

Security Duty Posting:
1] Reception 01:-${document.getElementById('reception01').value}
2] Reception 02:-${document.getElementById('reception02').value}
3] PTL Duty:-${document.getElementById('ptlDuty').value}
4] BMS Operator:-${document.getElementById('bmsOperator').value}
Total Security staff:-${formatNum(document.getElementById('security').value)}

Regards,
IDFC First bank
Airoli Gigaplex Building NO-09
(${document.getElementById('updatedBy').value})`;

    copyText(msg);
  }

  // 3. Parking Report
  function copyParking() {
    const msg = `Date:-${document.getElementById('date').value}
Time:-${document.getElementById('time').value}
Shift:-${document.getElementById('shift').value}
Airoli Gigaplex Building NO-09

Parking Duty Posting:
1] Parking Duty Staff:-${document.getElementById('parkingStaff').value}
2] Total Vehicles Parked:-${document.getElementById('totalVehicles').value}
3] Available Parking Slots:-${document.getElementById('availableSlots').value}

Regards,
IDFC First bank
Airoli Gigaplex Building NO-09
(${document.getElementById('updatedBy').value})`;

    copyText(msg);
  }

  // 1-Month Persistent Data Backup Logic
  function saveToStorage() {
    const record = {
      id: Date.now(),
      date: document.getElementById('date').value,
      time: document.getElementById('time').value,
      shift: document.getElementById('shift').value,
      totalHeadcount: document.getElementById('total').value,
      updatedBy: document.getElementById('updatedBy').value,
      savedAt: new Date().toISOString()
    };

    let history = JSON.parse(localStorage.getItem('idfc_operations_backup')) || [];
    history.push(record);

    // Filter data to retain only last 30 days
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    history = history.filter(item => new Date(item.savedAt) >= thirtyDaysAgo);

    localStorage.setItem('idfc_operations_backup', JSON.stringify(history));
    alert("Data saved successfully in 30-day backup storage!");
  }
</script>

</body>
</html>