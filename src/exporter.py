"""
exporter.py
-----------
ADVANCED VERSION FEATURE: Data export.
Lets the user export their expenses to formats other than CSV
(JSON for developers/other tools, Excel for spreadsheets).
"""

import json
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_FOLDER = os.path.join(PROJECT_ROOT, "data", "exports")


def export_to_json(expenses):
    """Exports all expenses to a timestamped .json file."""
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(EXPORT_FOLDER, f"expenses_{timestamp}.json")

    data = [
        {
            "date": e.date,
            "category": e.category,
            "amount": e.amount,
            "description": e.description,
        }
        for e in expenses
    ]

    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=2)
        return filepath
    except IOError as e:
        print(f"⚠️ JSON export failed: {e}")
        return None


def export_to_excel(expenses):
    """
    Exports all expenses to a timestamped .xlsx file, using the
    openpyxl library (listed in requirements.txt).
    """
    try:
        from openpyxl import Workbook
    except ImportError:
        print("⚠️ Excel export needs the 'openpyxl' package. "
              "Install it with: pip install openpyxl")
        return None

    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(EXPORT_FOLDER, f"expenses_{timestamp}.xlsx")

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Expenses"
    sheet.append(["Date", "Category", "Amount", "Description"])

    for expense in expenses:
        sheet.append([expense.date, expense.category, expense.amount, expense.description])

    # Make the header bold and widen columns a little, so the file
    # looks presentable when opened in Excel/Google Sheets.
    for cell in sheet[1]:
        cell.font = cell.font.copy(bold=True)
    for col in "ABCD":
        sheet.column_dimensions[col].width = 18

    try:
        workbook.save(filepath)
        return filepath
    except IOError as e:
        print(f"⚠️ Excel export failed: {e}")
        return None


def export_data(expenses):
    """Interactive prompt: choose JSON or Excel export."""
    if not expenses:
        print("\nNo expenses to export yet.")
        return

    print("\nEXPORT DATA:")
    print("1. Export as JSON")
    print("2. Export as Excel (.xlsx)")
    choice = input("Choose an option (1-2): ").strip()

    if choice == "1":
        path = export_to_json(expenses)
    elif choice == "2":
        path = export_to_excel(expenses)
    else:
        print("❌ Invalid choice.")
        return

    if path:
        print(f"\n✅ Exported to: {path}")
