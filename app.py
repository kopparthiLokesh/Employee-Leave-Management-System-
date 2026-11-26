from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'leave_management.db'
app = Flask(__name__)
app.secret_key = 'change-this-development-secret'

LEAVE_TYPES = ['Casual Leave', 'Sick Leave', 'Earned Leave']
STATUSES = ['Pending', 'Approved', 'Rejected']


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    with db() as con:
        con.executescript('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            casual_balance INTEGER NOT NULL DEFAULT 8,
            sick_balance INTEGER NOT NULL DEFAULT 8,
            earned_balance INTEGER NOT NULL DEFAULT 12
        );
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL REFERENCES employees(id),
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            days INTEGER NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            manager_comment TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        count = con.execute('SELECT COUNT(*) FROM employees').fetchone()[0]
        if count == 0:
            con.executemany('INSERT INTO employees(id,name,department) VALUES(?,?,?)', [
                (101, 'Asha Rao', 'Operations'), (102, 'Rahul Kumar', 'Engineering'),
                (103, 'Meera Singh', 'Finance'), (104, 'Arjun Das', 'Sales')])


def row_dict(row):
    return dict(row) if row else None


def get_balance(employee, leave_type):
    return {'Casual Leave': employee['casual_balance'], 'Sick Leave': employee['sick_balance'],
            'Earned Leave': employee['earned_balance']}[leave_type]


def validate_request(data):
    required = ['employee_id', 'leave_type', 'start_date', 'end_date', 'reason']
    missing = [field for field in required if not str(data.get(field, '')).strip()]
    if missing:
        return 'Missing required fields: ' + ', '.join(missing)
    if data['leave_type'] not in LEAVE_TYPES:
        return 'Invalid leave type.'
    try:
        start = date.fromisoformat(data['start_date'])
        end = date.fromisoformat(data['end_date'])
        employee_id = int(data['employee_id'])
    except (ValueError, TypeError):
        return 'Dates must be YYYY-MM-DD and employee_id must be an integer.'
    if start < date.today():
        return 'Start date cannot be in the past.'
    if end < start:
        return 'End date cannot be before start date.'
    if not data['reason'].strip():
        return 'Reason is required.'
    with db() as con:
        employee = con.execute('SELECT * FROM employees WHERE id=?', (employee_id,)).fetchone()
        if not employee:
            return 'Employee not found.'
        days = (end - start).days + 1
        if days > get_balance(employee, data['leave_type']):
            return f'Insufficient {data["leave_type"]} balance. Available: {get_balance(employee, data["leave_type"])} day(s).'
        overlap = con.execute('''SELECT id FROM leave_requests WHERE employee_id=? AND status!='Rejected'
          AND NOT(end_date < ? OR start_date > ?)''', (employee_id, start.isoformat(), end.isoformat())).fetchone()
        if overlap:
            return 'This request overlaps an existing non-rejected leave request.'
    return None


@app.route('/')
def index():
    with db() as con:
        employees = con.execute('SELECT * FROM employees ORDER BY name').fetchall()
        requests = con.execute('''SELECT lr.*, e.name employee_name, e.department FROM leave_requests lr
          JOIN employees e ON e.id=lr.employee_id ORDER BY lr.created_at DESC, lr.id DESC''').fetchall()
        stats = {
            'total': con.execute('SELECT COUNT(*) FROM leave_requests').fetchone()[0],
            'pending': con.execute("SELECT COUNT(*) FROM leave_requests WHERE status='Pending'").fetchone()[0],
            'approved': con.execute("SELECT COUNT(*) FROM leave_requests WHERE status='Approved'").fetchone()[0],
            'rejected': con.execute("SELECT COUNT(*) FROM leave_requests WHERE status='Rejected'").fetchone()[0],
        }
    return render_template('index.html', employees=employees, requests=requests, stats=stats, leave_types=LEAVE_TYPES, today=date.today().isoformat())


@app.post('/leave-requests')
def create_request():
    data = request.form.to_dict()
    error = validate_request(data)
    if error:
        flash(error, 'danger')
        return redirect(url_for('index'))
    days = (date.fromisoformat(data['end_date']) - date.fromisoformat(data['start_date'])).days + 1
    with db() as con:
        con.execute('''INSERT INTO leave_requests(employee_id,leave_type,start_date,end_date,days,reason)
          VALUES(?,?,?,?,?,?)''', (int(data['employee_id']), data['leave_type'], data['start_date'], data['end_date'], days, data['reason'].strip()))
    flash('Leave request submitted successfully.', 'success')
    return redirect(url_for('index'))


