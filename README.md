# Employee Leave Management System

<img width="1898" height="859" alt="Screenshot (1024)" src="https://github.com/user-attachments/assets/c354d6be-82ad-4b75-b953-4a0ceb258ed4" />


A beginner-friendly employee leave management web app built with **Python, Flask, and SQLite**. Employees can submit leave requests, and a manager can approve or reject them. The app also provides REST API endpoints that use JSON.

## Features

- View demo employees and leave balances.
- Submit Casual, Sick, or Earned Leave requests.
- Validate dates, available leave balance, and overlapping requests.
- Approve or reject pending requests with a manager comment.
- View request counts by status.
- Use REST API endpoints to retrieve and update leave data.
- Store data in a local SQLite database.

## Tech Stack

- Python
- FastAI
- SQ
- HTML and CSS
- REST APIs and JSON

## Project Structure

```text
leave_management/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── docs/
│   ├── BRD.md
│   ├── FRD.md
│   ├── USER_STORIES.md
│   └── RTM_UAT.md
└── README.md
```

## Requirements

- Python 3.10 or newer
- pip

## Setup and Run

### 1. Download or extract the project

Open a terminal in the `leave_management` folder.

### 2. Create a virtual environment (recommended)

**Windows**

```bash
py -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

### 5. Open the application

Visit:

http://127.0.0.1:5000

The SQLite database and demo employees are created automatically when the app starts.

## Demo Employees

| Employee ID | Name | Department |
|---|---|---|
| 101 | Asha Rao | Operations |
| 102 | Rahul Kumar | Engineering |
| 103 | Meera Singh | Finance |
| 104 | Arjun Das | Sales |

Each demo employee starts with:

- 8 Casual Leave days
- 8 Sick Leave days
- 12 Earned Leave days

## Using the App

1. Select an employee.
2. Enter the leave type, start date, end date, and reason.
3. Submit the request. It will be created with **Pending** status.
4. Use the manager controls to approve or reject the request.
5. Add a manager comment if required.
6. Review the request list and status summary.

Leave duration is calculated in calendar days, including weekends.

## REST API

The API is available while the Flask application is running.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check whether the app is running |
| GET | `/api/employees` | Get employees and current leave balances |
| GET | `/api/leave-requests` | Get all leave requests |
| GET | `/api/leave-requests?status=Pending` | Get requests with a selected status |
| POST | `/api/leave-requests` | Create a leave request |
| PUT | `/api/leave-requests/<request_id>/status` | Approve or reject a request |

### Example: Create a Leave Request

Send a `POST` request to:

`/api/leave-requests`

Request body:

```json
{
  "employee_id": 101,
  "leave_type": "Casual Leave",
  "start_date": "2026-12-01",
  "end_date": "2026-12-02",
  "reason": "Personal work"
}
```

Valid leave types:

- Casual Leave
- Sick Leave
- Earned Leave

Dates must use the `YYYY-MM-DD` format.

### Example: Approve or Reject a Request

Send a `PUT` request to:

`/api/leave-requests/1/status`

Request body:

```json
{
  "status": "Approved",
  "manager_comment": "Approved"
}
```

Use `Approved` or `Rejected` as the status.

You can test these endpoints using Postman or another API client.

For JSON requests, set the following header:

`Content-Type: application/json`

## Business Rules

- Required fields must be provided.
- The start date cannot be in the past.
- The end date cannot be before the start date.
- The request must use a supported leave type and an existing employee.
- Requested leave days cannot exceed the available balance.
- A request cannot overlap another non-rejected request for the same employee.
- Only pending requests can be approved or rejected.
- Leave balance is deducted when a request is approved.

## Project Documentation

The `docs/` folder contains:

- `BRD.md` — Business Requirements Document
- `FRD.md` — Functional Requirements Document
- `USER_STORIES.md` — User Stories
- `RTM_UAT.md` — Requirement Traceability Matrix and UAT material

## Limitations

This is a learning and portfolio project, not a production HR system.

The application does not include:

- Login or secure role-based authorization
- Audit history
- Holiday calendars
- Half-day leave
- Concurrency controls

The manager actions are demonstration functionality, not secure access control.

Before real-world use, add authentication and authorization, CSRF protection, secure configuration, database migrations, automated tests, and a security review.

## License

No license is specified. Add a license file if you plan to distribute the project.
