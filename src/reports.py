"""
reports.py
----------
STANDARD VERSION FEATURE: Reporting and analysis.
Turns a raw list of Expense objects into useful summaries.
"""

from collections import defaultdict
from datetime import datetime


def category_summary(expenses):
    """
    Groups expenses by category and returns a dict like:
    {
        "Food": {"total": 1950.0, "average": 975.0, "count": 2},
        ...
    }
    """
    totals = defaultdict(float)
    counts = defaultdict(int)

    for expense in expenses:
        totals[expense.category] += expense.amount
        counts[expense.category] += 1

    summary = {}
    for category in totals:
        summary[category] = {
            "total": totals[category],
            "average": totals[category] / counts[category],
            "count": counts[category],
        }
    return summary


def print_category_summary(expenses):
    """Prints a readable category-wise breakdown to the console."""
    summary = category_summary(expenses)

    if not summary:
        print("No expenses to summarize yet.")
        return

    print("\nCATEGORY-WISE SUMMARY:")
    print(f"{'Category':<15}{'Total (₹)':>12}{'Average (₹)':>14}{'Count':>8}")
    print("-" * 49)

    grand_total = 0
    for category, data in sorted(summary.items(), key=lambda x: -x[1]["total"]):
        print(f"{category:<15}{data['total']:>12.2f}{data['average']:>14.2f}{data['count']:>8}")
        grand_total += data["total"]

    print("-" * 49)
    print(f"{'GRAND TOTAL':<15}{grand_total:>12.2f}")


def monthly_report(expenses, year, month):
    """
    Filters expenses down to one calendar month (year, month) and
    returns (matching_expenses, total, category_summary_for_that_month).
    """
    matching = []
    for expense in expenses:
        try:
            date_obj = datetime.strptime(expense.date, "%Y-%m-%d")
        except ValueError:
            continue  # Skip any malformed dates instead of crashing
        if date_obj.year == year and date_obj.month == month:
            matching.append(expense)

    total = sum(e.amount for e in matching)
    return matching, total, category_summary(matching)


def print_monthly_report(expenses):
    """Asks the user for a month/year, then prints a report for it."""
    try:
        year = int(input("\nEnter year (e.g. 2024): ").strip())
        month = int(input("Enter month (1-12): ").strip())
        if not (1 <= month <= 12):
            raise ValueError
    except ValueError:
        print("❌ Please enter a valid year and month (1-12).")
        return

    matching, total, summary = monthly_report(expenses, year, month)
    month_name = datetime(year, month, 1).strftime("%B %Y")

    print(f"\nMONTHLY REPORT — {month_name}")
    print("-" * 40)

    if not matching:
        print("No expenses found for this month.")
        return

    for expense in matching:
        print(f"  {expense}")

    print("-" * 40)
    print(f"Total spent in {month_name}: ₹{total:.2f}")
    print(f"Number of transactions: {len(matching)}")

    print("\nBy category:")
    for category, data in sorted(summary.items(), key=lambda x: -x[1]["total"]):
        print(f"  {category}: ₹{data['total']:.2f} ({data['count']} transactions)")
