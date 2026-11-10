# Personal Expense & Budget Tracker

Day 2 of 4 - in progress

A simple command-line application to track personal expenses and manage daily spending.

## Features Done So Far
- **Add Expense**: Record an expense with amount, category, description, and date.
- **View Expenses**: Display all recorded expenses in a numbered tabular format with total spending summary.
- **Edit Expense**: Modify date, category, description, or amount of any existing expense (press Enter to keep old values).
- **Delete Expense**: Remove an expense by number with confirmation prompt (`y/n`).
- **Data Persistence**: Automatic loading and saving with CSV file (`expenses.csv`).
- **Input Validation & Safety**: Graceful validation for positive amounts, date formats (YYYY-MM-DD), predefined categories, and error handling for invalid selections.

## How to Run
Ensure you have Python installed, then run:

```bash
python expense_tracker.py
```
