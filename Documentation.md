# Personal Finance Manager - Technical Documentation

## Python Concepts & Code Snippets

### Multi-line String Printing

```python
print("""
╔══════════════════════════════════════╗
║         WELCOME TO APP               ║
╚══════════════════════════════════════╝
""")
```

**Explanation:** It prints everything between the triple quotes (`""" ... """`) exactly as written — including newlines and spaces — as plain text.

---

### File Path Construction

```python
file_path = os.path.join('data', 'transactions', f'transactions_{user["name"]}_{user["id"]}.json')
```

**Explanation:**
- `os.path.join()` safely combines folder and file names into one full path (it adds the right slashes for your OS).
- The `f` before the string makes it an f-string, letting you insert variable values inside `{}`.
- `user["name"]` and `user["id"]` pull the name and ID from the user dictionary to personalize the file name.

---

### Creating Directories

```python
os.makedirs(os.path.dirname(file_path), exist_ok=True)
```

**Explanation:**
- It creates all folders in the path if they don't already exist.
- `os.path.dirname(file_path)` gets the folder part of the path.
- `exist_ok=True` means "don't crash if the folder already exists."

---

### Writing JSON to File

```python
with open(file_path, 'w') as f:
    json.dump([], f)
```

**Explanation:**
- It opens (or creates) the file for writing and saves an empty list `[]` as JSON inside it.
- `'w'` means "write mode" (overwrites the file).
- `f` is the file object used for writing.

---

### Reading and Parsing JSON

```python
with open(file_path, "r") as file:
    transactions_data = json.load(file)
    transactions_list = [Transaction.from_dict(t) for t in transactions_data]
    user["number_of_transactions"] = len(transactions_list)
except json.JSONDecodeError:
    transactions_list = []
return transactions_list
```

**Explanation:**
- `with open(file_path, "r") as file:` → opens the file for reading safely (it auto-closes).
- `transactions_data = json.load(file)` → reads and converts the JSON content into a Python list or dict.
- `transactions_list = [Transaction.from_dict(t) for t in transactions_data]` → builds a list of Transaction objects using each JSON entry.
- `user["number_of_transactions"] = len(transactions_list)` → counts how many transactions were loaded and stores that in the user dict.
- `except json.JSONDecodeError:` → catches errors if the file isn't valid JSON (e.g., corrupted).
- `transactions_list = []` → starts fresh with an empty list in that case.
- `return transactions_list` → gives back the final list of transactions.

---

### File Reading Methods

```python
file.readline()   # reads one line from the file each time you call it
file.readlines()  # reads all lines and returns them as a list of strings
file.read()       # reads the whole file as one string
json.load(file)   # reads the whole file and parses it into Python data (like a list or dict)
```

**What makes it read as a list or a dict?**

It depends on what's inside the JSON file:
- If the file's content starts with `[` → it's a list (array).
- If it starts with `{` → it's a dict (object).

---

### Exception Handling

```python
except Exception as e:
    print(f"Error: {e}")
    return []
```

**Explanation:**
- This catches any error that happens in the try block.
- `Exception as e` stores the error message in `e`.
- `print(f"...{e}")` shows what went wrong.
- `return []` gives back an empty list instead of crashing.

**Some examples this could catch:**
- `FileNotFoundError` → file path doesn't exist.
- `PermissionError` → you don't have permission to access the file.
- `IsADirectoryError` → tried to open a folder like a file.
- `OSError` → general system-level file issue.
- `json.JSONDecodeError` (if reading JSON inside the same try block).

---

### Writing Formatted JSON

```python
with open(file_path, 'w') as f:
    json.dump(transactions_data, f, indent=4)
```

**Explanation:**
- It opens the file for writing and saves `transactions_data` into it as nicely formatted JSON.
- `'w'` → overwrites the file.
- `json.dump(..., indent=4)` → writes JSON with 4-space indentation for readability.
- `json.dump()` → writes JSON directly to a file.
- `json.dumps()` → converts data to a JSON string (you can print or store it in a variable).

---

### CSV Export

```python
filename = f"{user['name']}_transactions.csv"
fieldnames = ["transaction_id", "type", "user_id", "amount", "date", "category", "description", "payment_method"]

with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows([t.to_dict() for t in transactions])
```

**Explanation:**
- It creates a CSV file named after the user and writes all transactions into it.
- `fieldnames` → defines the CSV column headers.
- `csv.DictWriter` → writes rows from dictionaries.
- `writer.writeheader()` → writes the column names.
- `writer.writerows([...])` → writes each transaction as a row (converted to a dict).
- `newline=""` → prevents extra blank lines from appearing between rows (especially on Windows).
- `encoding="utf-8"` → ensures all characters (like emojis or non-English text) are saved correctly.

---

### CSV Import

