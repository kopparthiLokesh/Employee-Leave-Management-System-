# Agile User Stories

- **US-01:** As an employee, I want to submit a leave request so that my manager can review it. Acceptance: required fields validated; valid request becomes Pending.
- **US-02:** As a manager, I want to approve or reject a pending request so that leave decisions are recorded. Acceptance: decision and optional comment are saved; only Pending requests can be decided.
- **US-03:** As an employee, I want leave balances to reflect approved leave so that I can plan future requests. Acceptance: approved days are deducted once; rejected requests do not deduct.
- **US-04:** As HR/Operations, I want a request summary and balances so that I can monitor leave activity. Acceptance: totals and balances match stored records.
- **US-05:** As an integration consumer, I want JSON APIs so that another system can submit and retrieve requests. Acceptance: endpoints return documented JSON and appropriate HTTP status codes.

## Definition of Done
Feature implemented; validation handled; relevant UAT case passes; documentation updated; code committed; known limitations recorded.
