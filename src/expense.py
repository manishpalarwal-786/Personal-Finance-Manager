"""
expense.py
----------
Defines the Expense class: a simple object that represents one expense entry.
"""


class Expense:
    """Represents a single expense (one row of spending data)."""

    def __init__(self, amount, category, date, description):
        # We store amount as a float so we can do math with it later.
        self.amount = float(amount)
        self.category = category
        self.date = date
        self.description = description

    def __str__(self):
        """
        Defines how an Expense looks when printed.
        Example: 2024-01-15 | Food: ₹1500.0 - Grocery shopping
        """
        return f"{self.date} | {self.category}: ₹{self.amount:.2f} - {self.description}"

    def to_row(self):
        """Converts this Expense into a list, ready to write to a CSV file."""
        return [self.date, self.category, self.amount, self.description]

    @staticmethod
    def from_row(row):
        """
        Builds an Expense object back from a CSV row.
        CSV row order is: [Date, Category, Amount, Description]
        """
        date, category, amount, description = row
        return Expense(amount, category, date, description)