```python
with open(filename, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    transactions_data = list(reader)

if not transactions_data:
    print("⚠️ The CSV file is empty.")
    return

# Convert CSV data to Transaction objects
transactions = []
for t in transactions_data:
    # Convert string values to proper types
    if "amount" in t:
        t["amount"] = float(t["amount"])
    if "user_id" in t:
        t["user_id"] = int(t["user_id"]) if t["user_id"].isdigit() else t["user_id"]
    
    # Note: from_dict() will handle date conversion internally
    # Create Transaction object from dict
    transaction = Transaction.from_dict(t)
    transactions.append(transaction)
```

**Explanation:**
- `csv.DictReader` → reads each row as a dictionary.
- `transactions_data = list(reader)` → loads all rows into memory.
- `if not transactions_data:` → checks if the CSV is empty.
- Then it converts numeric strings to proper types (float, int).
- Finally, `Transaction.from_dict(t)` creates objects and adds them to the list.

---

### List Comprehension for Filtering

```python
transactions = [t for t in transactions if t.transaction_id != transaction_id]
```

**Explanation:** This creates a new list of all transactions except the one whose `transaction_id` matches the given `transaction_id`. In short — it filters out that specific transaction.

---

### Enumerate Function

```python
for i, option in enumerate(valid_sort_fields, 1):
    print(f"[{i}] {option}")
```

**Explanation:**
This loops through `valid_sort_fields`, giving both:
- `i` → the position (starting at 1, because of the `, 1`)
- `option` → the actual item.

**Example:** if `valid_sort_fields = ["date", "amount"]`, you get `(1, "date")`, then `(2, "amount")`.

---

### Dynamic Sorting with Lambda and getattr

```python
sorted_list = sorted(transaction_list, key=lambda x: getattr(x, sort_by), reverse=descending)
```

**Explanation:**
- It sorts `transaction_list` based on a specific attribute.
- `key=lambda x: getattr(x, sort_by)` → gets the value of the attribute named in `sort_by` for each transaction.
- `reverse=descending` → if True, sorts in descending order.
- `getattr(x, sort_by)` fetches an attribute value from object `x` using the name stored in `sort_by`.
  - So if `sort_by = "amount"` and `x.amount = 200`, then `getattr(x, "amount")` returns `200`.

**Note:**
- `sorted()` → creates and returns a new sorted list, leaving the original unchanged.
- `.sort()` → sorts the list in place and returns None.

---

### Date Parsing

```python
start_date = datetime.datetime.strptime(start_input, "%Y-%m-%d").date()
```

**Explanation:**
- It converts a string like `"2025-10-28"` into a Python date object.
- `strptime()` → parses the string using the given format.
- `.date()` → extracts only the date part (no time).

**Date Format Pattern (`%Y-%m-%d`):**
- `%Y` → 4-digit year (e.g. 2025)
- `%m` → 2-digit month (01–12)
- `%d` → 2-digit day (01–31)

---

### Date Formatting

```python
month_name = datetime.datetime(year, month, 1).strftime("%B %Y")
```

**Explanation:**
- It builds a date for the 1st day of a given month and formats it as a readable string.
- `datetime(year, month, 1)` → creates a date like 2025-10-01.
- `.strftime("%B %Y")` → formats it as "October 2025".

---

### Dictionary Operations

#### Sorting Dictionary Keys

```python
sorted_months = sorted(available_months.keys())
```

**Explanation:**
- It sorts the dictionary's keys (`available_months.keys()`) in ascending order and returns them as a list.
- `.keys()` returns all the keys from a dictionary as a special view object.

---

#### Tuple Unpacking

```python
selected_year, selected_month_num = selected_month
```

**Explanation:**
- It unpacks the tuple `selected_month` into two variables:
  - `selected_year` gets the first value
  - `selected_month_num` gets the second

---

#### Sorting Dictionary by Values

```python
sorted_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)
```

**Explanation:**
- It sorts the dictionary `category_spending` by its values (the amounts), from largest to smallest.
- `.items()` → gives key–value pairs as tuples.
- `key=lambda x: x[1]` → sorts using the value part of each pair.
- `reverse=True` → makes it descending.

---

### String Formatting

```python
print(f" {trans.date} | ${trans.amount:>10,.2f} | {trans.category:<15} | {trans.description}")
```

**Explanation:**
It prints a formatted line with aligned columns:
- `{trans.date}` → date
- `${trans.amount:>10,.2f}` → amount, right-aligned in 10 spaces with commas and 2 decimals
- `{trans.category:<15}` → category, left-aligned in 15 spaces
- `{trans.description}` → description

**Format Specifiers:**
- `>` → right-aligns text or numbers within the given width.
- `<` → left-aligns within the width.
- `10` → reserves 10 character spaces.
- `,.2f` → formats as a floating-point number with commas and 2 decimal places (e.g. 1,234.50).

---

### ISO Format Date Conversion

```python
date_str = self.date.isoformat() if hasattr(self.date, "isoformat") else str(self.date)
```

**Explanation:**
- It checks if `self.date` has an `isoformat()` method (like a datetime or date object).
- If yes → uses `self.date.isoformat()` (e.g. "2025-10-28")
- If no → just converts it to a string with `str(self.date)`
- `isoformat()` returns the date or datetime as a standardized ISO 8601 string — an international format computers and APIs understand easily.

---
