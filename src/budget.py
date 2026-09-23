"""
budget.py
---------
ADVANCED VERSION FEATURE: Budget planning.
Lets the user set a monthly spending limit per category and checks
actual spending against it.
"""

import csv
import os
from reports import category_summary

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUDGET_FILE = os.path.join(PROJECT_ROOT, "data", "budgets.csv")


def load_budgets():
    """Returns a dict like {"Food": 3000.0, "Transport": 1500.0}."""
    budgets = {}
    if not os.path.exists(BUDGET_FILE):
        return budgets

    try:
        with open(BUDGET_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for row in reader:
                if row:
                    category, limit = row
                    budgets[category] = float(limit)
    except (IOError, ValueError) as e:
        print(f"⚠️ Could not read budgets file: {e}")

    return budgets


def save_budgets(budgets):
    """Writes the budgets dict back to CSV."""
    os.makedirs(os.path.dirname(BUDGET_FILE), exist_ok=True)
    try:
        with open(BUDGET_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Limit"])
            for category, limit in budgets.items():
                writer.writerow([category, limit])
        return True
    except IOError as e:
        print(f"⚠️ Could not save budgets: {e}")
        return False


def set_budget():
    """Interactive prompt to set a budget limit for a category."""
    from utils import get_valid_category, get_valid_amount

    print("\nSET BUDGET:")
    category = get_valid_category()
    print("Enter the monthly limit for this category:")
    limit = get_valid_amount()

    budgets = load_budgets()
    budgets[category] = limit
    save_budgets(budgets)
    print(f"\n✅ Budget for {category} set to ₹{limit:.2f} per month.")


def check_budget_status(expenses):
    """Prints how actual spending compares to each set budget."""
    budgets = load_budgets()

    if not budgets:
        print("\nNo budgets set yet. Choose 'Set Budget' from the menu first.")
        return

    summary = category_summary(expenses)

    print("\nBUDGET STATUS:")
    print(f"{'Category':<15}{'Spent (₹)':>12}{'Budget (₹)':>12}{'Status':>12}")
    print("-" * 51)

    for category, limit in budgets.items():
        spent = summary.get(category, {}).get("total", 0.0)
        status = "⚠️ OVER" if spent > limit else "✅ OK"
        print(f"{category:<15}{spent:>12.2f}{limit:>12.2f}{status:>12}")


def warn_if_over_budget(category, expenses):
    """
    Called right after adding an expense — gives an immediate heads-up
    if this category has now gone over its budget.
    """
    budgets = load_budgets()
    if category not in budgets:
        return

    summary = category_summary(expenses)
    spent = summary.get(category, {}).get("total", 0.0)
    limit = budgets[category]

    if spent > limit:
        print(f"⚠️ Heads up: you've spent ₹{spent:.2f} on {category}, "
              f"over your ₹{limit:.2f} budget!")
