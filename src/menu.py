"""
menu.py
-------
The command-line interface: displays the menu, reads the user's choice,
and calls the right function to handle it. This is the "view" layer.

Combines all three project tiers:
  - Basic:    add / view / search / delete / backup
  - Standard: category summary / monthly report
  - Advanced: budget planning / data export / charts
"""

from expense import Expense
from file_manager import save_expenses, backup_expenses, load_expenses
from utils import get_valid_amount, get_valid_category, get_valid_date, get_description, pause
from reports import print_category_summary, print_monthly_report
from budget import set_budget, check_budget_status, warn_if_over_budget
from exporter import export_data
from charts import show_chart_menu


def show_menu():
    print("\n==========================================")
    print("     PERSONAL FINANCE MANAGER")
    print("==========================================\n")
    print("MAIN MENU:")
    print("  --- Basic ---")
    print("  1. Add New Expense")
    print("  2. View All Expenses")
    print("  3. Search Expenses by Category")
    print("  4. Delete an Expense")
    print("  5. Backup Data")
    print("  --- Standard: Reporting & Analysis ---")
    print("  6. Category-wise Summary")
    print("  7. Monthly Report")
    print("  --- Advanced: Budget, Export & Charts ---")
    print("  8. Set Budget")
    print("  9. View Budget Status")
    print(" 10. Export Data (JSON/Excel)")
    print(" 11. Generate Spending Chart")
    print("  0. Exit")


def add_expense(expenses):
    print("\nADD NEW EXPENSE:")
    amount = get_valid_amount()
    category = get_valid_category()
    date = get_valid_date()
    description = get_description()

    new_expense = Expense(amount, category, date, description)
    expenses.append(new_expense)
    save_expenses(expenses)

    print("\n✅ Expense added successfully!")
    warn_if_over_budget(category, expenses)  # Advanced: instant budget check


def view_expenses(expenses):
    print("\nALL EXPENSES:")
    if not expenses:
        print("No expenses recorded yet.")
        return

    total = 0
    for i, expense in enumerate(expenses, start=1):
        print(f"{i}. {expense}")
        total += expense.amount

    print(f"\nTotal spent: ₹{total:.2f}  |  Number of expenses: {len(expenses)}")


def search_by_category(expenses):
    from utils import VALID_CATEGORIES

    options = "/".join(VALID_CATEGORIES)
    category = input(f"\nEnter category to search ({options}): ").strip().title()

    matches = [e for e in expenses if e.category == category]

    if not matches:
        print(f"No expenses found in category '{category}'.")
        return

    total = 0
    print(f"\nExpenses in '{category}':")
    for i, expense in enumerate(matches, start=1):
        print(f"{i}. {expense}")
        total += expense.amount
    print(f"\nSubtotal for {category}: ₹{total:.2f}")


def delete_expense(expenses):
    if not expenses:
        print("\nNo expenses to delete.")
        return

    view_expenses(expenses)
    try:
        choice = int(input("\nEnter the number of the expense to delete (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(expenses):
            removed = expenses.pop(choice - 1)
            save_expenses(expenses)
            print(f"\n🗑️ Deleted: {removed}")
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Please enter a valid number.")


def backup_data():
    path = backup_expenses()
    if path:
        print(f"\n💾 Backup saved to: {path}")


def run():
    """Main program loop: keeps showing the menu until the user exits."""
    expenses = load_expenses()

    actions = {
        "1": lambda: add_expense(expenses),
        "2": lambda: view_expenses(expenses),
        "3": lambda: search_by_category(expenses),
        "4": lambda: delete_expense(expenses),
        "5": lambda: backup_data(),
        "6": lambda: print_category_summary(expenses),
        "7": lambda: print_monthly_report(expenses),
        "8": lambda: set_budget(),
        "9": lambda: check_budget_status(expenses),
        "10": lambda: export_data(expenses),
        "11": lambda: show_chart_menu(expenses),
    }

    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "0":
            print("\nGoodbye! 👋")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("❌ Invalid choice. Please pick a number from the menu.")

        pause()
