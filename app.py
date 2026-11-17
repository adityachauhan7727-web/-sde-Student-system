
import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT,
    email TEXT
)
""")
conn.commit()

st.title("🎓 Student Record Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.header("Add New Student")

    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    course = st.text_input("Course")
    email = st.text_input("Email")

    if st.button("Add Student"):
        if name and course and email:
            cursor.execute(
                "INSERT INTO students (name, age, course, email) VALUES (?, ?, ?, ?)",
                (name, age, course, email)
            )
            conn.commit()
            st.success("Student added successfully!")
        else:
            st.warning("Please fill all fields.")

# READ
elif menu == "View Students":
    st.header("All Student Records")

    df = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(df, use_container_width=True)

# UPDATE
elif menu == "Update Student":
    st.header("Update Student Record")

    cursor.execute("SELECT id FROM students")
    ids = [row[0] for row in cursor.fetchall()]

    if ids:
        student_id = st.selectbox("Select Student ID", ids)

        cursor.execute(
            "SELECT * FROM students WHERE id=?", (student_id,)
        )
        student = cursor.fetchone()

        name = st.text_input("Name", student[1])
        age = st.number_input("Age", min_value=1, max_value=100,
                              value=student[2])
        course = st.text_input("Course", student[3])
        email = st.text_input("Email", student[4])

        if st.button("Update Student"):
            cursor.execute("""
                UPDATE students
                SET name=?, age=?, course=?, email=?
                WHERE id=?
            """, (name, age, course, email, student_id))

            conn.commit()
            st.success("Student updated successfully!")
    else:
        st.info("No student records available.")

# DELETE
elif menu == "Delete Student":
    st.header("Delete Student Record")

    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()

    if students:
        student_dict = {
            f"{s[0]} - {s[1]}": s[0] for s in students
        }

        selected = st.selectbox(
            "Select Student", list(student_dict.keys())
        )

        if st.button("Delete Student"):
            student_id = student_dict[selected]

            cursor.execute(
                "DELETE FROM students WHERE id=?", (student_id,)
            )
            conn.commit()

            st.success("Student deleted successfully!")
    else:
        st.info("No student records available.")

conn.close()
