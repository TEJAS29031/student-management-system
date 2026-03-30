import streamlit as st
import pandas as pd
from database import StudentDatabase
import hashlib

# Page configuration
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        margin: 1rem 0;
    }
    h1 {
        color: #2C3E50;
        text-align: center;
        padding: 1rem 0;
    }
    .stat-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .login-title {
        text-align: center;
        color: #2C3E50;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Login credentials (in production, use database with hashed passwords)
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"

def check_login(username, password):
    """Verify login credentials"""
    return username == VALID_USERNAME and password == VALID_PASSWORD

def login_page():
    """Display login page"""
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="login-title">🎓 Student Management System</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #7f8c8d;">Admin Login</h3>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_btn = st.form_submit_button("🔐 Login", use_container_width=True)
        
        if login_btn:
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display credentials hint
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>
            <p><strong>Demo Credentials:</strong></p>
            <p>Username: <code>admin</code></p>
            <p>Password: <code>admin123</code></p>
        </div>
    """, unsafe_allow_html=True)

def logout():
    """Handle logout"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

def main_app():
    """Main application after login"""
    # Initialize database
    db = StudentDatabase()
    
    # Sidebar navigation
    st.sidebar.title("🎓 Navigation")
    st.sidebar.markdown(f"**Welcome, {st.session_state.username}!** 👋")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Add Student", "View Students", "Search Student", "Update/Delete"]
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        logout()
    
    # Main title
    st.title("🎓 Student Management System")
    st.markdown("---")
    
    # Dashboard Page
    if page == "Dashboard":
        st.header("📊 Dashboard")
        
        stats = db.get_statistics()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Total Students", stats['total'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Active Students", stats['active'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Inactive Students", stats['inactive'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Students by Course")
        if stats['by_course']:
            course_df = pd.DataFrame(stats['by_course'], columns=['Course', 'Count'])
            st.bar_chart(course_df.set_index('Course'))
        else:
            st.info("No student data available yet.")
    
    # Add Student Page
    elif page == "Add Student":
        st.header("➕ Add New Student")
        
        with st.form("add_student_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                student_id = st.text_input("Student ID*", placeholder="e.g., STU001")
                name = st.text_input("Full Name*", placeholder="e.g., John Doe")
                email = st.text_input("Email*", placeholder="e.g., john@example.com")
            
            with col2:
                phone = st.text_input("Phone Number", placeholder="e.g., +1234567890")
                course = st.selectbox(
                    "Course*",
                    ["Computer Science", "Electronics", "Mechanical", "Civil", "IT", "Other"]
                )
            
            submitted = st.form_submit_button("Add Student")
        
        if submitted:
            if not student_id or not name or not email:
                st.markdown('<div class="error-message">❌ Please fill all required fields!</div>', unsafe_allow_html=True)
            else:
                success, message = db.add_student(student_id, name, email, phone, course)
                if success:
                    st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
    
    # View Students Page
    elif page == "View Students":
        st.header("👥 All Students")
        
        students = db.get_all_students()
        
        if students:
            df = pd.DataFrame(
                students,
                columns=['ID', 'Student ID', 'Name', 'Email', 'Phone', 'Course', 'Enrollment Date', 'Status']
            )
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            
            st.download_button(
                label="📥 Download as CSV",
                data=df.to_csv(index=False),
                file_name="students.csv",
                mime="text/csv"
            )
        else:
            st.info("No students found in the database.")
    
    # Search Student Page
    elif page == "Search Student":
        st.header("🔍 Search Student")
        
        search_term = st.text_input("Enter Student ID, Name, or Email", placeholder="Search...")
        
        if search_term:
            students = db.search_student(search_term)
            
            if students:
                df = pd.DataFrame(
                    students,
                    columns=['ID', 'Student ID', 'Name', 'Email', 'Phone', 'Course', 'Enrollment Date', 'Status']
                )
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.warning("No students found matching your search.")
    
    # Update/Delete Page
    elif page == "Update/Delete":
        st.header("✏️ Update or Delete Student")
        
        students = db.get_all_students()
        
        if students:
            student_options = {f"{s[1]} - {s[2]}": s for s in students}
            selected = st.selectbox("Select Student", list(student_options.keys()))
            
            if selected:
                student = student_options[selected]
                
                st.markdown("### Update Information")
                
                with st.form("update_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        name = st.text_input("Full Name", value=student[2])
                        email = st.text_input("Email", value=student[3])
                        phone = st.text_input("Phone", value=student[4] or "")
                    
                    with col2:
                        courses = ["Computer Science", "Electronics", "Mechanical", "Civil", "IT", "Other"]
                        # Find the index of current course, default to 0 if not found
                        try:
                            course_index = courses.index(student[5])
                        except ValueError:
                            course_index = 0
                        
                        course = st.selectbox("Course", courses, index=course_index)
                        
                        # Fix for status selection
                        status_index = 0 if student[7] == "Active" else 1
                        status = st.selectbox("Status", ["Active", "Inactive"], index=status_index)
                    
                    col_update, col_delete = st.columns(2)
                    
                    with col_update:
                        update_btn = st.form_submit_button("Update Student", type="primary")
                    
                    with col_delete:
                        delete_btn = st.form_submit_button("Delete Student", type="secondary")
                
                # Handle buttons OUTSIDE the form
                if update_btn:
                    success, message = db.update_student(student[0], name, email, phone, course, status)
                    if success:
                        st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
                
                if delete_btn:
                    success, message = db.delete_student(student[0])
                    if success:
                        st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
        else:
            st.info("No students available to update or delete.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #7f8c8d;'>© 2024 Student Management System | Built with Streamlit</div>",
        unsafe_allow_html=True
    )

# Main entry point
if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()