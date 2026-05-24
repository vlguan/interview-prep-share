# RRK Frameworks Reference

Quick reference for RRK rounds. Don't memorize this verbatim — internalize the categories so you can ask the right questions under pressure.

## The seven clarifying question categories

> **USERS → PAIN → DATA → SCALE → RISK → SUCCESS → ROLLOUT**

Hit each category with at least one question. Time-box clarification to 5-8 minutes in a 45-min round.

### Users
- Who's the actual user — customer, employee, both?
- Walk me through what that person does today, step by step.
- How technical are they?
- Who else touches this workflow?

### Pain
- What's the cost of the status quo?
- Is the pain efficiency, quality, consistency, or coverage?
- What's tried and failed before?
- What's the headline number they want to move?

### Data
- What systems hold the data? APIs available?
- How fresh — real-time, hourly, daily?
- Structured or unstructured?
- Quality issues — duplicates, contradictions, missing fields?
- PII / PHI / regulated?

### Scale
- How many users / clients / records / tasks per day?
- Growth trajectory?
- Distribution — 80/20 or even spread?
- Peak vs average?

### Risk
- What's the worst case if it's wrong?
- Human-in-the-loop acceptable? At what stage?
- Reversibility?
- Acceptable error rate?

### Success
- What's the single metric for success?
- Baseline to compare against?
- Golden set of good outputs?
- How would we detect failure in prod?

### Rollout
- What's the MVP?
- Phased rollout (canary, shadow)?
- Who owns it after launch?
- Timeline?

---

## Architecture decision: tools vs RAG vs context

| Data type | Use |
|-----------|-----|
| Structured (DBs, APIs, dashboards) | Tool calls — agent queries on demand |
| Unstructured (docs, emails, transcripts) | RAG with embeddings |
| Small static refs (system prompt, schema) | In context |

**The trap:** putting everything through RAG. Numbers and structured data should come from tools, not embedded text.

---

## Cost levers

- **Model tiering** — cheap filter ("is this interesting?") → expensive writer. 10x savings typical.
- **Prompt caching** — cached input ~10-25% of normal price.
- **Batch APIs** — ~50% off for non-realtime.
- **Output budgets** — set `max_tokens` aggressively.
- **Prompt compression** — trim few-shot examples.
- **RAG over context stuffing** — retrieve 500 tokens, not 50K.
- **Self-host** — at very high volume.

### Pricing tiers to memorize (2026)
- Small: ~$0.10-0.50 / M input, $0.50-2 / M output
- Mid: ~$1-3 / M input, $5-15 / M output
- Frontier: ~$3-15 / M input, $15-75 / M output
- Output is ~3-5x more expensive than input on every provider
- 1 token ≈ ¾ word ≈ 4 chars

---

## Safety levers (especially for autonomous systems)

- **Grounding / citation** — every claim must trace to a tool call result
- **Confidence routing** — uncertain cases go to human queue, not autonomous send
- **Prompt injection defense** — sanitize/sandbox all retrieved content as untrusted
- **Brand/tone guardrails** — LLM-as-judge against rubric, reject and retry
- **Reversibility & kill switch** — global pause, per-entity opt-out, quarantine first-send
- **Audit trail** — every action logs inputs, tool calls, draft, final
- **Anomaly detection** — pre-action rule checks (PII leaks, profanity, contradictions)
- **Compliance** — CAN-SPAM, GDPR, HIPAA, sector-specific

---

## State management

For any recurring workflow (hourly, scheduled, triggered), persist per-entity state:
- Last action taken
- Last data snapshot
- Diff against current state determines whether to act

### Storage choices
- **Postgres** — structured, queryable by many dimensions
- **Redis** — hot cache, sub-ms reads, ephemeral
- **Object storage** (S3, GCS) — large blobs, write-once, cheap archive
- **Vector DB** (pgvector, Pinecone) — semantic similarity search, RAG

Common pattern: Postgres for hot recent state + S3 for cold archive.

---

## Eval strategy

- **Offline eval suite** — curated input/output pairs, deterministic checks, end-state checks, trajectory checks
- **LLM-as-judge** — for subjective quality; calibrate against human labels first
- **Simulation / sandbox** — fake versions of external systems with seeded state
- **Shadow mode** — new agent runs in parallel with old on real traffic, compare logs
- **Canary rollout** — 1% → 10% → 100%
- **Regression testing** — eval set runs on every prompt/model change
- **Production monitoring** — track per-category success, not just averages

---

## The framing move when constraints get hard

When the interviewer adds aggressive constraints ("hourly + fully autonomous + 10K clients"), don't just accept. Push back diplomatically:

> "That's technically possible, but I'd want to validate the assumption. At hourly frequency, most cases won't have material updates — so we'd really be designing a *significance detector* that emits maybe 1-2 actions per entity per week, with hourly *evaluation* under the hood. Does that match the customer's actual need?"

The interviewer wants to see that you'd push back on a real customer, not become a yes-man.

---

## Red flags to avoid

- Jumping into architecture before asking clarifying questions
- Putting everything through RAG (especially structured data)
- Designing for "fully autonomous from day 1" without phased rollout
- Skipping eval strategy
- Not mentioning cost
- Silent coding / silent designing — say it out loud
