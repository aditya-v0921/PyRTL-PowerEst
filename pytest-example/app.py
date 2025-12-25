# app.py

from typing import Iterable, List, Union

Number = Union[int, float]


def normalize_name(name: str) -> str:
    """
    Trim leading/trailing whitespace, collapse internal spaces to one,
    and title-case each word. Keeps hyphens/apostrophes within words.
    Examples:
      "   alice   o'neill  " -> "Alice O'Neill"
      "anne-marie   smith"  -> "Anne-Marie Smith"
    Raises:
      TypeError  - if name is not a str
      ValueError - if name is empty/only whitespace after trimming
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    stripped = name.strip()
    if not stripped:
        raise ValueError("name cannot be empty")

    # collapse spaces
    parts = stripped.split()
    collapsed = " ".join(parts)

    # title-case while preserving internal punctuation like '-' and "'"
    def _smart_title(token: str) -> str:
        # Title-case each subpart split by hyphen/apostrophe and rejoin
        out = []
        i = 0
        while i < len(token):
            if token[i] in "-'":
                out.append(token[i])
                i += 1
                continue
            # grab a run of letters until punctuation or end
            j = i
            while j < len(token) and token[j] not in "-'":
                j += 1
            chunk = token[i:j]
            out.append(chunk[:1].upper() + chunk[1:].lower())
            i = j
        return "".join(out)

    return " ".join(_smart_title(t) for t in collapsed.split(" "))


def is_prime(n: int) -> bool:
    """
    Basic primality test for non-negative integers.
    Returns False for n < 2. Efficient up to reasonable sizes.
    """
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def safe_divide(a: Number, b: Number, precision: int = 2, as_str: bool = False):
    """
    Divide a by b with simple error handling.
    - If b == 0, return None (instead of raising).
    - Round to 'precision' decimal places.
    - If as_str=True, return a string with fixed decimals (e.g., '3.14').
    Raises:
      TypeError - if inputs are not int/float or precision is negative
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("a and b must be numbers")
    if not isinstance(precision, int) or precision < 0:
        raise TypeError("precision must be a non-negative int")

    if b == 0:
        return None

    result = a / b
    result = round(result, precision)
    if as_str:
        return f"{result:.{precision}f}"
    return result


def compute_grade(scores: Iterable[int]) -> str:
    """
    Compute a letter grade from integer scores (0-100).
    Rules:
      - scores must be a non-empty iterable of ints in [0, 100]
      - if there are 5 or more scores, drop the single lowest score
      - average is arithmetic mean (float, no extra rounding)
      - thresholds: A>=90, B>=80, C>=70, D>=60, else F
    Raises:
      TypeError  - if scores is not iterable
      ValueError - if empty or contains invalid values
    """
    if scores is None:
        raise TypeError("scores must be an iterable of ints")

    try:
        vals: List[int] = list(scores)
    except TypeError:
        raise TypeError("scores must be an iterable of ints")

    if not vals:
        raise ValueError("scores cannot be empty")

    for v in vals:
        if not isinstance(v, int):
            raise ValueError("all scores must be ints")
        if v < 0 or v > 100:
            raise ValueError("scores must be between 0 and 100")

    # drop the single lowest if 5 or more
    working = vals.copy()
    if len(working) >= 5:
        working.remove(min(working))

    avg = sum(working) / len(working)

    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def find_median(nums: Iterable[Number]) -> Number:
    """
    Return the median of a non-empty iterable of numbers.
    - Works for ints/floats, negatives allowed.
    - Does not mutate the input (it makes a sorted copy).
    Raises:
      TypeError  - if nums is not iterable
      ValueError - if empty
    """
    if nums is None:
        raise TypeError("nums must be an iterable")

    try:
        data = list(nums)
    except TypeError:
        raise TypeError("nums must be an iterable")

    if not data:
        raise ValueError("nums cannot be empty")

    sorted_copy = sorted(data)
    n = len(sorted_copy)
    mid = n // 2
    if n % 2 == 1:
        return sorted_copy[mid]
    return (sorted_copy[mid - 1] + sorted_copy[mid]) / 2