# src/utils/constants.py

# This file contains system-wide constants that can be easily changed.
# This practice avoids "magic numbers" in the code, making it more readable
# and maintainable, as discussed in Module 4 of the course.

# --- Data Persistence ---
DATA_FILE = 'library_data.json'

# --- Loan Policies ---
LOAN_PERIOD_DAYS = 14  # The number of days a book can be borrowed.
MAX_BORROW_LIMIT = 5   # The maximum number of books a member can borrow at one time.

# --- Fine Policies ---
# We can add fine-related constants here later.
# For example:
# DAILY_FINE_RATE = 0.25
# MAX_FINE_AMOUNT = 10.00