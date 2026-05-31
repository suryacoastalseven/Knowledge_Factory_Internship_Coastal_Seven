# System Architecture & Design Basics

## 1. Introduction
System design is the process of defining the architecture, components, modules, interfaces, and data for a system to satisfy specified requirements.

## 2. The 3-Tier Architecture (Frontend / Backend / Database)
Most modern applications use a 3-tier architecture to keep the system modular and scalable.

### A. Presentation Tier (Frontend)
- **Role:** This is what the user interacts with (User Interface). 
- **Technologies:** HTML, CSS, JavaScript, React, Angular, or even a Command Line Interface (CLI).
- **Communication:** Sends requests to the Backend via REST APIs.

### B. Logic Tier (Backend / Application Layer)
- **Role:** The brain of the application. It processes frontend requests, runs business logic, performs validations, and communicates with the database or external APIs (like OpenAI).
- **Technologies:** Python, Django, FastAPI, Node.js, Java.

### C. Data Tier (Database)
- **Role:** Stores and manages the application's data securely.
- **Technologies:** 
  - Relational: PostgreSQL, MySQL.
  - NoSQL: MongoDB, Redis.
  - Files: JSON, CSV (for simple mini-projects).

## 3. How They Connect (Workflow)
1. **User** clicks a button on the **Frontend**.
2. **Frontend** sends an HTTP request (GET/POST) to the **Backend**.
3. **Backend** processes the request, asks the **Database** for required data.
4. **Database** returns the data to the Backend.
5. **Backend** formats the data (usually as JSON) and sends it back to the Frontend.
6. **Frontend** displays the result to the user.

*(Prepared for Knowledge Factory Internship - Day 5)*