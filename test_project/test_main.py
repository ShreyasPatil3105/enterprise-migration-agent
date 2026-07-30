from main import calculate_area
import math

def test_area():
    assert calculate_area(5) == math.pi * 25
