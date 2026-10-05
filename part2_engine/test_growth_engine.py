from growth_engine import (
    mom_growth,
    is_flagged,
    validate_feed,
)


# -----------------------------------------------------
# TEST 1
# GIVEN April → May Ethnic Wear
# WHEN growth is calculated
# THEN result is 77.1 and flagged
# -----------------------------------------------------
growth = mom_growth(104520.77, 185107.61)
assert growth == 77.1
assert is_flagged(growth) == "flagged"


# -----------------------------------------------------
# TEST 2
# GIVEN May → June Beauty & Personal Care
# THEN growth is 5.67 and not flagged
# -----------------------------------------------------
growth = mom_growth(35542.11, 37559.07)
assert growth == 5.67
assert is_flagged(growth) == "not_flagged"


# -----------------------------------------------------
# TEST 3
# GIVEN exactly 8% growth
# THEN boundary escalation happens
# -----------------------------------------------------
growth = mom_growth(100000, 108000)
assert growth == 8.0
assert is_flagged(growth) == "escalate_exact_boundary"


# -----------------------------------------------------
# TEST 4
# GIVEN corrupted CSV
# THEN validation returns exactly 3 errors
# -----------------------------------------------------
valid, errors = validate_feed("fixtures/corrupted_feed.csv")

assert valid is False

expected_errors = [
    "line 3: negative revenue (-4200.0) for category=Western Wear",
    "line 4: missing category (month=July)",
    "line 6: missing revenue (category=Home & Kitchen)",
]

assert errors == expected_errors


# -----------------------------------------------------
# TEST 5 (Bonus required by assignment)
# GIVEN valid monthly revenue feed
# THEN validation passes
# -----------------------------------------------------
valid, errors = validate_feed("fixtures/monthly_category_revenue.csv")

assert valid is True
assert errors == []

print("All Part 2 tests passed successfully!")