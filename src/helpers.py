SHORTNAMES = {
    ' - привилегированные акции': '-П',
    ' - акции привилегированные': '-П',
}


def short_name(name: str) -> str:
    for long_part, short_part in SHORTNAMES.items():
        name = name.replace(long_part, short_part)

    return name


def get_percentage_diff(a: float, b: float) -> float:
    """Return percentage different between two float digits

    Positive result means that b > a at result value
    Negative result means that b < a at result value
    """
    return (b - a) / a


def remove_zero_fractional(number: float) -> str:
    return '{:g}'.format(number)


def format_percentage(number: float) -> str:
    return '{:.1%}'.format(number)


def format_thousand_separator(number: float) -> str:
    return '{:,}'.format(number).replace(',', ' ')


def remove_negative_from_zero_number(number: int or float) -> int or float:
    return number if abs(number) else abs(number)


if __name__ == '__main__':
    print(short_name('Газпром - привилегированные акции'))
    pass
