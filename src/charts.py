"""
charts.py
---------
ADVANCED VERSION FEATURE: Charts.
Generates a bar chart of category-wise spending using matplotlib and
saves it as a PNG image (a CLI app can't "display" a chart on screen,
so we save it to a file the user can open).
"""

import os
from datetime import datetime
from reports import category_summary

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHART_FOLDER = os.path.join(PROJECT_ROOT, "reports")


def generate_spending_chart(expenses):
    """Creates a bar chart of total spending per category and saves it."""
    if not expenses:
        print("\nNo expenses to chart yet.")
        return None

    try:
        import matplotlib
        matplotlib.use("Agg")  # No display needed — we're just saving a file
        import matplotlib.pyplot as plt
    except ImportError:
        print("⚠️ Charts need the 'matplotlib' package. "
              "Install it with: pip install matplotlib")
        return None

    summary = category_summary(expenses)
    categories = list(summary.keys())
    totals = [summary[c]["total"] for c in categories]

    os.makedirs(CHART_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(CHART_FOLDER, f"spending_chart_{timestamp}.png")

    plt.figure(figsize=(8, 5))
    plt.bar(categories, totals, color="#4C72B0")
    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.tight_layout()

    try:
        plt.savefig(filepath)
        plt.close()
        return filepath
    except IOError as e:
        print(f"⚠️ Could not save chart: {e}")
        return None


def show_chart_menu(expenses):
    """Interactive wrapper called from the menu."""
    print("\nGenerating spending chart...")
    path = generate_spending_chart(expenses)
    if path:
        print(f"✅ Chart saved to: {path}")
        print("Open this image file to view it.")
