# main.py
# వేరే ఫైల్ (math_operations.py) నుండి Calculator క్లాస్ ని లాగుతున్నాం. ఇదే Modular Coding!
from math_operations import Calculator

print("--- Modular Coding Example ---")
sum_result = Calculator.add(10, 5)
mul_result = Calculator.multiply(10, 5)

print(f"Addition Result: {sum_result}")
print(f"Multiplication Result: {mul_result}")