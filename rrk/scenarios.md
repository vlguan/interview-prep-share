# RRK Practice Scenarios

10 system design scenarios in the FDE style. Each one tests: clarifying questions, workflow mapping, architecture (tools/RAG/context), trade-offs, eval, and rollout.

Strike through when you've done a full design doc.

## Scenarios

### 1. Healthcare triage
A hospital has an EMR with patient records, an internal medical knowledge base, and a scheduling system. Nurses currently triage incoming patient calls by looking up history, cross-referencing symptoms, and booking appointments or escalating. How would you optimize with an AI agent?

### 2. Legal contract review
A law firm has a contract management system, a precedent database of redlined past contracts, and Outlook. Associates currently review incoming contracts by pulling similar past contracts, flagging problematic clauses, drafting redlines, and emailing them back. How would you optimize?

### 3. Loan underwriting
A regional bank has a loan origination system, an internal credit policy doc repository, and external credit bureau APIs. Underwriters currently pull applicant data, cross-reference policy and credit reports, and write a decision memo. How would you build an agent?

### 4. Insurance claims
An insurance company has a claims management system, a fraud detection dashboard, and a document repository of past claims. Adjusters currently review new claims by checking similar past cases, running fraud signals, and writing decision letters. Design the agent.

### 5. Recruiting
A recruiting firm has an ATS, LinkedIn Recruiter, and a CRM tracking past candidate touchpoints. Recruiters currently source by searching LinkedIn, checking the ATS, reviewing CRM for warm relationships, and drafting personalized outreach. How would you optimize?

### 6. E-commerce support
An e-commerce company has an order management system, a help center knowledge base, and a returns processing system. Support agents handle tickets by looking up orders, finding relevant help articles, processing returns, and replying to customers. How would an agent help?

### 7. B2B sales / QBR prep
A SaaS company has Salesforce, a product analytics dashboard showing customer feature usage, and a content library of case studies. AEs prep for QBRs by pulling usage data, finding relevant case studies, and writing customized slide decks per client. Optimize this.

### 8. Investment research
An investment firm has an internal research database, Bloomberg, and a CRM. Analysts build investment theses by querying market data, pulling related past research, and writing memos. How would you design an agent?

### 9. IT managed services
An MSP has a ticketing system, a KB of past incidents, and customer infrastructure monitoring dashboards. L1 engineers triage tickets by reading alerts, searching for similar past incidents, and resolving or escalating. Design the workflow.

### 10. Editorial / content production
A media company has a CMS, content analytics showing which articles drive traffic, and a competitive intel tool. Editors brainstorm topics by reviewing performance data, checking competitor coverage, and pitching ideas in weekly editorial meetings. How would you optimize?

---

## Original scenario (from friend's interview)
Advertising company with internal market trend UI (impressions, keywords), Google Drive of past client docs, and CRM. Account managers cross-reference data and email client updates. How would you optimize using an AI agent?
