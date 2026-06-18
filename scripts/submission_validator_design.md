# Submission Validator Design
## Inputs
* submission.csv
## Checks

### Check 1
Candidate Count
Expected:100

### Check 2
Unique Candidate IDs
Expected:No duplicates

### Check 3
Rank Sequence
Expected:1 to 100

### Check 4
Score Monotonicity
Expected:score(rank n) >= score(rank n+1)

### Check 5
Explanation Presence
Expected:Every candidate has explanation text.

## Output
Validation Report
Example: PASS-->
* Candidate Count
* Unique IDs
* Rank Sequence

FAIL if 
* Duplicate Candidate ID
* Missing Explanation
