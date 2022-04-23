from brightness_levels import get_symbols

mapping = [
    (0.0, " "), (0.1, "."), (0.2, ";"), (0.3, "i"), (0.4, "l"), (0.5, "t"),
    (0.6, "c"), (0.7, "a"), (0.8, "d"), (0.9, "q"), (1.0, "w")
]


def test_exact_mapping():
    assert get_symbols(
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        mapping
    ) == " .;iltcadqw"


def test_between_symbols():
    for ((b1, s1), (b2, s2)) in zip(mapping[:-1], mapping[1:]):
        assert get_symbols([(b1 + b2) / 2], mapping) in (s1, s2)


def test_closest():
    for b, s in mapping:
        assert get_symbols([b + 0.03], mapping) == s
        assert get_symbols([b - 0.03], mapping) == s
