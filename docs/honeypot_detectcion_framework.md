# Honeypot Detection Framework

## Purpose
Identify candidates who appear highly relevant but contain inconsistencies,
inflated skills, unrealistic timelines, or misleading behavioral signals.
---

## Detection Categories
1. Skill Inflation
2. Timeline Anomalies
3. Profile Contradictions
4. Activity Mismatch
5. Behavioral Outliers
6. Duplicate / Near-Duplicate Profiles
---

### 1. Skill Inflation Detection
Purpose:Detect candidates listing many advanced skills without supporting evidence.
Checks:
- Count advanced skills
- Compare against projects
- Compare against work history

Red Flags:
- More than 15 advanced AI skills
- No matching project evidence
- No matching work experience

Penalty:-15

### 2. Timeline Anomaly Detection
Purpose:Detect impossible career progression.
Checks:
- Total experience consistency
- Education dates
- Employment dates

Red Flags:
- Experience before graduation
- Overlapping full-time jobs
- Unrealistic experience duration

Penalty:-30

### 3. Profile Contradiction Detection
Purpose:Detect inconsistencies across profile sections.
Checks:
- Headline vs Skills
- Skills vs Experience
- Summary vs Work History

Example: Headline-Backend Engineer
Skills:GANs, Speech AI, Computer Vision
Work History:Only ETL/Data Pipelines
Penalty:-15

### 4. Activity Mismatch Detection
Purpose:Detect candidates who appear strong but are unlikely to engage.
Checks:
- Last active date
- Response rate
- Interview completion

Red Flags:
- Active profile but near-zero responses
- High search appearances but no engagement

Penalty:-10

### 5. Behavioral Outlier Detection
Purpose:Detect unusual recruiter behavior patterns.
Checks:
- Extremely low response rate
- Extremely high response delay
- Very low offer acceptance

Penalty:-10

### 6. Duplicate / Near-Duplicate Detection
Purpose:Detect candidates with highly similar profiles that may distort rankings.
Checks:
- Similar skills
- Similar work history
- Similar education records
- Similar behavioral signals

Penalty:-5


## Candidate Risk Meter
Low Risk
- Consistent profile
- Strong evidence

Medium Risk
- Minor inconsistencies

High Risk
- Skill inflation
- Timeline anomalies
- Contradictions

## Candidate Credibility Score
100 = Fully trustworthy
Calculated from:
- Profile consistency
- Verification signals
- Timeline checks
- Skill evidence

## Honeypot Confidence Levels
Low Confidence:
- Single minor inconsistency

Medium Confidence:
- Multiple inconsistencies

High Confidence:
- Impossible timeline
- Severe skill inflation
- Major contradictions