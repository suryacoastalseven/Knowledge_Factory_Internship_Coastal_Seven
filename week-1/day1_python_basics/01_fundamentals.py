# 01_fundamentals.py

def analyze_student_marks():
    # Variables and Data Types
    student_name = "Ravi"  # String
    marks = [45, 85, 90, 30, 75]  # List of ints
    is_passed = True  # Boolean
    
    print(f"--- Analyzing marks for {student_name} ---")
    
    # Loop & Conditions
    for mark in marks:
        if mark >= 80:
            print(f"Score: {mark} - Grade: A (Excellent)")
        elif mark >= 50:
            print(f"Score: {mark} - Grade: B (Good)")
        else:
            print(f"Score: {mark} - Grade: F (Fail)")
            is_passed = False
            
    # Final Result
    if is_passed:
        print("Final Result: Student Passed all subjects!")
    else:
        print("Final Result: Student Failed in some subjects.")

# Calling the function
analyze_student_marks()