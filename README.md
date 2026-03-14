# Groww Weekly Review Pulse

## Overview
This automated script fetches public app store reviews from the last 4 weeks, processes them to extract the top 5 themes, and generates a one-page "Weekly Pulse" markdown file as well as an Email draft.

## Prerequisites
- Python 3.9+
- Run `pip install -r requirements.txt`

## How to Re-Run for a New Week
1. Open a terminal in this directory.
2. Run `python main.py`.
3. The script will automatically fetch reviews from the exact date it is run to 4 weeks prior.
4. It will regenerate the `sample_reviews.csv`, `Weekly_Pulse.md`, and `Email_Draft.txt`.
5. Share the generated files with stakeholders!

## Theme Legend
- 🔴 **High Severity**: Critical bugs, crashes, or severe user friction blocking workflows. Needs immediate engineering/support attention.
- 🟠 **Medium Severity**: Sub-optimal experiences, delayed transactions, or features not working as intended but with workarounds.
- 🟡 **Needs Clarity**: Confusion around pricing, taxes, or navigation. Needs UX or content updates.
- 🟢 **Positive**: Praise for features, UI, or support. Should be highlighted to boost team morale.
- 🔵 **Feature Request**: Users asking for new capabilities or integrations.

## Note on Privacy
This script only scrapes *public* reviews. It strips metadata and explicitly avoids extracting or storing User IDs or explicit personal names in the generated reports.
