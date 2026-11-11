import csv
import json
import os
from datetime import datetime

# Fixed list of categories
CATEGORIES = ["Food", "Travel", "Rent", "Shopping", "Bills", "Other"]
CSV_FILE = "expenses.csv"
BUDGET_FILE = "budget.json"


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


def load_budgets(filename):
    budgets = {}
    if not os.path.exists(filename):
        return budgets

    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return budgets
            data = json.loads(content)
            if isinstance(data, dict):
                for month, amount in data.items():
                    try:
                        budgets[month] = float(amount)
                    except (ValueError, TypeError):
                        continue
    except Exception as e:
        print("Error reading budget file:", e)

    return budgets


def save_budgets(filename, budgets):
    try:
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(budgets, file, indent=4)
    except Exception as e:
        print("Error saving budgets:", e)


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


def get_valid_month():
    while True:
        user_input = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()
        if user_input == "":
            return datetime.today().strftime("%Y-%m")

        try:
            valid_month = datetime.strptime(user_input, "%Y-%m")
            return valid_month.strftime("%Y-%m")
        except ValueError:
            print("Invalid month format. Please use YYYY-MM.")


def add_expense(expense_list, budgets):
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
    print("Expense added successfully!")

    # Check monthly budget warning after adding an expense
    month = date[:7]
    check_budget_warning(expense_list, budgets, month)
    print()


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


def daily_total(expense_list, target_date):
    total = 0.0
    for exp in expense_list:
        if exp["date"] == target_date:
            total += exp["amount"]
    return total


def monthly_total(expense_list, target_month):
    total = 0.0
    for exp in expense_list:
        if exp["date"].startswith(target_month):
            total += exp["amount"]
    return total


def category_totals(expense_list, target_month):
    totals = {}
    for exp in expense_list:
        if exp["date"].startswith(target_month):
            cat = exp["category"]
            if cat in totals:
                totals[cat] += exp["amount"]
            else:
                totals[cat] = exp["amount"]
    return totals


def check_budget_warning(expense_list, budgets, month):
    if month not in budgets:
        return

    budget = budgets[month]
    spent = monthly_total(expense_list, month)

    if spent > budget:
        over = spent - budget
        print(f"WARNING: You have exceeded your budget for {month}! Spent ${spent:.2f} out of ${budget:.2f} (over by ${over:.2f}).")
    elif spent > 0.8 * budget:
        percent = (spent / budget) * 100
        print(f"NOTICE: You have used {percent:.1f}% of your budget for {month} (${spent:.2f} / ${budget:.2f}).")


def set_budget(budgets):
    print("\n--- Set Monthly Budget ---")
    month = get_valid_month()
    if month in budgets:
        print(f"Current budget for {month} is ${budgets[month]:.2f}.")

    amount = get_valid_amount()
    budgets[month] = amount
    save_budgets(BUDGET_FILE, budgets)
    print(f"Monthly budget for {month} set to ${amount:.2f}.\n")


def show_summary(expense_list, budgets):
    print("\n--- Spending Summary ---")
    if not expense_list:
        print("No expenses recorded yet.\n")
        return

    print("1. Daily spending:")
    target_date = get_valid_date()
    d_total = daily_total(expense_list, target_date)
    print(f"Total spent on {target_date}: ${d_total:.2f}\n")

    print("2. Monthly spending:")
    target_month = get_valid_month()
    m_total = monthly_total(expense_list, target_month)
    print(f"\n--- Summary for {target_month} ---")
    print(f"Total spent in {target_month}: ${m_total:.2f}")

    cat_totals = category_totals(expense_list, target_month)
    if cat_totals:
        print("\nCategory-wise totals:")
        for cat in cat_totals:
            print(f"  {cat:<12}: ${cat_totals[cat]:>8.2f}")
    else:
        print("No expenses found for this month.")

    if target_month in budgets:
        budget = budgets[target_month]
        remaining = budget - m_total
        print("\nBudget overview:")
        print(f"  Monthly Budget : ${budget:.2f}")
        print(f"  Amount Spent   : ${m_total:.2f}")
        if remaining >= 0:
            print(f"  Remaining      : ${remaining:.2f}")
        else:
            print(f"  Over Budget by : ${abs(remaining):.2f}")
    else:
        print(f"\nNo budget set for {target_month}.")

    print()


def main():
    expense_list = load_expenses(CSV_FILE)
    budgets = load_budgets(BUDGET_FILE)
    print("Loaded", len(expense_list), "expenses from", CSV_FILE)
    print("Loaded", len(budgets), "monthly budget(s) from", BUDGET_FILE)

    while True:
        print("=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Edit expense")
        print("4. Delete expense")
        print("5. Set monthly budget")
        print("6. Spending summary")
        print("7. Exit")

        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            add_expense(expense_list, budgets)
        elif choice == "2":
            view_expenses(expense_list)
        elif choice == "3":
            edit_expense(expense_list)
        elif choice == "4":
            delete_expense(expense_list)
        elif choice == "5":
            set_budget(budgets)
        elif choice == "6":
            show_summary(expense_list, budgets)
        elif choice == "7":
            print("Thank you for using Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.\n")


if __name__ == "__main__":
    main()
