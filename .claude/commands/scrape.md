Scrape top-asked LeetCode problems for a FAANG company and write a ranked file.

Run the following command, using $ARGUMENTS as the company slug (e.g. `google`, `amazon`, `meta`, `apple`, `netflix`):

```bash
venv/bin/python scripts/scrape_company.py $ARGUMENTS
```

After the command completes, report:
1. How many problems were written to `leetcode/$ARGUMENTS-tagged.md`
2. Which sources succeeded and which failed
3. The top 10 problems by score from the output file
