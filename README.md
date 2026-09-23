# Personal Finance Manager (Basic + Standard + Advanced)

A command-line Python application for tracking personal expenses. Built as
a Month 1 project to practice core Python: OOP, file handling (CSV/JSON),
error handling, modular code organization, and (in the Advanced tier)
using external libraries.

This build includes all three project tiers in one app:

| Tier | Features |
|---|---|
| **Basic** | Add / view / search / delete expenses, CSV persistence, backups |
| **Standard** | Category-wise summary, monthly reports |
| **Advanced** | Budget planning with over-budget warnings, data export (JSON/Excel), spending charts |

## Setup Instructions

1. Make sure Python 3.8+ is installed:
   ```
   python3 --version
   ```
2. Download this project folder.
3. Install dependencies (only needed for the Advanced-tier features —
   charts and Excel export):
   ```
   pip install -r requirements.txt
   ```
   Basic and Standard features work with **no installs**, using only
   Python's standard library.
4. Run the app from the project's root folder:
   ```
   python3 main.py
   ```

## Code Structure

```
finance_manager/
├── main.py                # Entry point — run this file to start the app
├── requirements.txt       # matplotlib + openpyxl (Advanced tier only)
├── src/
│   ├── expense.py         # Expense class (data model)
│   ├── file_manager.py    # CSV read/write/backup functions      [Basic]
│   ├── menu.py            # Command-line interface & menu logic
│   ├── utils.py           # Input validation & formatting helpers
│   ├── reports.py         # Category summary & monthly reports   [Standard]
│   ├── budget.py          # Budget setting & over-budget checks  [Advanced]
│   ├── exporter.py        # JSON / Excel export                 [Advanced]
│   └── charts.py          # Matplotlib bar chart generation      [Advanced]
├── data/
│   ├── expenses.csv       # Your expense data (sample data included)
│   ├── budgets.csv        # Saved category budgets (created on demand)
│   ├── backups/           # Timestamped CSV backups
│   └── exports/           # JSON/Excel exports
├── reports/                # Generated chart images (.png)
├── docs/
│   └── user_guide.md      # How to use every menu option
└── screenshots/           # Add screenshots of the app running here
```

**Why this structure?** Each tier's features live in their own module, so
you can read `reports.py`, `budget.py`, `exporter.py`, and `charts.py`
independently to see exactly how each feature is built, without wading
through the whole app at once.

## How It Works (Technical Details)

- **Expense class** (`expense.py`): stores `amount`, `category`, `date`,
  `description`; converts to/from CSV rows.
- **Persistence** (`file_manager.py`): CSV read/write via Python's
  built-in `csv` module; starts empty instead of crashing if no file exists.
- **Validation** (`utils.py`): re-prompts until input is a valid amount,
  category, and `YYYY-MM-DD` date.
- **Reporting** (`reports.py`): uses `collections.defaultdict` to group
  expenses by category, computing totals/averages/counts; filters by
  month for the monthly report.
- **Budgets** (`budget.py`): stores a spending limit per category in
  `data/budgets.csv`; compares it against `reports.category_summary()`
  and warns immediately after adding an expense if a category goes over.
- **Export** (`exporter.py`): writes expenses to timestamped `.json`
  files (standard library `json` module) or `.xlsx` files (via the
  `openpyxl` package).
- **Charts** (`charts.py`): uses `matplotlib` in non-interactive ("Agg")
  mode to draw a bar chart of category totals and save it as a `.png` —
  a CLI app can't pop up a window, so the image is saved for you to open.

## Usage

```
MAIN MENU:
  --- Basic ---
  1. Add New Expense
  2. View All Expenses
  3. Search Expenses by Category
  4. Delete an Expense
  5. Backup Data
  --- Standard: Reporting & Analysis ---
  6. Category-wise Summary
  7. Monthly Report
  --- Advanced: Budget, Export & Charts ---
  8. Set Budget
  9. View Budget Status
 10. Export Data (JSON/Excel)
 11. Generate Spending Chart
  0. Exit
```

Sample data is already included in `data/expenses.csv` — run the app and
choose option 2 (or jump straight to 6 or 7) to see it in action.

## Testing Evidence

Manually tested every menu option end-to-end:
- Add/view/search/delete with valid and invalid input (bad numbers,
  bad dates, empty descriptions) → confirmed re-prompting works.
- Category summary and monthly report → confirmed totals/averages match
  manual calculation.
- Set a budget, then added an expense that exceeded it → confirmed the
  over-budget warning appears immediately, and "View Budget Status"
  reflects it.
- Exported to JSON and Excel → confirmed both files open correctly and
  contain all expense fields.
- Generated a chart → confirmed the `.png` shows correct per-category bars.
- Backup → confirmed a timestamped CSV copy appears in `data/backups/`.

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'menu'` | Run `main.py` from the project root, not from inside `src/`. |
| "Charts need the 'matplotlib' package" | Run `pip install -r requirements.txt`. |
| "Excel export needs the 'openpyxl' package" | Run `pip install -r requirements.txt`. |
| Expenses don't appear after restarting | Check that `data/expenses.csv` exists and wasn't deleted or moved. |
| "Invalid date format" keeps showing | Use exactly `YYYY-MM-DD`, e.g. `2024-01-15`. |
