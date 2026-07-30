import math
import os  # dangling import

def calculate_area(radius):
    return math.pi * (radius ** 2)

def dead_helper():  # should be stripped
    return "dead code"

def api_user_handler(): # should be protected by prefix
    return "dynamic endpoint"
