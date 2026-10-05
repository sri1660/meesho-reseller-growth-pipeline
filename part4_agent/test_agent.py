import os

from mock_agent_runner import run_agent


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

VALID_FEED = os.path.join(
    BASE_DIR,
    "part2_engine",
    "fixtures",
    "monthly_category_revenue.csv"
)

CORRUPTED_FEED = os.path.join(
    BASE_DIR,
    "part2_engine",
    "fixtures",
    "corrupted_feed.csv"
)


def test_valid_feed():
    result = run_agent(VALID_FEED)

    assert result["status"] == "success"
    assert len(result["flagged_categories"]) <= 3

    for item in result["flagged_categories"]:
        assert item["classification"] == "flagged"


def test_corrupted_feed():
    result = run_agent(CORRUPTED_FEED)

    assert result["status"] == "validation_failed"
    assert len(result["errors"]) == 3
    assert result["flagged_categories"] == []


if __name__ == "__main__":
    test_valid_feed()
    test_corrupted_feed()

    print("All Part 4 agent tests passed successfully.")