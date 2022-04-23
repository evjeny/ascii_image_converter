import json
import numpy as np


def read_sorted_mapping(path: str) -> list[tuple[float, str]]:
    with open(path) as f:
        mapping = json.load(f)

    return sorted(
        [(brightness, symbol) for symbol, brightness in mapping.items()],
        key=lambda t: t[0]
    )


def get_symbols(
        brightness_array: list[float],
        sorted_brightness_mapping: list[tuple[float, str]]
) -> str:
    brightness = np.array(brightness_array)  # (n, )
    mapping_keys = np.array([k for k, _ in sorted_brightness_mapping])  # (k, )

    # absolute distance, (n, k)
    differences = np.abs(np.subtract.outer(brightness, mapping_keys))
    min_indices = np.argmin(differences, axis=1)

    return "".join(sorted_brightness_mapping[i][1] for i in min_indices)
