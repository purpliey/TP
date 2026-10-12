# teste/test_decode.py
# Fistic Viorelia, SI-265
from arsenal.forensics.decode import desfa


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_hex():
    strat, b = desfa("48656c6c6f")
    assert strat == "hex"
    assert b == b"Hello"


def test_url():
    strat, b = desfa("%2Fetc")
    assert strat == "url"
    assert b == b"/etc"
