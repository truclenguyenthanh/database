* Student Database Management Application

** Description
This application is a simple console-based system for managing a student database. It allows for basic CRUD (Create, Read, Update, Delete) operations on a PostgreSQL database.

** Repository Structure
/src - Contains the source code of the application.
/scripts - Contains SQL scripts for database setup.
README.md - Instructions and information about the application.

** Setup Instructions
*** Prerequisites
    Python 3.x
    PostgreSQL
    psycopg2 (Python library)

*** Database Setup
    Install PostgreSQL on your system.
    Create a new PostgreSQL database.
    Run the SQL script in /scripts/setup.sql to create and initialize the students table.

*** Application Setup 
    Clone the repository to your local machine.
    Install psycopg2 using pip install psycopg2.
    Navigate to the /src directory.
    Update the database connection parameters in app.py to match your PostgreSQL setup.

** How to Run the Application
    Open a terminal or command prompt.
    Navigate to the /src directory.
    Run the application using the command: python app.py.
    Use the console menu to interact with the application.

** Application Functions
    reset_database(): Resets the students table to its initial state with predefined data.
    create_connection(): Establishes a connection to the PostgreSQL database.
    getAllStudents(): Retrieves and displays all student records from the database.
    addStudent(): Adds a new student record to the database. Includes input validation for each field.
    updateStudentEmail(): Updates the email address for a student, identified by their student ID. Includes input validation.
    deleteStudent(): Deletes the record of a student, identified by their student ID.
    menu(): Displays the main menu of the application and handles user input to call other functions.

** Additional Notes
Ensure that PostgreSQL is running before starting the application.
This application is designed for educational purposes and should be used in a development or testing environment.
