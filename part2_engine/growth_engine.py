import csv


def mom_growth(previous: float, current: float) -> float:
    """
    Calculate Month-on-Month growth percentage.
    """
    return round(((current - previous) / previous) * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """
    Decide whether growth crosses threshold.
    """
    if abs(mom_pct) > threshold:
        return "flagged"
    elif abs(mom_pct) < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"


def validate_feed(csv_path: str):
    """
    Validate monthly revenue feed.

    Returns:
        (True, []) if valid.
        (False, [errors]) if invalid.
    """
    errors = []

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Header is line 1.
        for index, row in enumerate(reader, start=2):
            month = row["month"]
            category = row["category"]
            revenue = row["revenue"]

            # Missing category
            if category.strip() == "":
                errors.append(
                    f"line {index}: missing category (month={month})"
                )

            # Missing revenue
            if revenue.strip() == "":
                errors.append(
                    f"line {index}: missing revenue (category={category})"
                )
                continue

            # Revenue numeric check
            try:
                revenue_value = float(revenue)
            except ValueError:
                errors.append(
                    f"line {index}: revenue not numeric: {revenue!r}"
                )
                continue

            # Negative revenue
            if revenue_value < 0:
                errors.append(
                    f"line {index}: negative revenue ({revenue_value}) for category={category}"
                )

    return (len(errors) == 0, errors)