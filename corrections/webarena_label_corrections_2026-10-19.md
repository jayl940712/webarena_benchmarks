# WebArena label corrections (2026-10-19)

This change fixes the reference labels of 36 tasks in `webarena.jsonl` (40 fields: 18 answer checks, 4 URL checks, 18 page checks). All other lines are byte-identical. The full old and new values are in `webarena_label_corrections_2026-10-19.tsv`.

## How the errors were found and checked

- Candidates: tasks that strong agents fail although the page shows the correct result.
- Each correction was checked against the site pages (screenshots of agent runs on a freshly reset instance), the task text in this file, WebArena-Verified 1.2.3, and WebArena's own later data file (`test.raw.json`, shipped with WebArena-Verified).
- Separate reviewers then tried to disprove each correction. All 36 hold. For task 323 the review replaced our first new value with 264.49 (two of the March 2022 orders were canceled); this is also the value in `test.raw.json` and WebArena-Verified.
- The site data match the official images (orders, totals, SKUs, forum names), so these are label errors, not environment differences.

## Two causes

1. **The original label is wrong (19 tasks):** 11, 33, 34, 50, 68, 80, 81, 110, 111, 178, 184, 323, 438, 493, 536, 659, 660, 780, 782. Examples: wrong counts or dates (110/111: April has 7 orders; the raw annotation in this file also says 7), a wrong base price (780: 84 + 17 = 101, label 64), a 23% cut checked for a 23% raise (782), a wrong user (536), a URL that a correct run can never reach (660). For 11, 33, 34, 80, 81, 110, 111 and 323, WebArena's own later `test.raw.json` already has the corrected value.
2. **Task text and label do not match (17 tasks):** 62, 63, 64, 65, 116, 185, 288, 444, 464, 591, 592, 594, 603, 608, 615, 617, 638. This file uses WebArena-Verified's rewritten task text but keeps the original label. Examples: the text asks for emails and the label holds names (62-65, 288); the text names the Connecticut / news forum and the check still wants /f/earthporn (615, 617); "(inclusive)" was added to the text but not to the due dates (591, 592, 594); the typo "budge" was fixed in the text but not in the check (603, 608).

## Please check

- Lower confidence: 65 (medium-low: "fifth most" can mean the 5th-highest order count or the customer in 5th place), 64 and 185 (medium), 33, 63, 81, 178, 184, 323 (medium-high). All others: high.
- Not changed (conflicting evidence): 28, 32, 51, 142, 147, 179, 443, 736, 804.
- This file still differs from WebArena's `test.raw.json` in other labels (53 answers, 37 URLs, 65 page checks). Many of those are deliberate (added alternatives, looser matching), so this change does not adopt them.

## Effect

On our real-site reads, each model's score moves by -1 to +14 tasks out of 812; no ranking changes. The 14 page-check fixes can only be scored by a new run.

## Changed fields

