def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(
    text: str,
    reseller_names: list[str]
) -> bool:
    """
    Returns False if any raw reseller name
    appears inside the supplied text.
    """
    for name in reseller_names:
        if name in text:
            return False

    return True


if __name__ == "__main__":

    reseller_names = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5"
    ]

    print("Alias tests:")

    print(alias_for("RS019"))
    print(alias_for("RS006"))

    safe_text = (
        "West region reseller ALIAS-19 "
        "showed strong performance."
    )

    unsafe_text = (
        "Mumbai Reseller 1 showed strong performance."
    )

    print("\nPrivacy tests:")

    print(
        "Safe text:",
        assert_no_raw_names_leak(
            safe_text,
            reseller_names
        )
    )

    print(
        "Unsafe text:",
        assert_no_raw_names_leak(
            unsafe_text,
            reseller_names
        )
    )