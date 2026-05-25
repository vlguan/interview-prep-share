#!/usr/bin/env python3
import re
import sys
import csv
import io
import argparse
from datetime import date
from pathlib import Path
from collections import defaultdict
from typing import NamedTuple

import requests


class ScraperResult(NamedTuple):
    scores: dict   # {slug: int} — slug-keyed for all sources
    names: dict    # {slug: str} — problem names keyed by slug
    source: str
    error: str | None


def parse_github_json(data: list) -> dict:
    """Parse hxu296 GitHub JSON into {id: (name, score)}. Kept for backward compat."""
    result = {}
    for item in data:
        if "id" not in item:
            continue
        name = item.get("name", f"Problem #{item['id']}")
        score = int(item.get("frequency", 1))
        result[item["id"]] = (name, score)
    return result


def parse_github_csv(csv_text: str) -> dict:
    """Parse hxu296 company CSV into {slug: (name, count)}."""
    result = {}
    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        link = row.get('problem_link', '')
        name = row.get('problem_name', '').strip()
        try:
            count = int(row.get('num_occur') or 1)
        except (ValueError, TypeError):
            count = 1
        m = re.search(r'/problems/([\w-]+)/', link)
        if m and name:
            result[m.group(1)] = (name, count)
    return result


def parse_lintcode_api(data: dict) -> dict:
    """Parse LintCode API response into {slug: count}."""
    counts = {}
    for problem in data.get('problems', []):
        slug = problem.get('unique_name', '')
        if slug:
            counts[slug] = counts.get(slug, 0) + 1
    return counts


def extract_ids_from_discuss_html(html: str) -> dict:
    """Return {slug: count} from LeetCode Discuss HTML."""
    counts: dict[str, int] = defaultdict(int)
    for m in re.finditer(r'/problems/([\w-]+)/', html):
        counts[m.group(1)] += 1
    return dict(counts)


def extract_ids_from_lintcode_html(html: str) -> dict:
    """Return {slug: count} from LintCode HTML (kept for testing)."""
    counts: dict[str, int] = defaultdict(int)
    for m in re.finditer(r'/problem/([\w-]+)/', html):
        slug = m.group(1)
        if slug and slug != "problem":
            counts[slug] += 1
    return dict(counts)


def build_slug_to_id_from_csv(csv_text: str) -> dict:
    """Build {slug: int_id} from leetcode_problems.csv using Java solution URLs."""
    mapping = {}
    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        link = row.get('link', '')
        solution = row.get('solution', '')
        slug_m = re.search(r'/problems/([\w-]+)/', link)
        id_m = re.search(r'_(\d+)\.java', solution)
        if slug_m and id_m:
            mapping[slug_m.group(1)] = int(id_m.group(1))
    return mapping


def aggregate(results: list, slug_to_id: dict) -> list:
    """
    Merge ScraperResults into sorted [(display_id, name, score)] list.
    slug_to_id: {slug: int} for resolving slugs to numeric LeetCode IDs.
    display_id is int when resolved, else the slug string.
    """
    totals: dict = defaultdict(int)
    slug_names: dict[str, str] = {}

    for r in results:
        if r.error:
            continue
        for key, score in r.scores.items():
            slug = str(key)
            totals[slug] += score
            if slug not in slug_names and slug in r.names:
                slug_names[slug] = r.names[slug]

    ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    result = []
    for slug, score in ranked:
        display_id = slug_to_id.get(slug, slug)
        name = slug_names.get(slug, slug.replace('-', ' ').title())
        result.append((display_id, name, score))
    return result


def format_markdown(company: str, ranked: list, failed_sources: list, scraped_date: str) -> str:
    lines = [
        f"# {company.title()} — Top Asked LeetCode Problems",
        f"_Scraped {scraped_date} · sources: github/hxu296, leetcode-discuss, lintcode_",
    ]
    if failed_sources:
        lines.append(f"_Failed sources: {', '.join(failed_sources)}_")
    lines += [
        "",
        "| Rank | # | Problem | Score |",
        "|------|---|---------|-------|",
    ]
    for rank, (pid, name, score) in enumerate(ranked, 1):
        lines.append(f"| {rank} | {pid} | {name} | {score} |")
    return "\n".join(lines) + "\n"


