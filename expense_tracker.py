import csv
import os
from datetime import datetime

# Fixed list of categories
CATEGORIES = ["Food", "Travel", "Rent", "Shopping", "Bills", "Other"]
CSV_FILE = "expenses.csv"


def load_expenses(filename):
    expenses = []
    # If the file does not exist, return an empty list
    if not os.path.exists(filename):
        return expenses

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Basic check to avoid blank rows
                if row and "amount" in row and row["amount"]:
                    try:
                        amount = float(row["amount"])
                        expenses.append({
                            "date": row["date"],
                            "category": row["category"],
                            "description": row["description"],
                            "amount": amount
                        })
                    except ValueError:
                        # Skip row if amount cannot be parsed
                        continue
    except Exception as e:
        print("Error reading expenses file:", e)

    return expenses


def save_expenses(filename, expense_list):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["date", "category", "description", "amount"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for exp in expense_list:
                writer.writerow({
                    "date": exp["date"],
                    "category": exp["category"],
                    "description": exp["description"],
                    "amount": f"{exp['amount']:.2f}"
                })
    except Exception as e:
        print("Error saving expenses:", e)


def get_valid_amount():
    while True:
        user_input = input("Enter amount: ").strip()
        try:
            amount = float(user_input)
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Invalid input. Please enter a valid number for amount.")


def get_valid_category():
    print("Categories:")
    for i in range(len(CATEGORIES)):
        print(f"  {i + 1}. {CATEGORIES[i]}")

    while True:
        choice = input("Select a category (number or name): ").strip()
        # Check if user entered a number from the list
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(CATEGORIES):
                return CATEGORIES[index]
            else:
                print("Invalid number. Please choose from the list.")
                continue

        # Check if user entered the category name directly
        for cat in CATEGORIES:
            if choice.lower() == cat.lower():
                return cat

        print("Invalid category. Please select a valid category from the list.")


def get_valid_date():
    while True:
        user_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if user_input == "":
            return datetime.today().strftime("%Y-%m-%d")

        try:
            valid_date = datetime.strptime(user_input, "%Y-%m-%d")
            return valid_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def add_expense(expense_list):
    print("\n--- Add New Expense ---")
    amount = get_valid_amount()
    category = get_valid_category()
    description = input("Enter description: ").strip()
    if description == "":
        description = "No description"
    date = get_valid_date()

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    }

    expense_list.append(expense)
    save_expenses(CSV_FILE, expense_list)
    print("Expense added successfully!\n")


def view_expenses(expense_list):
    print("\n--- All Expenses ---")
    if not expense_list:
        print("No expenses recorded yet.\n")
        return

    # Print table header
    print(f"{'Date':<12} | {'Category':<10} | {'Description':<25} | {'Amount':>8}")
    print("-" * 62)

    total = 0.0
    for exp in expense_list:
        print(f"{exp['date']:<12} | {exp['category']:<10} | {exp['description']:<25} | ${exp['amount']:>7.2f}")
        total += exp['amount']

    print("-" * 62)
    print(f"Total Expenses: ${total:.2f} ({len(expense_list)} records)\n")


def main():
    expense_list = load_expenses(CSV_FILE)
    print("Loaded", len(expense_list), "expenses from", CSV_FILE)

    while True:
        print("=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            add_expense(expense_list)
        elif choice == "2":
            view_expenses(expense_list)
        elif choice == "3":
            print("Thank you for using Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")


if __name__ == "__main__":
    main()
