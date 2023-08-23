from pathlib import Path

import pytest
from rich import print

SAMPLE_INPUT = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000\
"""
EXPECTED = 24000

data = (Path(__file__).parent / "input.txt").read_text()


def parse_input(_input: str) -> str:
    return "str"


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    assert parse_input(_input) == expected


if __name__ == "__main__":
    print(f"Input:{parse_input(data)}")
