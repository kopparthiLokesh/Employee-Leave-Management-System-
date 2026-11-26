Employee Leave Management System
A simple employee leave management application built with Python, Flask, and SQLite. Employees can submit leave requests, managers can approve or reject them, and users can view leave balances and request summaries.
Features
- Submit and track leave requests
- Approve or reject requests with comments
- Validate dates, leave balances, and overlapping requests
- Track leave balances by leave type
- View request summaries
- JSON-based REST-style API endpoints
Tech Stack
Python · FastAPI · SQL · REST APIs · HTML/CSS · JSON
Setup
pip install -r requirements.txt
python app.py
Open http://127.0.0.1:5000 in your browser.
API Endpoints
Method	Endpoint	Purpose
GET	/health	Health check
GET	/api/employees	List employees and balances
GET	/api/leave-requests	List requests
POST	/api/leave-requests	Submit a request
PUT	/api/leave-requests/<request_id>/status	Approve or reject


Business Rules
- End date must be on or after start date.
- Requests must fit the available leave balance.
- Overlapping active requests are not allowed.
- Approved requests deduct leave; rejected requests do not.
Project Documentation
Supporting BRD, FRD, user stories, RTM, and UAT documents are available in the docs/ folder.
Note
This is a portfolio/demo project. Authentication, production security, notifications, and advanced leave policies are not implemented. Do not use real employee data.
