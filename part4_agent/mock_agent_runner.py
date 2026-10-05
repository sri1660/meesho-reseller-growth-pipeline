import csv
import json
import os
import sys

PART2_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "part2_engine"
)

sys.path.insert(0, os.path.abspath(PART2_PATH))

from growth_engine import mom_growth, is_flagged, validate_feed


def load_feed(csv_path):
    rows = []

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return rows


def calculate_growth(rows):
    grouped = {}

    for row in rows:
        category = row["category"].strip()
        month = row["month"].strip()
        revenue = float(row["revenue"])

        grouped.setdefault(category, {})
        grouped[category][month] = revenue

    return grouped


def find_months(grouped):
    months = []

    for category_data in grouped.values():
        for month in category_data:
            if month not in months:
                months.append(month)

    return months


def run_agent(csv_path):
    valid, errors = validate_feed(csv_path)

    if not valid:
        return {
            "status": "validation_failed",
            "file": os.path.basename(csv_path),
            "errors": errors,
            "flagged_categories": []
        }

    rows = load_feed(csv_path)
    grouped = calculate_growth(rows)

    months = find_months(grouped)

    if len(months) < 2:
        return {
            "status": "error",
            "file": os.path.basename(csv_path),
            "errors": ["At least two months are required."],
            "flagged_categories": []
        }

    previous_month = months[-2]
    current_month = months[-1]

    flagged = []

    for category, month_data in grouped.items():

        if previous_month not in month_data:
            continue

        if current_month not in month_data:
            continue

        previous_revenue = month_data[previous_month]
        current_revenue = month_data[current_month]

        mom_pct = mom_growth(
            previous_revenue,
            current_revenue
        )

        classification = is_flagged(mom_pct)

        if classification == "flagged":
            flagged.append({
                "category": category,
                "previous_month": previous_month,
                "current_month": current_month,
                "previous_revenue": previous_revenue,
                "current_revenue": current_revenue,
                "mom_pct": mom_pct,
                "classification": classification
            })

    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True
    )

    top_3 = flagged[:3]

    return {
        "status": "success",
        "file": os.path.basename(csv_path),
        "previous_month": previous_month,
        "current_month": current_month,
        "flagged_categories": top_3
    }


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Usage: python mock_agent_runner.py <csv_file>"
        )
        sys.exit(1)

    csv_path = sys.argv[1]

    result = run_agent(csv_path)

    print(json.dumps(result, indent=2))