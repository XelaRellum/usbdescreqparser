from pytest import mark
from usbdescreqparser import Parser

with open("testdata/stddesc-hex.txt", "r", encoding="utf-8") as file:
    stddesc_hex = file.read()

with open("testdata/stddesc-expected.txt", "r", encoding="utf-8") as file:
    stddesc_expected = file.read().rstrip()

def test_best_guess():
    parser = Parser()
    actual = parser.best_guess(stddesc_hex)

    assert actual == stddesc_expected
