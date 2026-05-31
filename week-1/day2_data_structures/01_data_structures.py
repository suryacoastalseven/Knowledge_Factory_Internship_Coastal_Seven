# 01_data_structures.py

def manage_company_data():
    # 1. Tuple (Immutable - మార్చలేని డేటా కోసం వాడుతాం. ఉదాహరణకు: Server Config)
    db_config = ("localhost", 5432, "admin")
    print(f"Database connected at {db_config[0]}:{db_config[1]}\n")

    # 2. List of Dictionaries (Employees data)
    employees = [
        {"id": 1, "name": "Ravi", "department": "IT", "salary": 60000},
        {"id": 2, "name": "Sita", "department": "HR", "salary": 50000},
        {"id": 3, "name": "John", "department": "IT", "salary": 65000},
        {"id": 4, "name": "Ali", "department": "Finance", "salary": 70000}
    ]

    # 3. Set (Unique values కోసం వాడుతాం. డూప్లికేట్స్ తీసేస్తుంది)
    # కంపెనీలో ఉన్న డిపార్ట్మెంట్స్ ఏంటో తెలుసుకోవడానికి:
    departments = set()
    for emp in employees:
        departments.add(emp["department"])
    print(f"Unique Departments in Company: {departments}\n")

    # 4. List Comprehension (ఒకే లైన్ లో లిస్ట్ క్రియేట్ చేయడం - Pythonic way)
    # 60000 కన్నా ఎక్కువ శాలరీ ఉన్న వాళ్ళ పేర్లు:
    high_earners = [emp["name"] for emp in employees if emp["salary"] > 60000]
    print(f"High Earners: {high_earners}\n")

    # 5. Dictionary Comprehension (ఒకే లైన్ లో డిక్షనరీ క్రియేట్ చేయడం)
    # Employee ID ని Key లాగా, Name ని Value లాగా మారుద్దాం:
    emp_dict = {emp["id"]: emp["name"] for emp in employees}
    print(f"Employee ID to Name Mapping: {emp_dict}\n")

manage_company_data()