# Business Requirements Document (BRD)

**Project:** Employee Leave Management System  
**Version:** 1.0 | **Status:** Portfolio prototype

## 1. Business problem
Leave requests managed through email or spreadsheets can be difficult to track, approve consistently, and report. The organization needs a central process for submitting, reviewing, and tracking employee leave.

## 2. Business objective
Provide a simple centralized workflow that records requests, supports manager decisions, tracks balances, and exposes data for reporting.

## 3. Stakeholders
- Employees: submit and track requests.
- Managers: review, approve, or reject requests.
- HR/Operations: maintain employee leave balances and monitor trends.
- Project team: analyze, build, test, and support the solution.

## 4. Scope
**In scope:** employee selection, leave request submission, validation, pending/approved/rejected status, manager comment, balance deduction on approval, request list, summary counts, REST endpoints.

**Out of scope:** authentication, payroll integration, public holiday calendar, half-day leave, email notifications, mobile app, production deployment.

## 5. Business requirements
- BR-01: Employees can submit a leave request with type, date range, and reason.
- BR-02: The system validates required fields, date order, balance, and overlapping requests.
- BR-03: Managers can approve or reject pending requests and add a comment.
- BR-04: Approved requests deduct the relevant leave balance once.
- BR-05: Users can view requests and their status.
- BR-06: HR/Operations can view request counts and employee balances.
- BR-07: The system provides JSON endpoints for request creation, retrieval, and decision updates.

## 6. Assumptions and constraints
Demo employees and opening balances are seeded. Leave days are calendar days. Only pending requests may be decided. Prototype is local and has no access control.

## 7. Success criteria
All defined UAT cases pass; valid requests are recorded; invalid/overlapping/over-balance requests are rejected; approval updates status and balance; dashboard counts reflect stored requests.