# --- Network fetchers (side-effectful, not unit-tested) ---

def fetch_github(company: str) -> ScraperResult:
    company_title = company.title()
    url = f"https://raw.githubusercontent.com/hxu296/leetcode-company-wise-problems-2022/main/companies/{company_title}.csv"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 404:
            return ScraperResult(scores={}, names={}, source="github", error=None)
        resp.raise_for_status()
        parsed = parse_github_csv(resp.text)
        scores = {slug: count for slug, (_, count) in parsed.items()}
        names = {slug: name for slug, (name, _) in parsed.items()}
        return ScraperResult(scores=scores, names=names, source="github", error=None)
    except Exception as e:
        return ScraperResult(scores={}, names={}, source="github", error=str(e))


def fetch_leetcode_discuss(company: str) -> ScraperResult:
    try:
        from scrapling.fetchers import DynamicFetcher
        fetcher = DynamicFetcher()
        slug_counts: dict[str, int] = defaultdict(int)
        for page_num in range(1, 4):
            url = (
                f"https://leetcode.com/discuss/interview-question"
                f"?currentPage={page_num}&orderBy=hot&query={company}"
            )
            page = fetcher.fetch(url, wait=2000)
            extracted = extract_ids_from_discuss_html(page.html_content)
            for slug, count in extracted.items():
                slug_counts[slug] += count
        return ScraperResult(scores=dict(slug_counts), names={}, source="discuss", error=None)
    except Exception as e:
        return ScraperResult(scores={}, names={}, source="discuss", error=str(e))


def fetch_lintcode(company: str) -> ScraperResult:
    """Fetch company problems from LintCode JSON API."""
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
    slug_counts: dict[str, int] = defaultdict(int)
    try:
        for page in range(1, 4):  # first 3 pages = 150 problems
            url = f"https://www.lintcode.com/api/problems/?company={company}&limit=50&page={page}"
            resp = requests.get(url, timeout=10, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            page_counts = parse_lintcode_api(data)
            for slug, count in page_counts.items():
                slug_counts[slug] += count
            if page >= data.get('maximum_page', 1):
                break
        return ScraperResult(scores=dict(slug_counts), names={}, source="lintcode", error=None)
    except Exception as e:
        return ScraperResult(scores={}, names={}, source="lintcode", error=str(e))


def fetch_slug_to_id() -> dict:
    """Fetch slug→LeetCode ID mapping from hxu296 leetcode_problems.csv."""
    url = "https://raw.githubusercontent.com/hxu296/leetcode-company-wise-problems-2022/main/data/leetcode_problems.csv"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return build_slug_to_id_from_csv(resp.text)
    except Exception:
        return {}


def main():
    parser = argparse.ArgumentParser(description="Scrape top LeetCode problems for a company")
    parser.add_argument("company", help="Company slug, e.g. google, amazon, meta")
    parser.add_argument("--output-dir", default="leetcode", help="Directory for output file")
    args = parser.parse_args()

    company = args.company.lower()
    print(f"Scraping {company}...")

    github = fetch_github(company)
    if github.error:
        print(f"  github: FAILED — {github.error}")
    else:
        print(f"  github: {len(github.scores)} problems")

    discuss = fetch_leetcode_discuss(company)
    if discuss.error:
        print(f"  leetcode-discuss: FAILED — {discuss.error}")
    else:
        print(f"  leetcode-discuss: {len(discuss.scores)} slug mentions")

    lintcode = fetch_lintcode(company)
    if lintcode.error:
        print(f"  lintcode: FAILED — {lintcode.error}")
    else:
        print(f"  lintcode: {len(lintcode.scores)} slug mentions")

    print("  building slug→ID map...")
    slug_to_id = fetch_slug_to_id()
    ranked = aggregate([github, discuss, lintcode], slug_to_id=slug_to_id)

    failed = [r.source for r in [github, discuss, lintcode] if r.error]
    md = format_markdown(company, ranked, failed_sources=failed, scraped_date=str(date.today()))

    output_path = Path(args.output_dir) / f"{company}-tagged.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md)
    print(f"\nWrote {len(ranked)} problems to {output_path}")

    if not ranked:
        sys.exit(1)


if __name__ == "__main__":
    main()
