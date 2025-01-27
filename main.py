import psycopg2
from psycopg2 import Error
import sys

# Database connection parameters
DB_NAME = "student_grades"
DB_USER = "grade_user"     # Changed from pg_user
DB_PASSWORD = "grade_password"
DB_HOST = "localhost"

def connect():
    """Connect to PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        sys.exit(1)

def display_menu():
    """Display CLI menu."""
    print("\nPGradeTracker Menu:")
    print("1. Add Student")
    print("2. Add Course")
    print("3. Add Grade")
    print("4. View All Students")
    print("5. View All Courses")
    print("6. View Grades for a Student")
    print("7. Calculate Student Average")
    print("8. Exit")

def add_student(conn):
    """Add a student to the database."""
    name = input("Enter student name: ")
    email = input("Enter student email: ")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, email) VALUES (%s, %s)",
            (name, email)
        )
        conn.commit()
        print("Student added successfully!")
    except Error as e:
        conn.rollback()  # Reset the transaction
        print(f"Error adding student: {e}")

def add_course(conn):
    """Add a course to the database."""
    name = input("Enter course name: ")
    instructor = input("Enter instructor name: ")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (name, instructor) VALUES (%s, %s)",
            (name, instructor)
        )
        conn.commit()
        print("Course added successfully!")
    except Error as e:
        conn.rollback()  # Reset the transaction
        print(f"Error adding course: {e}")

def add_grade(conn):
    """Add a grade for a student in a course."""
    student_id = input("Enter student ID: ")
    course_id = input("Enter course ID: ")
    grade = input("Enter grade (0-100): ")
    semester = input("Enter semester (e.g., Fall 2023): ")
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO grades (student_id, course_id, grade, semester)
               VALUES (%s, %s, %s, %s)""",
            (student_id, course_id, grade, semester)
        )
        conn.commit()
        print("Grade added successfully!")
    except Error as e:
        print(f"Error adding grade: {e}")

def view_students(conn):
    """View all students."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        print("\nStudents:")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]}, Email: {student[2]}")
    except Error as e:
        conn.rollback()  # Reset the transaction
        print(f"Error fetching students: {e}")

def view_courses(conn):
    """View all courses."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        print("\nCourses:")
        for course in courses:
            print(f"ID: {course[0]}, Name: {course[1]}, Instructor: {course[2]}")
    except Error as e:
        conn.rollback()
        print(f"Error fetching courses: {e}")

def view_grades_for_student(conn):
    """View grades for a specific student."""
    student_id = input("Enter student ID: ")
    try:
        cursor = conn.cursor()
        # Join with courses to show course names instead of IDs
        cursor.execute("""
            SELECT courses.name, grades.grade, grades.semester 
            FROM grades 
            INNER JOIN courses ON grades.course_id = courses.course_id 
            WHERE grades.student_id = %s
        """, (student_id,))
        grades = cursor.fetchall()
        if not grades:
            print(f"No grades found for student ID {student_id}.")
            return
        print(f"\nGrades for Student ID {student_id}:")
        for grade in grades:
            print(f"Course: {grade[0]}, Grade: {grade[1]}, Semester: {grade[2]}")
    except Error as e:
        conn.rollback()
        print(f"Error fetching grades: {e}")

def calculate_average(conn):
    """Calculate average grade for a student."""
    student_id = input("Enter student ID: ")
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT AVG(grade) FROM grades
               WHERE student_id = %s""",
            (student_id,)
        )
        average = cursor.fetchone()[0]
        print(f"\nAverage grade for student {student_id}: {average:.2f}")
    except Error as e:
        print(f"Error calculating average: {e}")

def main():
    conn = connect()
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")
        if choice == "1":
            add_student(conn)
        elif choice == "2":
            add_course(conn)
        elif choice == "3":
            add_grade(conn)
        elif choice == "4":
            view_students(conn)
        elif choice == "5":
            view_courses(conn)  # Fixed: Call view_courses
        elif choice == "6":
            view_grades_for_student(conn)  # Fixed: Call view_grades
        elif choice == "7":
            calculate_average(conn)
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
    conn.close()
    
if __name__ == "__main__":
    main()