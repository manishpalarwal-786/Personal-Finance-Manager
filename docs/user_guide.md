# User Guide

## Starting the App

From the project's root folder, run:
```
python3 main.py
```
(Run `pip install -r requirements.txt` first if you want the chart and
Excel-export features — everything else works with no installs.)

## Menu Options

### Basic

**1. Add New Expense** — Enter amount, category, date (`YYYY-MM-DD`), and
description. The app re-prompts on any invalid input. If you've set a
budget for that category, you'll get an instant warning if you've now
gone over it.

**2. View All Expenses** — Lists every expense with a running total.

**3. Search Expenses by Category** — Filters to one category, with a
subtotal.

**4. Delete an Expense** — Pick a numbered expense to remove, or `0` to cancel.

**5. Backup Data** — Saves a timestamped copy of `expenses.csv` to
`data/backups/`.

### Standard: Reporting & Analysis

**6. Category-wise Summary** — Shows total, average, and count of
expenses per category, sorted highest-spending first.

**7. Monthly Report** — Enter a year and month; see every transaction
that month, the total, and a per-category breakdown.

### Advanced: Budget, Export & Charts

**8. Set Budget** — Choose a category and set a monthly spending limit
for it. Limits are saved in `data/budgets.csv` and persist between runs.

**9. View Budget Status** — Shows spending vs. budget for every category
you've set a limit for, marking each ✅ OK or ⚠️ OVER.

**10. Export Data (JSON/Excel)** — Choose to export all expenses as a
`.json` file or an `.xlsx` (Excel) file, saved to `data/exports/`.

**11. Generate Spending Chart** — Creates a bar chart (PNG image) of
total spending per category, saved to `reports/`. Open the image file
to view it.

**0. Exit** — Closes the program. Data is saved after every add/delete/
budget change, so there's nothing extra to do before exiting.

## Tips

- Dates must be `YYYY-MM-DD` (year-month-day), e.g. `2024-03-05`.
- Categories aren't case-sensitive — "food" and "FOOD" both work.
- Budgets are per category, not per month — they apply to your
  all-time total in that category (a good beginner-friendly starting
  point; a future version could reset budgets each month).
- Your raw data lives in `data/expenses.csv` — you can open it in Excel
  directly, but it's best to only *edit* it through the app.
