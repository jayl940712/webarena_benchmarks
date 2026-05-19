#!/usr/bin/env python3
"""Render WebVoyager date templates into a fresh JSONL benchmark file."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path


MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

ABBR_MONTHS = [
    "Jan.",
    "Feb.",
    "Mar.",
    "Apr.",
    "May",
    "Jun.",
    "Jul.",
    "Aug.",
    "Sep.",
    "Oct.",
    "Nov.",
    "Dec.",
]


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def month_name(d: date) -> str:
    return MONTHS[d.month - 1]


def abbr_month_name(d: date) -> str:
    return ABBR_MONTHS[d.month - 1]


def month_day(d: date) -> str:
    return f"{month_name(d)} {d.day}"


def month_day_ordinal(d: date) -> str:
    return f"{month_name(d)} {ordinal(d.day)}"


def month_day_year(d: date) -> str:
    return f"{month_name(d)} {d.day}, {d.year}"


def month_day_ordinal_year(d: date) -> str:
    return f"{month_name(d)} {ordinal(d.day)}, {d.year}"


def day_month(d: date) -> str:
    return f"{d.day} {month_name(d)}"


def day_month_year(d: date) -> str:
    return f"{d.day} {month_name(d)} {d.year}"


def month_day_range(start: date, end: date) -> str:
    if start.month == end.month and start.year == end.year:
        return f"{month_name(start)} {start.day}-{end.day}"
    return f"{month_day(start)}-{month_day(end)}"


def month_day_range_year(start: date, end: date) -> str:
    if start.month == end.month and start.year == end.year:
        return f"{month_name(start)} {start.day}-{end.day}, {start.year}"
    return f"{month_day_year(start)} - {month_day_year(end)}"


def ordinal_month_day_range(start: date, end: date) -> str:
    if start.month == end.month and start.year == end.year:
        return f"{month_name(start)} {ordinal(start.day)} - {month_name(end)} {ordinal(end.day)}"
    return f"{month_day_ordinal(start)} - {month_day_ordinal(end)}"


def month_day_to_day(start: date, end: date) -> str:
    if start.month == end.month and start.year == end.year:
        return f"{month_name(start)} {start.day} to {end.day}"
    return f"{month_day(start)} to {month_day(end)}"


def month_day_to_day_year(start: date, end: date) -> str:
    if start.month == end.month and start.year == end.year:
        return f"{month_name(start)} {start.day} to {end.day}, {start.year}"
    return f"{month_day_year(start)} to {month_day_year(end)}"


def day_month_range_year(start: date, end: date) -> str:
    if start.month == end.month and start.year == end.year:
        return f"{start.day} {month_name(start)} to {end.day} {month_name(end)} {start.year}"
    return f"{day_month_year(start)} to {day_month_year(end)}"


def numeric_dmy_range(start: date, end: date) -> str:
    return f"{start:%d/%m/%Y} - {end:%d/%m/%Y}"


def sentence_range_year(start: date, end: date) -> str:
    return f"{month_day_year(start)}, to {month_day_year(end)}"


def between_ordinal_range_year(start: date, end: date) -> str:
    return f"{month_day_ordinal_year(start)}, and {month_day_ordinal_year(end)}"


def format_value(style: str, start: date, end: date | None) -> str:
    if style.startswith("end_"):
        if end is None:
            raise ValueError(f"Format {style!r} requires an end date")
        return format_value(style.removeprefix("end_"), end, None)
    if style == "month_day":
        return month_day(start)
    if style == "month_day_ordinal":
        return month_day_ordinal(start)
    if style == "month_day_year":
        return month_day_year(start)
    if style == "month_day_ordinal_year":
        return month_day_ordinal_year(start)
    if style == "abbr_month_day":
        return f"{abbr_month_name(start)} {start.day}"
    if style == "day_month_year":
        return day_month_year(start)
    if end is None:
        raise ValueError(f"Format {style!r} requires an end date")
    if style == "month_day_range":
        return month_day_range(start, end)
    if style == "month_day_range_year":
        return month_day_range_year(start, end)
    if style == "ordinal_month_day_range":
        return ordinal_month_day_range(start, end)
    if style == "month_day_to_day":
        return month_day_to_day(start, end)
    if style == "month_day_to_day_year":
        return month_day_to_day_year(start, end)
    if style == "day_month_range_year":
        return day_month_range_year(start, end)
    if style == "numeric_dmy_range":
        return numeric_dmy_range(start, end)
    if style == "sentence_range_year":
        return sentence_range_year(start, end)
    if style == "between_ordinal_range_year":
        return between_ordinal_range_year(start, end)
    raise ValueError(f"Unknown date render style: {style}")


def style_uses_end_date(style: str) -> bool:
    if style.startswith("end_"):
        return True
    return style in {
        "month_day_range",
        "month_day_range_year",
        "ordinal_month_day_range",
        "month_day_to_day",
        "month_day_to_day_year",
        "day_month_range_year",
        "numeric_dmy_range",
        "sentence_range_year",
        "between_ordinal_range_year",
    }


def parse_today(value: str | None) -> date:
    if value is None:
        return date.today()
    return datetime.strptime(value, "%Y-%m-%d").date()


def entry_dates(today: date, entry_index: int, policy: dict) -> tuple[date, date | None]:
    min_days = int(policy.get("min_days_from_today", 30))
    spread_days = int(policy.get("spread_days", 90))
    duration_days = policy.get("duration_days")

    offset = min_days + ((entry_index * 3) % max(spread_days, 1))
    start = today + timedelta(days=offset)
    end = None if duration_days is None else start + timedelta(days=int(duration_days))

    if start <= today:
        raise ValueError(f"Generated start date {start} is not after {today}")
    if end is not None and end < start:
        raise ValueError(f"Generated end date {end} is before start date {start}")

    return start, end


def render_entry(template_entry: dict, today: date, entry_index: int) -> dict:
    start, end = entry_dates(today, entry_index, template_entry["date_policy"])
    question = template_entry["ques_template"]

    for placeholder, style in template_entry["render"].items():
        value = format_value(style, start, end)
        question = question.replace("{" + placeholder + "}", value)

    if "{" in question or "}" in question:
        raise ValueError(f"Unrendered placeholder in {template_entry['id']}: {question}")

    return {
        "web_name": template_entry["web_name"],
        "id": template_entry["id"],
        "ques": question,
        "web": template_entry["web"],
    }


def rendered_dates(template_entry: dict, today: date, entry_index: int) -> list[date]:
    start, end = entry_dates(today, entry_index, template_entry["date_policy"])
    dates = [start]

    if end is not None and any(style_uses_end_date(style) for style in template_entry["render"].values()):
        dates.append(end)

    return dates


def load_jsonl(path: Path) -> list[dict]:
    return parse_jsonl(path.read_text(encoding="utf-8"), str(path))


def parse_jsonl(text: str, source: str) -> list[dict]:
    entries: list[dict] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on line {line_number} of {source}") from exc
    return entries


def write_jsonl(path: Path, entries: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=True) + "\n")


def write_update_time(path: Path, today: date, dates_used: list[date]) -> None:
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    closest_date = min(dates_used)
    furthest_date = max(dates_used)
    path.write_text(
        f"date_used={today.isoformat()}\n"
        f"generated_at={generated_at}\n"
        f"closest_updated_question_date={closest_date.isoformat()}\n"
        f"furthest_updated_question_date={furthest_date.isoformat()}\n",
        encoding="utf-8",
    )


def load_base_entries(base_path: Path | None, benchmark_dir: Path) -> list[dict]:
    if base_path is not None:
        return load_jsonl(base_path)

    base_template = benchmark_dir / "template" / "webvoyager.base.jsonl"
    if base_template.exists():
        return load_jsonl(base_template)

    try:
        result = subprocess.run(
            ["git", "show", "HEAD:webvoyager.jsonl"],
            cwd=benchmark_dir,
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError(
            "Could not load a base dataset. Pass --base PATH or create "
            "template/webvoyager.base.jsonl."
        ) from exc

    return parse_jsonl(result.stdout, "HEAD:webvoyager.jsonl")


def merge_rendered_entries(base_entries: list[dict], rendered_entries: list[dict]) -> list[dict]:
    rendered_by_id = {entry["id"]: entry for entry in rendered_entries}
    merged_entries: list[dict] = []
    replaced_ids: set[str] = set()

    for entry in base_entries:
        replacement = rendered_by_id.get(entry.get("id"))
        if replacement is None:
            merged_entries.append(entry)
            continue
        merged_entries.append(replacement)
        replaced_ids.add(replacement["id"])

    for entry in rendered_entries:
        if entry["id"] not in replaced_ids:
            merged_entries.append(entry)

    return merged_entries


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    benchmark_dir = script_dir.parent

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--template",
        type=Path,
        default=script_dir / "webvoyager.template.jsonl",
        help="Template JSONL input path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=benchmark_dir / "webvoyager.jsonl",
        help="Generated WebVoyager JSONL output path.",
    )
    parser.add_argument(
        "--base",
        type=Path,
        help=(
            "Full base JSONL to preserve. If omitted, uses "
            "template/webvoyager.base.jsonl when present, otherwise "
            "HEAD:webvoyager.jsonl from git."
        ),
    )
    parser.add_argument(
        "--today",
        help="Override today's date for reproducible generation, formatted as YYYY-MM-DD.",
    )
    parser.add_argument(
        "--update-time-output",
        type=Path,
        default=script_dir / "update_time.txt",
        help="Path for recording the date/time used to generate the output.",
    )
    args = parser.parse_args()

    today = parse_today(args.today)
    base_entries = load_base_entries(args.base, benchmark_dir)
    templates = load_jsonl(args.template)
    rendered = [render_entry(entry, today, index) for index, entry in enumerate(templates)]
    dates_used = [
        used_date
        for index, entry in enumerate(templates)
        for used_date in rendered_dates(entry, today, index)
    ]
    merged = merge_rendered_entries(base_entries, rendered)
    write_jsonl(args.output, merged)
    write_update_time(args.update_time_output, today, dates_used)
    print(f"Wrote {len(merged)} entries to {args.output} ({len(rendered)} templated updates)")
    print(f"Wrote update time to {args.update_time_output}")


if __name__ == "__main__":
    main()
