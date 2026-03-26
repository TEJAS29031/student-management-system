import sqlite3
from datetime import datetime

class StudentDatabase:
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
        
        # 🔥 SINGLE persistent connection (IMPORTANT)
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.init_database()

    def init_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                course TEXT NOT NULL,
                enrollment_date TEXT NOT NULL,
                status TEXT DEFAULT 'Active'
            )
        ''')
        self.conn.commit()

    def add_student(self, student_id, name, email, phone, course):
        try:
            enrollment_date = datetime.now().strftime('%Y-%m-%d')

            self.cursor.execute('''
                INSERT INTO students (student_id, name, email, phone, course, enrollment_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, name, email, phone, course, enrollment_date))

            self.conn.commit()
            return True, "Student added successfully!"

        except sqlite3.IntegrityError:
            return False, "Student ID already exists!"
        except Exception as e:
            return False, str(e)

    def get_all_students(self):
        self.cursor.execute('SELECT * FROM students ORDER BY id DESC')
        return self.cursor.fetchall()

    def search_student(self, search_term):
        self.cursor.execute('''
            SELECT * FROM students
            WHERE student_id LIKE ? OR name LIKE ? OR email LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        return self.cursor.fetchall()

    def update_student(self, id, name, email, phone, course, status):
        try:
            self.cursor.execute('''
                UPDATE students
                SET name=?, email=?, phone=?, course=?, status=?
                WHERE id=?
            ''', (name, email, phone, course, status, id))

            self.conn.commit()
            return True, "Student updated successfully!"

        except Exception as e:
            return False, str(e)

    def delete_student(self, id):
        try:
            self.cursor.execute('DELETE FROM students WHERE id=?', (id,))
            self.conn.commit()
            return True, "Student deleted successfully!"

        except Exception as e:
            return False, str(e)

    def get_statistics(self):
        self.cursor.execute('SELECT COUNT(*) FROM students')
        total = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM students WHERE status='Active'")
        active = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT course, COUNT(*) FROM students GROUP BY course')
        by_course = self.cursor.fetchall()

        return {
            'total': total,
            'active': active,
            'inactive': total - active,
            'by_course': by_course
        }

    def close(self):
        self.conn.close()