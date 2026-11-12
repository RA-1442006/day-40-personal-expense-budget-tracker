# Personal Expense & Budget Tracker

Status: Completed (4 of 4 days)

A simple command-line Personal Expense & Budget Tracker built in Python to record daily spending, manage monthly budgets, view summaries, and search or filter past expenses.

## Features
- **Add Expenses**: Log expenses with amount, category, description, and date (defaults to today if left blank).
- **View Expenses**: Display all recorded expenses in a clean, numbered table along with the overall total.
- **Edit Expenses**: Update any field (date, category, description, amount) of an existing record, or press Enter to keep the old value.
- **Delete Expenses**: Remove an expense by its number with a confirmation check (`y/n`) before deleting.
- **Fixed Categories**: Organize spending across `Food`, `Travel`, `Rent`, `Shopping`, `Bills`, and `Other`.
- **Monthly Budget with Warnings**: Set monthly spending limits (`YYYY-MM`) and get automatic alerts when spending crosses 80% or exceeds the budget.
- **Spending Summary**: Check daily totals for any date, monthly totals, category-wise breakdowns, and remaining/over-budget status.
- **Search and Filter**: Search expenses by keyword (in description or category) or filter by category, month, date range, or amount range with match count and subtotal.
- **CSV and JSON Storage**: Saves expenses in `expenses.csv` and monthly budgets in `budget.json`.
- **Input Validation**: Checks positive amounts, valid `YYYY-MM-DD` dates, valid `YYYY-MM` months, and handles missing or empty files without crashing.

## Tools Used
- Python 3 (standard library: `csv`, `json`, `os`, `datetime`)
- CSV and JSON file formats
- VS Code
- Git and GitHub

## Project Structure
- `expense_tracker.py` - Main Python program with all menu features, validation, and file handling functions.
- `expenses.csv` - Stores all expense records (`date,category,description,amount`).
- `budget.json` - Stores monthly budget limits in `YYYY-MM` format.
- `sample_output.txt` - Real terminal output from testing search and filter options.
- `README.md` - Project documentation and overview.
- `.gitignore` - Standard Python ignore rules for cache and virtual environment files.

## How to Run
1. Open a terminal in the project folder.
2. Run the script with Python:

```bash
python expense_tracker.py
```

## Sample Usage
```text
--- Search Results for 'grocer' ---
#   | Date         | Category   | Description               |   Amount
--------------------------------------------------------------------
1   | 2026-09-10   | Food       | Weekly groceries          | $  54.00
2   | 2026-10-12   | Food       | Grocery shopping          | $  62.50
3   | 2026-11-05   | Food       | Groceries at supermarket  | $  45.50
--------------------------------------------------------------------
Matches found: 3 | Total Amount: $162.00
```

## My Approach
I built this project step by step over 4 days to keep the code simple and easy to extend:
- **Day 1**: Set up the project folder, built the basic CLI menu, added expense logging and viewing, and connected `expenses.csv` storage with input validation.
- **Day 2**: Added editing (keeping old values when Enter is pressed) and safe deleting with confirmation, plus numbered row displays.
- **Day 3**: Added monthly budget tracking in `budget.json`, over-limit and near-limit (80%) warnings, and daily/monthly/category spending summaries.
- **Day 4**: Added keyword search and filtering by category, month, date range, and amount range, cleaned up unused code, and wrote the final README.

## What I Learned
- Breaking a program into small, reusable functions for each feature and validation check.
- Working with lists and dictionaries to store, update, and aggregate expense records.
- Reading and writing persistent data with CSV (`csv.DictReader`, `csv.DictWriter`) and JSON (`json.load`/`json.dump`).
- Validating and formatting dates and months using the `datetime` module.
- Using `try/except` blocks and input loops so invalid user input or missing files never crash the program.

## Possible Future Improvements
- Export monthly spending summaries to a formatted text or CSV report file.
- Support recurring monthly expenses like rent or subscriptions automatically.
- Add custom user-defined categories instead of a fixed list.
- Include simple text-based bar charts in the terminal for category spending.
