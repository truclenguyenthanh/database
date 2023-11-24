import psycopg2
import re
from psycopg2 import sql
from datetime import datetime

# Database connection parameters
db_params = {
    'dbname': 'students',
    'user': 'postgres',
    'password': 'postgres',
    'host': '127.0.0.1'
}

# Function to create a database connection
def create_connection():
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as e:
        print(f"Error creating connection: {e}")
        return None

# Function to get all students
def getAllStudents():
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM students;")
                records = cur.fetchall()
                for record in records:
                    print(record)
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            conn.close()

# Input validation functions
def validate_name(name):
    return re.match("^[A-Za-z\s]+$", name) is not None

def validate_email(email):
    return re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def emailExists(email):
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS(SELECT 1 FROM students WHERE email = %s);", (email,))
                return cur.fetchone()[0]
        except Exception as e:
            print(f"Error checking email: {e}")
        finally:
            conn.close()
    return False

# Function to add a new student with validation
def addStudent():
    while True:
        first_name = input("Enter first name: ")
        if validate_name(first_name):
            break
        print("Invalid first name. Please use only letters and spaces.")

    while True:
        last_name = input("Enter last name: ")
        if validate_name(last_name):
            break
        print("Invalid last name. Please use only letters and spaces.")

    while True:
        email = input("Enter email: ")
        if not validate_email(email):
            print("Invalid email format.")
            continue

        if emailExists(email):
            print("This email is already in use. Please enter a different email.")
            continue
        break

    while True:
        enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
        if validate_date(enrollment_date):
            break
        print("Invalid date format. Please use YYYY-MM-DD.")

    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);", 
                            (first_name, last_name, email, enrollment_date))
                conn.commit()
        except Exception as e:
            print(f"Error adding student: {e}")
        finally:
            conn.close()

# Function to update a student's email with validation
def updateStudentEmail():
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                while True:
                    student_id = input("Enter student ID to update: ")
                    if not student_id.isdigit():
                        print("Invalid student ID. Please enter a numeric value.")
                        continue

                    # Check if the student ID exists in the database
                    cur.execute("SELECT EXISTS(SELECT 1 FROM students WHERE student_id = %s);", (student_id,))
                    exists = cur.fetchone()[0]
                    if not exists:
                        print("No student found with that ID. Please try again.")
                        continue

                    break

                while True:
                    new_email = input("Enter new email: ")
                    if not validate_email(new_email):
                        print("Invalid email format.")
                        continue

                    if emailExists(new_email):
                        print("This email is already in use. Please enter a different email.")
                        continue
                    
                    break

                # Perform the update
                cur.execute("UPDATE students SET email = %s WHERE student_id = %s;", (new_email, student_id))
                conn.commit()
                print("Student email updated successfully.")

        except Exception as e:
            print(f"Error updating student email: {e}")
        finally:
            conn.close()

# Function to delete a student
def deleteStudent():
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                while True:
                    student_id = input("Enter student ID to delete: ")
                    if not student_id.isdigit():
                        print("Invalid student ID. Please enter a numeric value.")
                        continue

                    # Check if the student ID exists in the database
                    cur.execute("SELECT EXISTS(SELECT 1 FROM students WHERE student_id = %s);", (student_id,))
                    exists = cur.fetchone()[0]
                    if not exists:
                        print("No student found with that ID. Please try again.")
                        continue
                    break
                    
                # Perform the delete
                cur.execute("DELETE FROM students WHERE student_id = %s;", 
                            (student_id,))
                conn.commit()
        except Exception as e:
            print(f"Error deleting student: {e}")
        finally:
            conn.close()

# Function to reset the database to its initial state
def reset_database():
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Truncate the table and restart the ID sequence
                cur.execute("TRUNCATE TABLE students RESTART IDENTITY;")

                # Re-insert the initial data
                cur.execute("""
                    INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
                    ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
                    ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
                    ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
                """)
                conn.commit()
                print("Database has been reset to its initial state.")
        except Exception as e:
            print(f"Error resetting database: {e}")
        finally:
            conn.close()


# Function to display the menu and handle user input
def menu():
    while True:
        print("\nStudent Database Management")
        print("1. View All Students")
        print("2. Add New Student")
        print("3. Update Student Email")
        print("4. Delete Student")
        print("5. Reset the database")
        print("6. Exit")

        choice = input("Enter choice (1-5): ")

        if choice == '1':
            getAllStudents()
        elif choice == '2':
            addStudent()
        elif choice == '3':
            updateStudentEmail()
        elif choice == '4':
            deleteStudent()
        elif choice == '5':
            reset_database()
        elif choice == '6':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please enter a number between 1-5.")

if __name__ == "__main__":
    menu()