| task | check | old | new | confidence |
|---|---|---|---|---|
| 11 | string_match | ["4"] | ["6"] | high |
| 33 | string_match | ["DoubleTree by Hilton Hotel Pittsburgh Airport", "1.9km"] | ["DoubleTree by Hilton Hotel Pittsburgh Airport", "1.4km"] | medium-high |
| 34 | string_match | ["Time: 3h 38min"] | ["Time: 3h 30min"] | high |
| 50 | string_match | ["24 orders", "$6560.69 total spend"] | ["21 orders", "$6560.69 total spend"] | high |
| 62 | string_match | ["Jane Smith"] | ["janesmith456@yahoo.com"] | high |
| 63 | string_match | ["Adam Garcia", "Michael Nguyen", "Sarah Miller"] | ["helloworld@yahoo.com", "michael.nguyen@yahoo.com"] | medium-high |
| 64 | string_match | ["Lisa Kim", "Lisa Green", "Julia Williams", "Brian Smith", "Alexan... | ["musiclover99@hotmail.com", "roni_cost@example.com"] | medium |
| 65 | string_match | ["Jane Doe"] | ["adam.garcia@gmail.com", "jason.miller@yahoo.com", "jennifer.white... | medium-low |
| 68 | string_match | ["A Christmas Carol", "Levar Burton", "The Hobbit", "J. R. R. Tolki... | ["A Christmas Carol", "The Hobbit", "Tolkien"] | high |
| 80 | string_match | ["42 min"] | ["38 min"] | high |
| 81 | string_match | ["43 min"] | ["49 min"] | medium-high |
| 110 | string_match | ["January: 11 orders", "Feburary: 16 orders", "March: 14 orders", "... | ["January: 11 orders", "Feburary: 16 orders", "March: 14 orders", "... | high |
| 111 | string_match | ["Feburary: 16 orders", "March: 14 orders", "April: 8 orders", "May... | ["Feburary: 16 orders", "March: 14 orders", "April: 7 orders", "May... | high |
| 116 | string_match | ["Alexander", "Carma", "Dominic", "Merrie", "Monroe", "Scotty", "Sh... | ["Dominic", "Trey", "Edmund", "Merrie", "Shaunte", "Teofila", "Carm... | high |
| 178 | url_match | __GITLAB__/a11yproject/a11yproject.com/-/issues/566 | __GITLAB__/a11yproject/a11yproject.com/-/issues/1057 | medium-high |
| 184 | string_match | Sinbad Fitness Tank | Cronus Yoga Pant -33-Blue | medium-high |
| 185 | string_match | ["Eos", "Minerva"] | ["Cotton", "Fleece"] | medium |
| 288 | string_match | Samantha Jones | coolcat321@hotmail.com | high |
| 323 | string_match | ["97.9"] | ["264.49"] | medium-high |
| 438 | program_html | ["B08PVHRRB7"] | ["B017SK5E3M"] | high |
| 444 | program_html | __GITLAB__/byteblaze/gimmiethat.space/-/raw/main/index.html | __GITLAB__/byteblaze/gimmiethat.space/-/raw/title-update/index.html | high |
| 464 | program_html | ["This is in regular rotation at the gym", "Its colorful and looks ... | ["1 customer(s) love it!"] | high |
| 493 | program_html | __SHOPPING_ADMIN__/sales/order/view/order_id/307/ | __SHOPPING_ADMIN__/sales/order/view/order_id/65/ | high |
| 536 | program_html | ["@lahwaacz", "@R1kk3r", "@abisubramanya27"] | ["@ghost", "@R1kk3r", "@abisubramanya27"] | high |
| 591 | program_html | ["Feb 5, 2030"] | ["Feb 4, 2030"] | high |
| 592 | program_html | ["Mar 8, 2030"] | ["Mar 7, 2030"] | high |
| 594 | program_html | ["May 21, 2044"] | ["May 20, 2044"] | high |
| 603 | program_html | ["safe and budge apartment to live in nyc"] | ["safe and budget apartment to live in nyc"] | high |
| 608 | program_html | ["safe and budge apartment to live"] | ["safe and budget apartment to live"] | high |
| 615 | url_match | __REDDIT__/f/earthporn | __REDDIT__/f/Connecticut | high |
| 617 | url_match | __REDDIT__/f/earthporn | __REDDIT__/f/news | high |
| 638 | program_html | ["30", "must-have", "product", "life"] | ["30", "must have", "product", "life"] | high |
| 659 | program_html | ["Roshan Jossey"] | ["Roshan Jossy"] | high |
| 660 | url_match | __GITLAB__/byteblaze/dotfiles/-/tree/main | __GITLAB__/byteblaze/dotfiles/-/issues | high |
| 780 | program_html | 64.00 | 101.00 | high |
| 780 | program_html | 64.00 | 101.00 | high |
| 782 | program_html | 22.33 | 35.67 | high |
| 782 | program_html | 22.33 | 35.67 | high |
| 782 | program_html | 21.56 | 34.44 | high |
| 782 | program_html | 21.56 | 34.44 | high |
