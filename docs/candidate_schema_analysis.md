# Candidate Schema Analysis

## Core Candidate Structure

Each candidate profile contains:

1. candidate_id
2. profile
3. career_history
4. education
5. skills
6. redrob_signals

---

## Profile Features

- Headline
- Summary
- Location
- Country
- Years of Experience
- Current Title
- Current Company
- Company Size
- Industry

Purpose:
Used for relevance matching against Job Description.

---

## Career History Features

- Company
- Title
- Duration
- Industry
- Company Size
- Description

Purpose:
Used for experience verification and title matching.

---

## Education Features

- Institution
- Degree
- Field of Study
- Tier

Purpose:
Secondary relevance signal.

---

## Skills Features

- Skill Name
- Proficiency
- Endorsements
- Duration

Purpose:
Primary technical relevance signal.

---

## Redrob Signals

Behavioral and recruiter engagement signals.

Includes:

- Open To Work
- Last Active Date
- Recruiter Response Rate
- Notice Period
- Interview Completion Rate
- Offer Acceptance Rate
- GitHub Activity
- Search Appearance
- Saved By Recruiters
- Profile Completeness

Purpose:
Recruitability scoring.