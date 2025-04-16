from typing import List, Union

def print_array(arr: List[Union[str, int, float, bool]], show_index: bool = True, from_index: int = 0, to_index: int = None):
    to_index = len(arr) - 1 if to_index is None else to_index
    for i in range(from_index, to_index + 1):
        if i < len(arr):
            value = arr[i]
            if show_index:
                print(f"{i}: {value}")
            else:
                print(f"{value}")

def print_series(series: List[str], skip_na: bool = False, show_index: bool = True, from_index: int = 0, to_index: int = None):
    to_index = len(series) - 1 if to_index is None else to_index
    for i in range(from_index, to_index + 1):
        if i < len(series):
            val = series[i]
            if skip_na and val in ["NaN", "None", None]:
                continue
            if show_index:
                print(f"{i}: {val}")
            else:
                print(f"{val}")

def print_value(value: Union[str, int, float, bool]):
    print(str(value))

def bool_to_int_arr(arr: List[bool]) -> List[int]:
    return [i for i, val in enumerate(arr) if val]

def int_to_bool_arr(arr: List[int], n: int) -> List[bool]:
    result = [False] * n
    for i in arr:
        if 0 <= i < n:
            result[i] = True
    return result




