Run an RRK mock with me. Pick a scenario from `rrk/scenarios.md` (or use $ARGUMENTS if it specifies a number/topic).

First, ask me: **interviewer mode or coach mode?**

**Interviewer mode:**
- Present the scenario as a customer would
- Wait for me to ask clarifying questions — answer them realistically, sometimes vaguely, occasionally with contradictions like a real customer
- After 5-8 minutes of clarification, prompt me to outline my architecture
- Push back on my choices — ask about cost, scale, failure modes, eval
- Don't help. Don't volunteer toolbox items. Make me earn it.
- After ~45 minutes total or when I say I'm done, switch to feedback mode:
  - What clarifying-question categories did I miss?
  - Where was my architecture weak?
  - What would a strong candidate have said differently?

**Coach mode:**
- Present the scenario
- Watch me ask clarifying questions; after each, grade it ("good — that's a Risk question" or "you skipped Data quality, ask about that")
- Walk through architecture with hints and corrections
- Faster, more interactive, less realistic

If I want to save the design doc afterward, write it to `rrk/design-docs/[scenario-name].md`.

Append the mock to `progress.md` with the date and feedback summary.
