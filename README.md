# Personal Expense & Budget Tracker

Day 3 of 4 - in progress

A simple command-line application to track personal expenses, set monthly budgets, and review spending summaries.

## Features Done So Far
- **Add Expense**: Record an expense with amount, category, description, and date. Includes automatic monthly budget warning checks (near-limit >80% and over-budget warnings).
- **View Expenses**: Display all recorded expenses in a numbered tabular format with total spending.
- **Edit Expense**: Modify date, category, description, or amount of an existing expense (press Enter to keep old values).
- **Delete Expense**: Remove an expense by number with confirmation prompt (`y/n`).
- **Monthly Budget**: Set monthly spending limits (`YYYY-MM`) stored in `budget.json`.
- **Spending Summary**: View daily total for a chosen date, monthly total, category-wise totals, and budget remaining/overage status.
- **Data Persistence & Validation**: Safe CSV/JSON storage and error handling for invalid inputs or missing files.

## How to Run
Ensure you have Python installed, then run:

```bash
python expense_tracker.py
```
