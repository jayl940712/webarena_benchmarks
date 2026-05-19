# WebVoyager Date Renderer

`render_webvoyager.py` regenerates `webvoyager.jsonl` from `template/webvoyager.template.jsonl`, updating the dated Booking and Google Flights questions so their dates are in the future.

The renderer only replaces entries whose IDs appear in the template. All other WebVoyager rows are preserved from the base dataset.

## Basic Usage

From `webarena/benchmarks`:

```bash
python3 template/render_webvoyager.py
```

This writes:

- `webvoyager.jsonl`
- `template/update_time.txt`

## Reproducible Date Generation

Use `--today` to make generation deterministic:

```bash
python3 template/render_webvoyager.py --today 2026-05-19
```

`--today` controls the reference date used to generate all future check-in, checkout, departure, and return dates.

## Base Dataset

By default, the script preserves non-templated entries from:

1. `template/webvoyager.base.jsonl`, if that file exists
2. otherwise `HEAD:webvoyager.jsonl` from git

You can pass an explicit base file:

```bash
python3 template/render_webvoyager.py --base /path/to/full_webvoyager.jsonl
```

## Custom Paths

Use a different template:

```bash
python3 template/render_webvoyager.py --template template/webvoyager.template.jsonl
```

Write to a different output:

```bash
python3 template/render_webvoyager.py --output /tmp/webvoyager.jsonl
```

Write update metadata somewhere else:

```bash
python3 template/render_webvoyager.py --update-time-output /tmp/update_time.txt
```

## Update Metadata

`template/update_time.txt` records the generation date and date range used by templated questions:

```text
date_used=2026-05-19
generated_at=2026-05-19T11:14:56-05:00
closest_updated_question_date=2026-06-18
furthest_updated_question_date=2026-10-09
```

## Template Format

Each line in `webvoyager.template.jsonl` is one JSON object with:

- `ques_template`: question text with placeholders such as `{date}`, `{dates}`, `{depart_date}`, or `{return_date}`
- `date_policy`: how far in the future to place the date and how long the stay/trip is
- `render`: how to render each placeholder into natural language

Example:

```json
{"web_name":"Booking","id":"Booking--0","ques_template":"Find a Mexico hotel with deals for {dates}","date_policy":{"type":"hotel_stay","min_days_from_today":30,"duration_days":2},"render":{"dates":"month_day_range"},"web":"https://www.booking.com/"}
```
