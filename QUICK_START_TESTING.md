# 🚀 Quick Start Testing Guide

## Test User Credentials
```
Username: TestUser
Password: Test123!@#
User ID: 999
```

## What's Been Created

### 📁 Files Created:
1. **TEST_PLAN.md** - Comprehensive test checklist (50+ test cases)
2. **data/users.json** - TestUser added with hashed password
3. **data/transactions/transactions_TestUser_999.json** - 15 sample transactions
4. **data/RecurringTransactions/RecurringTransactions_TestUser_999.json** - 5 recurring transactions
5. **TestUser_transactions.csv** - 5 sample CSV transactions for import testing

---

## 📊 Test Data Summary

### Transactions (15 total)
| Month | Income | Expenses | Net |
|-------|--------|----------|-----|
| Jun 2024 | $3,000 | $150 | +$2,850 |
| Jul 2024 | $500 | $400 | +$100 |
| Aug 2024 | $0 | $350 | -$350 |
| Sep 2024 | $4,000 | $800 | +$3,200 |
| Oct 2024 | $0 | $1,800 | -$1,800 |
| Oct 2025 | $0 | $1,950 | -$1,950 |
| **TOTAL** | **$7,500** | **$5,450** | **+$2,050** |

### By Category
- **Food:** 3 transactions ($600 total)
- **Transport:** 3 transactions ($850 total)
- **Entertainment:** 3 transactions ($2,100 total)
- **Other:** 6 transactions ($4,400 total - includes income)

### Recurring Transactions (5 total)
1. **Monthly Rent** - $1,200 (expense, next: Dec 1)
2. **Weekly Groceries** - $150 (expense, next: Nov 4)
3. **Monthly Salary** - $3,000 (income, next: Dec 1)
4. **Streaming Subscription** - $50 (expense, next: Nov 15)
5. **Weekly Fuel** - $80 (expense, next: Nov 2)

### CSV Import File
- 5 December 2024 transactions
- Total: $2,500 income, $580 expenses

---

## 🎯 Quick Test Steps

### 1️⃣ Login Test
```
1. Run main.py
2. Select option [2] Login
3. Enter: TestUser
4. Enter: Test123!@#
5. You should see: "✅ Welcome back, TestUser!"
```

### 2️⃣ View Data Test
```
1. After login, select [2] View All Transactions
2. You should see 15 transactions displayed
3. Check dashboard shows: Income $7,500, Expenses $5,450, Balance $2,050
```

### 3️⃣ Monthly Report Test
```
1. Select [10] Monthly Reports
2. Select October 2024 (should find 2 transactions)
3. Verify: Income $0, Expenses $1,800
4. Most spent category should be "Other" ($1,200)
```

### 4️⃣ Category Breakdown Test
```
1. Select [11] Category Breakdown
2. Should show all 4 categories with visual bars
3. Food: $600, Transport: $850, Entertainment: $2,100, Other: $2,000
```

### 5️⃣ Spending Trends Test
```
1. Select [12] Spending Trends
2. Should show 6 months of data
3. Highest: October 2024 ($1,800)
4. Visual chart with bars and 🔥 indicators
```

### 6️⃣ Recurring Transactions Test
```
1. Select [13] Recurring Transactions
2. View existing (should show 5 recurring transactions)
3. Try adding a new one
4. Check if auto-creation works for due dates
```

### 7️⃣ CSV Export Test
```
1. Select [14] Export Transactions to CSV
2. Check file created: TestUser_transactions.csv
3. Open in Excel/text editor to verify format
```

### 8️⃣ CSV Import Test
```
1. First, delete a transaction (option [4])
2. Select [15] Import Transactions from CSV
3. Uses pre-made TestUser_transactions.csv
4. Check if December 2024 transactions are added
```

### 9️⃣ Filter & Sort Test
```
1. [6] Filter by Category → Food (should find 3)
2. [7] Filter by Amount → $0-$100 (should find smaller ones)
3. [5] Search by Date → 2024-06-01 to 2024-08-31 (summer)
4. [8] Sort Results → by amount (descending)
```

### 🔟 Monthly Budget Test
```
1. Select [9] Monthly Budget Tracker
2. Should show current month's spending
3. Compare against budget limit
4. Check if over/under budget indicator shows
```

---

## 🐛 Things to Watch For

### Potential Issues:
- [ ] Does `number_of_transactions` update correctly?
- [ ] Do backup files get created?
- [ ] Are recurring transactions auto-created on next_date?
- [ ] Does CSV import handle date/amount conversions?
- [ ] Do monthly expenses track correctly in users.json?

### Expected Behaviors:
- ✅ Dashboard should update after each transaction
- ✅ Deleting transaction should reduce count
- ✅ Editing transaction should preserve ID
- ✅ Reports should show accurate calculations
- ✅ Visual bars should scale proportionally

---

## 💡 Testing Tips

1. **Start Fresh:** Test with clean TestUser first before making changes
2. **Check Files:** After each operation, check JSON files to verify changes
3. **Test Invalid Input:** Try wrong passwords, non-existent IDs, invalid dates
4. **Test Edge Cases:** Empty filters, future dates, negative amounts
5. **Test Flow:** Complete full workflows (add → edit → delete → import)

---

## 📝 Bug Reporting Template

If you find issues, document them like this:

```
**Bug:** [Brief description]
**Steps to Reproduce:**
1. Login as TestUser
2. Select option X
3. Do Y
4. See error Z

**Expected:** What should happen
**Actual:** What actually happened
**Files Affected:** Which JSON files changed incorrectly
**Error Message:** Copy exact error if any
```

---

## ✅ Quick Validation Checklist

After each test session, verify:
- [ ] transactions_TestUser_999.json has correct transaction count
- [ ] users.json shows updated balance and number_of_transactions
- [ ] Backup files exist in data/transactions folder
- [ ] No crashes or unhandled exceptions occurred
- [ ] Data persists after restarting the program

---

## 🎓 Learning Opportunity

This test setup demonstrates:
- **Authentication** with hashed passwords (SHA256)
- **CRUD operations** on JSON files
- **Data persistence** across sessions
- **Financial calculations** and aggregations
- **CSV import/export** for data portability
- **Recurring transaction automation**
- **Data visualization** with text-based charts

---

## 🚀 Ready to Test!

You now have everything needed to thoroughly test the Personal Finance Manager!

**Start by:** Running `python main.py` and logging in with TestUser / Test123!@#

**Happy Testing! 🎉**
