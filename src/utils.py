"""
utils.py
--------
Small helper functions used across the app: input validation and formatting.
Keeping these separate keeps main.py and menu.py clean and readable.
"""

from datetime import datetime

VALID_CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Other"]


def get_valid_amount():
    """Keeps asking the user for an amount until they type a valid positive number."""
    while True:
        raw = input("Enter amount: ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("❌ Amount must be greater than 0. Try again.")
                continue
            return amount
        except ValueError:
            print("❌ That's not a valid number. Try again.")


def get_valid_category():
    """Keeps asking until the user picks one of the allowed categories."""
    options = "/".join(VALID_CATEGORIES)
    while True:
        category = input(f"Enter category ({options}): ").strip().title()
        if category in VALID_CATEGORIES:
            return category
        print(f"❌ Please choose one of: {options}")


def get_valid_date():
    """Keeps asking until the user enters a date in YYYY-MM-DD format."""
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD (e.g. 2024-01-15).")


def get_description():
    """Gets a non-empty description from the user."""
    while True:
        description = input("Enter description: ").strip()
        if description:
            return description
        print("❌ Description can't be empty.")


def pause():
    """Waits for the user to press Enter before continuing (used after each action)."""
    input("\nPress Enter to continue...")
