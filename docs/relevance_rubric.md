# Relevance Rubric

## Final Ranking Formula
Final Score =
Technical Fit +
Recruitability +
Activity +
Trust
---

## Technical Fit (50%)
Purpose:
Can the candidate successfully perform the job?

Signals:
### Core Skills (20%)
- Retrieval Systems
- Ranking Systems
- Recommendation Systems
- Embeddings
- Vector Databases
### Experience Relevance (15%)
- Years of ML Experience
- Years of AI Engineering Experience
- Production System Experience
### Career Evidence (10%)
- Projects mentioned in work history
- Search systems
- Recommendation engines
- Candidate matching systems
### Company Background (5%)
- Product companies preferred
- Startups with shipped products


## Recruitability (25%)
Purpose:Can we realistically hire this candidate?
Signals:
### Response Behaviour (10%)
- recruiter_response_rate
- avg_response_time_hours
### Hiring Success Signals (10%)
- interview_completion_rate
- offer_acceptance_rate
### Availability (5%)
- open_to_work_flag
- notice_period_days
---


## Activity (15%)
Purpose:Is the candidate currently active and discoverable?
Signals:
### Platform Activity
- last_active_days
### Engagement
- applications_submitted_90d
- recruiter_search_appearances_90d
### Recruiter Interest
- saved_by_recruiters_count
- profile_views_90d
---

## Trust (10%)
Purpose:Can we trust the profile information?
Signals:
### Verification
- verified_email
- verified_phone
- linkedin_connected
### Profile Quality
- profile_completeness_score
### Consistency
- Skills supported by experience
- Timeline consistency
---

## Penalties
### Skill Inflation (-15)
Trigger:Many advanced skills listed
but little or no evidence in work history.

Example:
Skills:
- LLM
- GAN
- NLP
- Computer Vision
- Speech AI

Experience:
Backend Engineer

Penalty:
-15


### Inactive Candidate (-10)
Trigger:No recent activity for extended period.

Example:
last_active_days > 180

Penalty:
-10

### Impossible Career Timeline (-30)
Trigger:Career timeline impossible.

Examples:
- Experience before graduation
- Company joined before company existed
- 12 years experience at age 24

Penalty:
-30

### Contradictory Profile (-15)
Trigger:Headline, skills, and work history disagree.

Example:
Headline:
Backend Engineer

Skills:
GANs
Speech AI
Computer Vision

Work History:
ETL Pipelines Only

Penalty:
-15


## Tie Breaking Rules
When two candidates have equal scores:
1. Higher Technical Fit wins
2. Higher Recruitability wins
3. More recent activity wins
4. Candidate ID ascending