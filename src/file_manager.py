"""
file_manager.py
----------------
Handles saving and loading expenses to/from a CSV file, so data
survives between program runs. This is the "persistence" layer.
"""

import csv
import os
import shutil
from expense import Expense

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_FILE = os.path.join(PROJECT_ROOT, "data", "expenses.csv")
HEADER = ["Date", "Category", "Amount", "Description"]


def load_expenses(filename=DEFAULT_FILE):
    """
    Reads all expenses from the CSV file and returns them as a list
    of Expense objects. If the file doesn't exist yet, returns an
    empty list instead of crashing (this is our error handling).
    """
    expenses = []

    if not os.path.exists(filename):
        return expenses  # No file yet = no expenses yet, that's fine.

    try:
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            for row in reader:
                if row:  # Skip any blank lines
                    expenses.append(Expense.from_row(row))
    except (IOError, ValueError) as e:
        print(f"⚠️ Could not read expenses file: {e}")

    return expenses


def save_expenses(expenses, filename=DEFAULT_FILE):
    """Writes the full list of Expense objects to the CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)
            for expense in expenses:
                writer.writerow(expense.to_row())
        return True
    except IOError as e:
        print(f"⚠️ Could not save expenses: {e}")
        return False


def backup_expenses(filename=DEFAULT_FILE, backup_folder=None):
    if backup_folder is None:
        backup_folder = os.path.join(PROJECT_ROOT, "data", "backups")
    """Makes a timestamped copy of the expenses file, for safekeeping."""
    from datetime import datetime

    if not os.path.exists(filename):
        print("⚠️ No expenses file to back up yet.")
        return None

    os.makedirs(backup_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_folder, f"expenses_backup_{timestamp}.csv")

    try:
        shutil.copy(filename, backup_path)
        return backup_path
    except IOError as e:
        print(f"⚠️ Backup failed: {e}")
        return None
