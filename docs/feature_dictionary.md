# Feature Dictionary

## Technical Fit Features
### skill_overlap_score
Description:
Percentage overlap between JD skills and candidate skills.
Range:0-100
Weight:High
---

### retrieval_experience_score
Description:
Evidence of retrieval/search systems in work history.
Keywords:retrieval, search, semantic search, vector search
Range:0-100
---
### ranking_experience_score
Description:Evidence of ranking/recommendation systems.
Keywords:ranking, recommendation engine, relevance scoring
Range:0-100
---

## Recruitability Features
### response_rate_score
Source:recruiter_response_rate

Higher is better.
---
### notice_period_score
Source:notice_period_days
Lower is better.
---
### open_to_work_score
Source:open_to_work_flag
Binary:
1 = Yes
0 = No
---

## Activity Features
### activity_score
Derived from:
1. last_active_days
2. applications_submitted_90d
3. recruiter_search_appearances_90d
---

## Trust Features
### credibility_score
Derived from:
1. verified_email
2. verified_phone
3. linkedin_connected
4. profile_completeness
