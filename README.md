# Employee Leave Management System

A Business Analyst portfolio prototype demonstrating requirement-to-solution thinking, workflow, CRUD operations, REST APIs, JSON, validation, and reporting-ready data.

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create and activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start: `python app.py`
6. Open `http://127.0.0.1:5000`.

SQLite database and sample employees are initialized on first run. To reset demo data, stop the app and delete `leave_management.db`; restart it.

## Demo employees

Asha Rao (101), Rahul Kumar (102), Meera Singh (103), Arjun Das (104). Each starts with 8 Casual, 8 Sick, and 12 Earned Leave days.

## API examples

List employees: `GET /api/employees`

List requests: `GET /api/leave-requests` (optional `?status=Pending`)

Create request: `POST /api/leave-requests`, JSON body:
```json
{"employee_id":101,"leave_type":"Casual Leave","start_date":"2026-12-01","end_date":"2026-12-02","reason":"Personal work"}
```

Approve/reject: `PUT /api/leave-requests/1/status`, JSON body:
```json
{"status":"Approved","manager_comment":"Approved"}
```

Health check: `GET /health`.

## Important limitations

This is a learning/demo project, not a production HR system. It intentionally has no login, authorization, audit trail, holiday calendar, half-day handling, or concurrency controls. Add authentication, role-based access, CSRF protection, migrations, and security review before any real use. Dates are counted as calendar days, including weekends.
