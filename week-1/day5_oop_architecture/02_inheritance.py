# 02_inheritance.py

# Parent Class (Base)
class Employee:
    def __init__(self, name: str, salary: int):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"{self.name} earns ${self.salary}"

# Child Class (Inherits from Employee)
class Developer(Employee):
    def __init__(self, name: str, salary: int, programming_language: str):
        super().__init__(name, salary) # Parent class కి డేటా పంపుతున్నాం
        self.programming_language = programming_language

    # Method Overriding
    def get_details(self):
        return f"{self.name} is a Developer coding in {self.programming_language} and earns ${self.salary}"

# Testing Inheritance
print("--- OOP Inheritance ---")
emp1 = Employee("Rahul", 50000)
dev1 = Developer("Surya", 80000, "Python")

print(emp1.get_details())
print(dev1.get_details())