@app.post('/leave-requests/<int:request_id>/decision')
def decide_request(request_id):
    status = request.form.get('status')
    comment = request.form.get('manager_comment', '').strip()
    if status not in ['Approved', 'Rejected']:
        flash('Invalid decision.', 'danger')
        return redirect(url_for('index'))
    with db() as con:
        req = con.execute('SELECT * FROM leave_requests WHERE id=?', (request_id,)).fetchone()
        if not req:
            flash('Request not found.', 'danger')
        elif req['status'] != 'Pending':
            flash('Only pending requests can be changed.', 'warning')
        else:
            if status == 'Approved':
                col = {'Casual Leave':'casual_balance', 'Sick Leave':'sick_balance', 'Earned Leave':'earned_balance'}[req['leave_type']]
                employee = con.execute(f'SELECT {col} FROM employees WHERE id=?', (req['employee_id'],)).fetchone()
                if employee[col] < req['days']:
                    flash('Insufficient balance at approval time.', 'danger')
                    return redirect(url_for('index'))
                con.execute(f'UPDATE employees SET {col}={col}-? WHERE id=?', (req['days'], req['employee_id']))
            con.execute('UPDATE leave_requests SET status=?, manager_comment=? WHERE id=?', (status, comment, request_id))
            flash(f'Request {status.lower()}.', 'success')
    return redirect(url_for('index'))


@app.get('/api/employees')
def api_employees():
    with db() as con:
        rows = con.execute('SELECT id,name,department,casual_balance,sick_balance,earned_balance FROM employees ORDER BY id').fetchall()
    return jsonify([dict(r) for r in rows])


@app.get('/api/leave-requests')
def api_requests():
    status = request.args.get('status')
    query = '''SELECT lr.*,e.name employee_name,e.department FROM leave_requests lr
               JOIN employees e ON e.id=lr.employee_id'''
    params = ()
    if status:
        if status not in STATUSES:
            return jsonify({'error': 'status must be Pending, Approved, or Rejected'}), 400
        query += ' WHERE lr.status=?'
        params = (status,)
    query += ' ORDER BY lr.created_at DESC,lr.id DESC'
    with db() as con:
        rows = con.execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])


@app.post('/api/leave-requests')
def api_create_request():
    data = request.get_json(silent=True) or {}
    error = validate_request(data)
    if error:
        return jsonify({'error': error}), 400
    days = (date.fromisoformat(data['end_date']) - date.fromisoformat(data['start_date'])).days + 1
    with db() as con:
        cur = con.execute('''INSERT INTO leave_requests(employee_id,leave_type,start_date,end_date,days,reason)
          VALUES(?,?,?,?,?,?)''', (int(data['employee_id']), data['leave_type'], data['start_date'], data['end_date'], days, data['reason'].strip()))
        request_id = cur.lastrowid
    return jsonify({'id': request_id, 'status': 'Pending', 'days': days}), 201


@app.put('/api/leave-requests/<int:request_id>/status')
def api_update_status(request_id):
    data = request.get_json(silent=True) or {}
    status = data.get('status')
    if status not in ['Approved', 'Rejected']:
        return jsonify({'error': 'status must be Approved or Rejected'}), 400
    with db() as con:
        req = con.execute('SELECT * FROM leave_requests WHERE id=?', (request_id,)).fetchone()
        if not req:
            return jsonify({'error': 'Request not found'}), 404
        if req['status'] != 'Pending':
            return jsonify({'error': 'Only pending requests can be changed'}), 409
        if status == 'Approved':
            col = {'Casual Leave':'casual_balance', 'Sick Leave':'sick_balance', 'Earned Leave':'earned_balance'}[req['leave_type']]
            emp = con.execute(f'SELECT {col} FROM employees WHERE id=?', (req['employee_id'],)).fetchone()
            if emp[col] < req['days']:
                return jsonify({'error': 'Insufficient leave balance'}), 409
            con.execute(f'UPDATE employees SET {col}={col}-? WHERE id=?', (req['days'], req['employee_id']))
        con.execute('UPDATE leave_requests SET status=?,manager_comment=? WHERE id=?', (status, data.get('manager_comment',''), request_id))
    return jsonify({'id': request_id, 'status': status})


@app.get('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
