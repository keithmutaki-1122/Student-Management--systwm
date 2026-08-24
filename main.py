import json
import os
import getpass

STUDENT_FILE = "students.json"

# Default login details
USERNAME = "admin"
PASSWORD = "1234"

students = []


# =========================================================
# FILE HANDLING
# =========================================================

def save_students():
    try:
        with open(STUDENT_FILE, "w") as file:
            json.dump(students, file, indent=4)
    except Exception as error:
        print("Error saving students:", error)


def load_students():
    global students

    try:
        if os.path.exists(STUDENT_FILE):
            with open(STUDENT_FILE, "r") as file:
                students = json.load(file)
        else:
            students = []

    except (json.JSONDecodeError, FileNotFoundError):
        students = []


# =========================================================
# VALIDATION
# =========================================================

def get_non_empty_input(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Input cannot be empty. Please try again.")


def get_mark(message):
    while True:
        try:
            mark = float(input(message))

            if 0 <= mark <= 100:
                return mark

            print("Mark must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


# =========================================================
# GRADE CALCULATION
# =========================================================

def calculate_grade(average):

    if average >= 80:
        return "A"

    elif average >= 70:
        return "B"

    elif average >= 60:
        return "C"

    elif average >= 50:
        return "D"

    else:
        return "E"


# =========================================================
# FIND STUDENT
# =========================================================

def find_student(admission):

    for student in students:

        if student["admission"] == admission:
            return student

    return None


# =========================================================
# ADD STUDENT
# =========================================================

def add_student():

    print("\n========== ADD STUDENT ==========")

    name = get_non_empty_input("Enter student name: ")
    admission = get_non_empty_input("Enter admission number: ")

    # Prevent duplicate admission numbers
    if find_student(admission) is not None:
        print("\nStudent with that admission number already exists.")
        return

    cat = get_mark("Enter CAT mark: ")
    assignment = get_mark("Enter assignment mark: ")
    exam = get_mark("Enter exam mark: ")

    student = {
        "name": name,
        "admission": admission,
        "cat": cat,
        "assignment": assignment,
        "exam": exam
    }

    students.append(student)

    save_students()

    print("\nStudent added successfully! ✅")
    print("Student saved successfully! 💾")


# =========================================================
# VIEW STUDENTS
# =========================================================

def view_students():

    print("\n========== ALL STUDENTS ==========")

    if len(students) == 0:
        print("No students found.")
        return

    for student in students:

        total = (
            student["cat"]
            + student["assignment"]
            + student["exam"]
        )

        average = total / 3
        grade = calculate_grade(average)

        print("\n--------------------------------")
        print("Student Name:", student["name"])
        print("Admission Number:", student["admission"])
        print("CAT Mark:", student["cat"])
        print("Assignment Mark:", student["assignment"])
        print("Exam Mark:", student["exam"])
        print("Total:", total)
        print("Average:", round(average, 2))
        print("Grade:", grade)
        print("--------------------------------")


# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student():

    print("\n========== SEARCH STUDENT ==========")

    admission = get_non_empty_input(
        "Enter admission number: "
    )

    student = find_student(admission)

    if student is None:
        print("\nStudent not found. ❌")
        return

    total = (
        student["cat"]
        + student["assignment"]
        + student["exam"]
    )

    average = total / 3
    grade = calculate_grade(average)

    print("\nStudent found! ✅")
    print("--------------------------------")
    print("Student Name:", student["name"])
    print("Admission Number:", student["admission"])
    print("CAT Mark:", student["cat"])
    print("Assignment Mark:", student["assignment"])
    print("Exam Mark:", student["exam"])
    print("Total:", total)
    print("Average:", round(average, 2))
    print("Grade:", grade)
    print("--------------------------------")


# =========================================================
# UPDATE STUDENT
# =========================================================

def update_student():

    print("\n========== UPDATE STUDENT ==========")

    admission = get_non_empty_input(
        "Enter admission number of student to update: "
    )

    student = find_student(admission)

    if student is None:
        print("\nStudent not found. ❌")
        return

    print("\nStudent found! Enter the new details.")

    student["name"] = get_non_empty_input(
        "Enter new student name: "
    )

    student["cat"] = get_mark(
        "Enter new CAT mark: "
    )

    student["assignment"] = get_mark(
        "Enter new assignment mark: "
    )

    student["exam"] = get_mark(
        "Enter new exam mark: "
    )

    save_students()

    print("\nStudent updated successfully! ✅")


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student():

    print("\n========== DELETE STUDENT ==========")

    admission = get_non_empty_input(
        "Enter admission number of student to delete: "
    )

    student = find_student(admission)

    if student is None:
        print("\nStudent not found. ❌")
        return

    print("\nStudent found:", student["name"])

    confirmation = input(
        "Are you sure you want to delete this student? (Y/N): "
    ).strip().lower()

    if confirmation == "y":

        students.remove(student)

        save_students()

        print("\nStudent deleted successfully! ✅")

    else:
        print("\nDeletion cancelled.")


# =========================================================
# REPORT
# =========================================================

def student_report():

    print("\n========== STUDENT REPORT ==========")

    if len(students) == 0:
        print("No students available for the report.")
        return

    total_students = len(students)

    total_marks = 0
    passed_students = 0
    failed_students = 0

    highest_average = -1
    lowest_average = 101

    highest_student = ""
    lowest_student = ""

    for student in students:

        total = (
            student["cat"]
            + student["assignment"]
            + student["exam"]
        )

        average = total / 3

        total_marks += total

        if average >= 50:
            passed_students += 1
        else:
            failed_students += 1

        if average > highest_average:
            highest_average = average
            highest_student = student["name"]

        if average < lowest_average:
            lowest_average = average
            lowest_student = student["name"]

    overall_average = total_marks / (total_students * 3)

    print("\n--------------------------------")
    print("TOTAL STUDENTS:", total_students)
    print("OVERALL AVERAGE:", round(overall_average, 2))
    print("PASSED STUDENTS:", passed_students)
    print("FAILED STUDENTS:", failed_students)

    print("\nHIGHEST PERFORMER:")
    print(highest_student)
    print("Average:", round(highest_average, 2))

    print("\nLOWEST PERFORMER:")
    print(lowest_student)
    print("Average:", round(lowest_average, 2))

    print("--------------------------------")


# =========================================================
# LOGIN
# =========================================================

def login():

    print("\n================================")
    print("     STUDENT MANAGEMENT SYSTEM")
    print("================================")

    print("\nLOGIN")

    attempts = 3

    while attempts > 0:

        username = input("Username: ")

        password = getpass.getpass("Password: ")

        if username == USERNAME and password == PASSWORD:

            print("\nLogin successful! ✅")
            return True

        attempts -= 1

        print("\nIncorrect username or password. ❌")
        print("Attempts remaining:", attempts)

    print("\nToo many failed attempts.")
    print("Program closing...")

    return False


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():

    while True:

        print("\n================================")
        print("       MAIN MENU")
        print("================================")

        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Student Report")
        print("7. Logout")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            student_report()

        elif choice == "7":
            print("\nLogging out...")
            break

        elif choice == "8":
            print("\nThank you for using the system.")
            exit()

        else:
            print("\nInvalid choice. Please choose 1-8.")


# =========================================================
# PROGRAM START
# =========================================================

load_students()

if login():

    main_menu()

else:

    print("Goodbye.")