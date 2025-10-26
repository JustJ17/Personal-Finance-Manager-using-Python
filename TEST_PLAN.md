# 🧪 Personal Finance Manager - Comprehensive Test Plan

## Test User Credentials
**Username:** `TestUser`  
**Password:** `Test123!@#`  
**User ID:** 999  
**Email:** testuser@example.com

---

## ✅ Test Checklist

### 🔐 **1. Authentication Tests**
- [ ] **Register New User** (Option 1)
  - Test with valid credentials
  - Test with duplicate username (should fail)
  - Test with weak password (should fail)
  - Test with invalid email (should fail)

- [ ] **Login** (Option 2)
  - Login with TestUser credentials
  - Test wrong password (should fail)
  - Test non-existent username (should fail)

---

### 💰 **2. Transaction Management Tests**
- [ ] **Add Income/Expense** (Option 1)
  - Add income transaction
  - Add expense transaction
  - Test all categories: food, transport, entertainment, other
  - Test all payment methods: cash, credit, debit, other
  - Test with optional description
  - Test date input (custom date vs today)

- [ ] **View All Transactions** (Option 2)
  - Should display all 12 pre-loaded transactions
  - Check formatting and readability

- [ ] **Edit Transaction** (Option 3)
  - Edit transaction: `TestUser13` (October expense)
  - Change amount, category, date, payment method
  - Press Enter to keep existing values
  - Cancel edit (press 'n' when asked to save)

- [ ] **Delete Transaction** (Option 4)
  - Delete transaction: `TestUser6` (June expense)
  - Verify it's removed from list
  - Try deleting non-existent ID (should fail)

---

### 🔍 **3. Filtering & Sorting Tests**
- [ ] **Search by Date Range** (Option 5)
  - Search 2024-06-01 to 2024-08-31 (should find summer transactions)
  - Search 2025-01-01 to 2025-12-31 (should find 2025 transactions)

- [ ] **Filter by Category** (Option 6)
  - Filter by "Food" (should find 3 transactions)
  - Filter by "Transport" (should find 3 transactions)
  - Filter by "Entertainment" (should find 3 transactions)
  - Filter by "Other" (should find 3 transactions)

- [ ] **Filter by Amount Range** (Option 7)
  - Filter $0 to $100 (should find smaller transactions)
  - Filter $500 to $2000 (should find larger transactions)

- [ ] **Sort Results** (Option 8)
  - Sort by date (ascending/descending)
  - Sort by amount (ascending/descending)
  - Sort by category (alphabetical)

---

### 📊 **4. Reporting & Analytics Tests**
- [ ] **Monthly Budget Tracker** (Option 9)
  - View current month's spending
  - Check if over/under budget
  - Verify calculation accuracy

- [ ] **Monthly Reports** (Option 10)
  - Select "Current Month" (option 0)
  - Select specific month: June 2024 (should show 2 transactions)
  - Select month: October 2024 (should show 2 transactions)
  - View detailed transactions breakdown
  - Check most spent category
  - Verify visual category breakdown bars

- [ ] **Category Breakdown** (Option 11)
  - View all-time spending by category
  - Check total income vs total expenses
  - Verify net balance calculation
  - Check visual bar charts

- [ ] **Spending Trends** (Option 12)
  - View month-by-month spending chart
  - Check highest spending month (should be October 2024: $1,800)
  - Check lowest spending month (should be June 2024: $150)
  - Verify above-average indicators (🔥)
  - Check trend analysis (increasing/decreasing)

---

### 🔁 **5. Recurring Transactions Tests**
- [ ] **Recurring Transactions Menu** (Option 13)
  - View existing recurring transactions (3 pre-loaded)
  - Add new recurring transaction
  - Edit recurring transaction
  - Delete recurring transaction
  - Check if recurring transactions auto-create

---

### 📁 **6. CSV Import/Export Tests**
- [ ] **Export Transactions** (Option 14)
  - Export to CSV file
  - Check file exists: `TestUser_transactions.csv`
  - Open CSV and verify data format
  - Check all fields are present

- [ ] **Import Transactions** (Option 15)
  - Delete a transaction first
  - Import from pre-made `TestUser_transactions.csv`
  - Verify deleted transaction is restored
  - Check transaction count matches

---

### 🚪 **7. Exit & Session Management**
- [ ] **Exit Program** (Option 0)
  - Exit transaction manager (returns to login menu)
  - Exit main program (option 3)
  - Verify backup files are created

---

## 📋 Pre-Loaded Test Data Summary

### Transactions (12 total):
- **Income:** 3 transactions totaling $7,500
- **Expenses:** 9 transactions totaling $5,450
- **Net Balance:** $2,050
- **Date Range:** June 2024 - October 2025
- **Categories:** Food (3), Transport (3), Entertainment (3), Other (3)

### Recurring Transactions (3 total):
1. Monthly Rent: $1,200 (expense, other)
2. Weekly Groceries: $150 (expense, food)
3. Monthly Salary: $3,000 (income, other)

---

## 🐛 Known Issues to Test

1. **User dictionary update:** When creating transactions, check if `number_of_transactions` updates correctly
2. **Backup creation:** Verify backup files are created on startup and exit
3. **Monthly budget tracking:** Check if expenses correctly add to monthly totals
4. **Date formatting:** Ensure dates display correctly across all functions
5. **Empty lists:** Test all functions with empty transaction list

---

## 📝 Testing Notes

**Test Order Recommendation:**
1. Start with authentication tests
2. View existing data (option 2)
3. Test filtering and sorting
4. Test analytics/reports
5. Test CRUD operations (add/edit/delete)
6. Test CSV import/export
7. Test recurring transactions

**Tips:**
- Take screenshots of each successful test
- Note any error messages or unexpected behavior
- Check console output for proper formatting
- Verify JSON files update correctly after changes
- Test both valid and invalid inputs

---

## ✅ Test Completion Status

**Date Tested:** _______________  
**Tester Name:** _______________  
**Total Tests Passed:** _____ / 50+  
**Critical Bugs Found:** _____  
**Minor Issues Found:** _____  

---

## 🎯 Success Criteria

- [ ] All authentication tests pass
- [ ] All CRUD operations work correctly
- [ ] All filters and sorts work as expected
- [ ] All reports display accurate data
- [ ] CSV import/export works bidirectionally
- [ ] Recurring transactions auto-create properly
- [ ] No crashes or unhandled exceptions
- [ ] Data persists correctly across sessions
