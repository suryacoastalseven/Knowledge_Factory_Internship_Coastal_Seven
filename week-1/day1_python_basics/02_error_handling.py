# 02_error_handling.py

def divide_numbers(a: float, b: float):
    # Type hints (a: float, b: float) వాడటం వల్ల ప్రొఫెషనల్ గా కనిపిస్తుంది
    try:
        result = a / b
        print(f"The result of {a} / {b} is: {result}")
    except ZeroDivisionError as e:
        # Stack trace ని అర్థం చేసుకోవడం మరియు హ్యాండిల్ చేయడం
        print(f"Error: Cannot divide by zero! System message: {e}")
    except TypeError as e:
        print(f"Error: Please provide numbers only. System message: {e}")
    finally:
        print("Execution of divide_numbers function completed.\n")

# Testing with good data
divide_numbers(10, 2)

# Testing with edge cases (Errors)
divide_numbers(10, 0) # This will trigger ZeroDivisionError
divide_numbers(10, "two") # This will trigger TypeError