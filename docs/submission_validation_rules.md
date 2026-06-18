# Submission Validation Rules

## Purpose:Validate submission before final upload.


## Candidate Count Check
Requirement:
* Exactly 100 candidates must be submitted.

Failure:
* Less than 100 candidates
* More than 100 candidates

## Unique Candidate Check
Requirement:
* Every candidate_id must be unique.

Failure:
* Duplicate candidate IDs

## Rank Check
Requirement: Ranks must be sequential.

Example:
1
2
3
...
100

Failure: Missing ranks and duplicate ranks

## Score Ordering Check
Requirement:Higher ranked candidates must have scores greater than or equal to lower ranked candidates.

Example:Rank 1 Score ≥ Rank 2 Score ≥ Rank 3 Score

Failure:Rank order inconsistent with score order

## Explanation Check
Requirement:
Each candidate must have:
* Selection reason
* Supporting evidence
* Recruitability insight (if applicable)

Failure:
* Empty explanation
* Generic explanation

## Honeypot Check
Requirement: Flagged high-risk candidates should not appear in top ranks without justification.

Failure:Honeypot candidates in top positions

## Final Validation Checklist
Before Submission:
1. 100 candidates
2. Unique candidate IDs
3. Sequential ranks
4. Correct score ordering
5. Explanations present
6. No obvious honeypots
7. CSV format validated
