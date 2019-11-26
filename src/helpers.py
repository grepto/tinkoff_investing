SHORTNAMES = {
    ' - привилегированные акции': '-П',
}


def short_name(name: str) -> str:
    for long_part, short_part in SHORTNAMES.items():
        shorten_name = name.replace(long_part, short_part)

    return shorten_name


def get_percentage_diff(a: float, b: float) -> float:
    """Return percentage different between two float digits

    Positive result means that b > a at result value
    Negative result means that b < a at result value
    """
    return (b - a) / a


if __name__ == '__main__':
    # print(get_percentage_diff(1656.5, 1748))
    pass
