# Requirement Traceability Matrix and UAT

| Requirement | Feature/API | UAT ID |
|---|---|---|
| BR-01 | Request form / POST API | UAT-01 |
| BR-02 | Request validation | UAT-02, UAT-03, UAT-04 |
| BR-03 | Decision form / PUT API | UAT-05, UAT-06 |
| BR-04 | Balance deduction | UAT-05, UAT-07 |
| BR-05 | Request list / GET API | UAT-08 |
| BR-06 | Summary and balances | UAT-09 |
| BR-07 | JSON endpoints | UAT-10 |

## UAT test cases

| ID | Scenario | Steps / Test data | Expected result |
|---|---|---|---|
| UAT-01 | Valid request | Employee 101, Casual, future 2-day range, reason | Request created as Pending; days=2 |
| UAT-02 | Missing required field | Submit without reason | Validation error; no record created |
| UAT-03 | Invalid date range | End date before start date | Validation error |
| UAT-04 | Insufficient balance | Request more days than available | Validation error; no record created |
| UAT-05 | Approve pending request | Approve a valid pending request | Status Approved; matching balance reduced once |
| UAT-06 | Reject pending request | Reject a valid pending request | Status Rejected; balance unchanged |
| UAT-07 | Decide twice | Attempt decision after approval | Conflict/error; no second deduction |
| UAT-08 | Retrieve requests | GET request list | JSON list includes saved requests/status |
| UAT-09 | Dashboard totals | Create requests in multiple statuses | Counts match database records |
| UAT-10 | API validation | POST malformed/missing JSON fields | HTTP 400 with error message |
