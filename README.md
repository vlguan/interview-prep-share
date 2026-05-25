# FDE Interview Prep

Workspace for prepping the Google Forward Deployed Engineer interview (2026-06-15).

## How to use this repo

This repo is designed to work with [Claude Code](https://docs.claude.com/en/docs/claude-code/overview). The `CLAUDE.md` at the root tells Claude how to behave when you open a session here — defaulting to rubber-duck mode, never writing solutions for you, and tracking progress.

### Setup

1. Install Claude Code:
   ```bash
   # macOS / Linux (native installer, no Node.js needed)
   curl -fsSL https://claude.ai/install.sh | bash

   # Windows (PowerShell as admin)
   irm https://claude.ai/install.ps1 | iex
   ```

2. From this repo's root, run:
   ```bash
   claude
   ```
   Claude Code will auto-load `CLAUDE.md` on every session.

### Daily session pattern

- Open Claude Code in this repo: `claude`
- Use a slash command to start: `/drill graphs`, `/rrk`, `/redo`
- Code in `leetcode/solved/`; Claude reviews via Socratic questioning
- Update `progress.md` and `toolbox.md` yourself — they're sacred

## Directory layout

```
.
├── CLAUDE.md              # Claude's instructions for this repo
├── toolbox.md             # My personal reference doc (in my own words)
├── progress.md            # Log of what I've done
├── leetcode/
│   ├── todo.md            # Problem queue
│   ├── redo-queue.md      # Spaced repetition
│   └── solved/            # My solutions
├── rrk/
│   ├── scenarios.md       # System design scenarios
│   ├── frameworks.md      # RRK reference material
│   └── design-docs/       # My 1-page design docs
├── mocks/                 # Mock interview notes
└── .claude/
    └── commands/          # Custom slash commands
```

## Slash commands

- `/drill [pattern]` — pick a problem from todo.md (optionally filtered by pattern), rubber duck through it
- `/review [filepath]` — review a solution via Socratic questioning, don't rewrite
- `/rrk [scenario]` — run an RRK mock (Claude plays interviewer or coach)
- `/redo` — surface a problem from the redo queue that's due
- `/scrape [company]` — scrape top-asked LeetCode problems for a company and write a ranked list to `leetcode/<company>-tagged.md`

## Scrape setup

The `/scrape` command pulls company-tagged problems from GitHub, LeetCode Discuss, and LintCode, then ranks them by frequency. It requires a Python venv with a headless browser for the LeetCode Discuss source.

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/playwright install
```

Then use it via Claude Code:

```
/scrape google
```

Or run directly:

```bash
venv/bin/python scripts/scrape_company.py google
```

Output is written to `leetcode/google-tagged.md` (or whichever company slug you pass).
