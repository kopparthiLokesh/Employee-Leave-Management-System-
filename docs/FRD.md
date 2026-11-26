# Functional Requirements Document (FRD)

## Functional behavior
- FR-01: Show employee list and available leave balances.
- FR-02: Request form requires employee, leave type, start date, end date, and reason.
- FR-03: Start date cannot be in the past; end date must be on/after start date.
- FR-04: Requested calendar days cannot exceed the available balance.
- FR-05: A request cannot overlap another non-rejected request for the same employee.
- FR-06: New requests receive Pending status.
- FR-07: Manager can approve/reject a Pending request and optionally enter a comment.
- FR-08: Approval deducts the requested days from the corresponding balance; rejection does not.
- FR-09: Summary cards display total, pending, approved, and rejected counts.
- FR-10: API returns JSON; validation failures return HTTP 400, missing request returns 404, and non-pending decision returns 409.

## Data entities
**Employee:** id, name, department, casual_balance, sick_balance, earned_balance.  
**LeaveRequest:** id, employee_id, leave_type, start_date, end_date, days, reason, status, manager_comment, created_at.

## Use case UC-01: Submit leave request
1. Employee selects employee, leave type, dates, and reason.
2. System validates fields, dates, balance, and overlap.
3. If valid, system stores request as Pending and displays confirmation.
4. If invalid, system displays an actionable error and does not create a request.

## Use case UC-02: Decide leave request
1. Manager reviews a Pending request.
2. Manager chooses Approve or Reject and may add a comment.
3. System verifies request is still Pending.
4. On approval, system checks balance and deducts days; on rejection, balance is unchanged.
5. System stores decision and displays updated status.

## Business rules
- Calendar-day count = end date − start date + 1.
- Leave types: Casual Leave, Sick Leave, Earned Leave.
- Only Pending requests can be decided.
- Rejected requests do not block overlapping future requests.
- Approval deducts balance exactly once.
