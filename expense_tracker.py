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


def get_valid_amount(current_value=None):
    prompt = "Enter amount: "
    if current_value is not None:
        prompt = f"Enter amount (press Enter to keep {current_value:.2f}): "

    while True:
        user_input = input(prompt).strip()
        if current_value is not None and user_input == "":
            return current_value

        try:
            amount = float(user_input)
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Invalid input. Please enter a valid number for amount.")


def get_valid_category(current_category=None):
    print("Categories:")
    for i in range(len(CATEGORIES)):
        print(f"  {i + 1}. {CATEGORIES[i]}")

    prompt = "Select a category (number or name): "
    if current_category is not None:
        prompt = f"Select a category (press Enter to keep '{current_category}'): "

    while True:
        choice = input(prompt).strip()
        if current_category is not None and choice == "":
            return current_category

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


def get_valid_date(current_date=None):
    while True:
        if current_date is not None:
            prompt = f"Enter date (YYYY-MM-DD) or press Enter to keep {current_date}: "
        else:
            prompt = "Enter date (YYYY-MM-DD) or press Enter for today: "

        user_input = input(prompt).strip()
        if user_input == "":
            if current_date is not None:
                return current_date
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
    print(f"{'#':<3} | {'Date':<12} | {'Category':<10} | {'Description':<25} | {'Amount':>8}")
    print("-" * 68)

    total = 0.0
    for i, exp in enumerate(expense_list, start=1):
        print(f"{i:<3} | {exp['date']:<12} | {exp['category']:<10} | {exp['description']:<25} | ${exp['amount']:>7.2f}")
        total += exp['amount']

    print("-" * 68)
    print(f"Total Expenses: ${total:.2f} ({len(expense_list)} records)\n")


def edit_expense(expense_list):
    print("\n--- Edit Expense ---")
    if not expense_list:
        print("No expenses to edit.\n")
        return

    view_expenses(expense_list)

    while True:
        choice = input("Enter the number of the expense to edit (or 'c' to cancel): ").strip()
        if choice.lower() == 'c':
            print("Edit cancelled.\n")
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(expense_list):
                break
            else:
                print(f"Number out of range. Please enter a number between 1 and {len(expense_list)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    exp = expense_list[index]
    print(f"\nEditing Expense #{index + 1}:")
    print("Press Enter on any field to keep the current value.\n")

    new_date = get_valid_date(current_date=exp["date"])
    new_category = get_valid_category(current_category=exp["category"])

    new_desc = input(f"Enter description (press Enter to keep '{exp['description']}'): ").strip()
    if new_desc == "":
        new_desc = exp["description"]

    new_amount = get_valid_amount(current_value=exp["amount"])

    # Update the record
    exp["date"] = new_date
    exp["category"] = new_category
    exp["description"] = new_desc
    exp["amount"] = new_amount

    save_expenses(CSV_FILE, expense_list)
    print("Expense updated successfully!\n")


def delete_expense(expense_list):
    print("\n--- Delete Expense ---")
    if not expense_list:
        print("No expenses to delete.\n")
        return

    view_expenses(expense_list)

    while True:
        choice = input("Enter the number of the expense to delete (or 'c' to cancel): ").strip()
        if choice.lower() == 'c':
            print("Deletion cancelled.\n")
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(expense_list):
                break
            else:
                print(f"Number out of range. Please enter a number between 1 and {len(expense_list)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    selected = expense_list[index]
    print(f"Selected: #{index + 1} - {selected['date']} | {selected['category']} | {selected['description']} | ${selected['amount']:.2f}")
    confirm = input("Are you sure? (y/n): ").strip().lower()

    if confirm == "y" or confirm == "yes":
        deleted = expense_list.pop(index)
        save_expenses(CSV_FILE, expense_list)
        print("Expense deleted successfully!\n")
    else:
        print("Expense deletion cancelled.\n")


def main():
    expense_list = load_expenses(CSV_FILE)
    print("Loaded", len(expense_list), "expenses from", CSV_FILE)

    while True:
        print("=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Edit expense")
        print("4. Delete expense")
        print("5. Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            add_expense(expense_list)
        elif choice == "2":
            view_expenses(expense_list)
        elif choice == "3":
            edit_expense(expense_list)
        elif choice == "4":
            delete_expense(expense_list)
        elif choice == "5":
            print("Thank you for using Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.\n")


if __name__ == "__main__":
    main()
