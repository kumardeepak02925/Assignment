import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clean_data import validate_email, parse_date


def test_valid_email():
    assert validate_email("user@example.com") == True


def test_invalid_email():
    assert validate_email("invalidemail") == False


def test_parse_date():
    d = parse_date("2023-01-10")
    assert str(d.date()) == "2023-01-10"