import streamlit as st
import pandas as pd
from database import StudentDatabase

# ---------------- AUTHENTICATION ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

# 🔴 STOP APP IF NOT LOGGED IN
if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- MAIN APP ---------------- #

# Page configuration (MUST COME AFTER LOGIN)
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main { padding: 2rem; }
.stButton>button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    border-radius: 5px;
    padding: 0.5rem;
    font-weight: bold;
}
.stButton>button:hover { background-color: #45a049; }
</style>
""", unsafe_allow_html=True)

# Initialize DB
db = StudentDatabase()

# Sidebar
st.sidebar.title("🎓 Navigation")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Add Student", "View Students", "Search Student", "Update/Delete"]
)

# Title
st.title("🎓 Student Management System")
st.markdown("---")

# ---------------- DASHBOARD ---------------- #
if page == "Dashboard":
    st.header("📊 Dashboard")

    stats = db.get_statistics()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", stats['total'])
    col2.metric("Active Students", stats['active'])
    col3.metric("Inactive Students", stats['inactive'])

    if stats['by_course']:
        df = pd.DataFrame(stats['by_course'], columns=['Course', 'Count'])
        st.bar_chart(df.set_index('Course'))
    else:
        st.info("No data available")

# ---------------- ADD STUDENT ---------------- #
elif page == "Add Student":
    st.header("➕ Add Student")

    with st.form("add_form"):
        student_id = st.text_input("Student ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        course = st.selectbox("Course", ["Computer Science", "IT", "Mechanical", "Civil"])

        submit = st.form_submit_button("Add")

        if submit:
            if not student_id or not name or not email:
                st.error("Fill required fields")
            else:
                success, msg = db.add_student(student_id, name, email, phone, course)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

# ---------------- VIEW ---------------- #
elif page == "View Students":
    st.header("👥 Students")

    data = db.get_all_students()

    if data:
        df = pd.DataFrame(data, columns=[
            'ID', 'Student ID', 'Name', 'Email', 'Phone',
            'Course', 'Date', 'Status'
        ])
        st.dataframe(df)
    else:
        st.info("No students")

# ---------------- SEARCH ---------------- #
elif page == "Search Student":
    st.header("🔍 Search")

    q = st.text_input("Search")

    if q:
        data = db.search_student(q)
        if data:
            df = pd.DataFrame(data, columns=[
                'ID', 'Student ID', 'Name', 'Email', 'Phone',
                'Course', 'Date', 'Status'
            ])
            st.dataframe(df)
        else:
            st.warning("No results")

# ---------------- UPDATE / DELETE ---------------- #
elif page == "Update/Delete":
    st.header("✏️ Update/Delete")

    data = db.get_all_students()

    if data:
        options = {f"{s[1]} - {s[2]}": s for s in data}
        selected = st.selectbox("Select", list(options.keys()))

        student = options[selected]

        name = st.text_input("Name", student[2])
        email = st.text_input("Email", student[3])
        phone = st.text_input("Phone", student[4] or "")
        course = st.text_input("Course", student[5])
        status = st.selectbox("Status", ["Active", "Inactive"])

        if st.button("Update"):
            success, msg = db.update_student(student[0], name, email, phone, course, status)
            if success:
                st.success(msg)
                st.rerun()

        if st.button("Delete"):
            success, msg = db.delete_student(student[0])
            if success:
                st.success(msg)
                st.rerun()

# Footer
st.markdown("---")
st.markdown("© Student Management System")