Find problems in `leetcode/redo-queue.md` that are due.

A problem is due if today's date is >= the 3-day redo date or the 7-day redo date (and the corresponding redo hasn't been marked done).

Steps:
1. Read `leetcode/redo-queue.md`
2. List 2-3 problems that are due. If none are due, say so and suggest I move on to a new problem instead.
3. Pick the oldest due problem.
4. Tell me only the LC number and name — don't show my prior solution.
5. Wait for me to re-solve from scratch.
6. After I solve it: mark that redo as `done` in `redo-queue.md`. If it was the 3-day, schedule a 7-day. If it was the 7-day, the problem is "learned" — move it out of the queue into a "Learned" section.
7. If I can't solve it from scratch: mark as "failed" and put it back at the start of the cycle (today + 3 days).
