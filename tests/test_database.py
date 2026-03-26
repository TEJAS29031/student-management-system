import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import StudentDatabase

@pytest.fixture
def test_db():
    """Use in-memory DB (NO FILE, NO ERRORS)"""
    db = StudentDatabase(':memory:')
    yield db

def test_add_student(test_db):
    success, _ = test_db.add_student('STU001', 'John', 'john@test.com', '123', 'CS')
    assert success

def test_duplicate_student(test_db):
    test_db.add_student('STU001', 'John', 'john@test.com', '123', 'CS')
    success, _ = test_db.add_student('STU001', 'Jane', 'jane@test.com', '456', 'IT')
    assert not success

def test_get_all_students(test_db):
    test_db.add_student('STU001', 'John', 'john@test.com', '123', 'CS')
    test_db.add_student('STU002', 'Jane', 'jane@test.com', '456', 'IT')
    students = test_db.get_all_students()
    assert len(students) == 2

def test_search_student(test_db):
    test_db.add_student('STU001', 'John', 'john@test.com', '123', 'CS')
    results = test_db.search_student('John')
    assert len(results) == 1

def test_update_student(test_db):
    test_db.add_student('STU001', 'John', 'john@test.com', '123', 'CS')
    student = test_db.get_all_students()[0]
    success, _ = test_db.update_student(student[0], 'Updated', 'u@test.com', '999', 'IT', 'Active')
    assert success

def test_delete_student(test_db):
    test_db.add_student('STU001', 'John', 'john@test.com', '123', 'CS')
    student = test_db.get_all_students()[0]
    success, _ = test_db.delete_student(student[0])
    assert success

def test_statistics(test_db):
    test_db.add_student('STU001', 'John', 'john@test.com', '123', 'CS')
    test_db.add_student('STU002', 'Jane', 'jane@test.com', '456', 'IT')
    stats = test_db.get_statistics()
    assert stats['total'] == 2