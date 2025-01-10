# Object-Oriented Student Course Management System

## Overview
This project implements a Student Course Management System in Python using:
- Object-Oriented Programming principles
- File I/O operations for data persistence
- Pandas for data manipulation
- NumPy for numerical computations
- Exception handling for robustness

## Classes and Methods
### 1. **Student Class**
- Attributes:
  - `student_id`: Unique identifier for the student
  - `name`: Name of the student
  - `grades`: Dictionary of grades for enrolled courses

- Methods:
  - `add_grade(course_code: str, grade: float)`
  - `get_gpa() -> float`: Calculate GPA using NumPy

### 2. **Course Class**
- Attributes:
  - `code`: Unique course code
  - `name`: Name of the course
  - `credits`: Number of credits
  - `capacity`: Maximum number of students
  - `enrolled_students`: List of student IDs enrolled

- Methods:
  - `add_student(student_id: int)`
  - `remove_student(student_id: int)`

### 3. **CourseManagementSystem Class**
- Attributes:
  - `students_df`: Pandas DataFrame to store student information
  - `courses_df`: Pandas DataFrame to store course information
  - `enrollments_df`: Pandas DataFrame to store enrollment information
  - `waitlist_df`: Pandas DataFrame to store waitlist information

- Methods:
  - `add_student(name: str, student_id: int)`
  - `add_course(code: str, name: str, credits: int, capacity: int)`
  - `enroll_student(student_id: int, course_code: str)`
  - `calculate_total_credits(student_id: int) -> int`
  - `find_students_in_course(course_code: str) -> List[str]`
  - `get_most_popular_course() -> str`
  - `remove_course(course_code: str)`
  - `calculate_gpa(student_id: int) -> float`
  - `get_student_courses(student_id: int) -> List[str]`
  - `add_to_waitlist(student_id: int, course_code: str)`

## File I/O Operations
- Load initial data from:
  - `students.csv`
  - `courses.csv`

- Save updated data to respective files after each operation.
- Log operations to `operations.log`.

## Implementation
### Loading and Saving Data
```python
import pandas as pd
import numpy as np
import logging

logging.basicConfig(filename='operations.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class CourseManagementSystem:
    def __init__(self):
        self.students_df = pd.read_csv('students.csv')
        self.courses_df = pd.read_csv('courses.csv')
        self.enrollments_df = pd.DataFrame(columns=['student_id', 'course_code'])
        self.waitlist_df = pd.DataFrame(columns=['student_id', 'course_code'])

    def save_data(self):
        self.students_df.to_csv('students.csv', index=False)
        self.courses_df.to_csv('courses.csv', index=False)
        self.enrollments_df.to_csv('enrollments.csv', index=False)
        self.waitlist_df.to_csv('waitlist.csv', index=False)
```

### Adding a Student
```python
def add_student(self, name: str, student_id: int):
    if student_id in self.students_df['student_id'].values:
        logging.error(f"Student ID {student_id} already exists.")
        raise ValueError("Student ID already exists.")
    
    new_student = {'student_id': student_id, 'name': name}
    self.students_df = self.students_df.append(new_student, ignore_index=True)
    logging.info(f"Added student: {name}, ID: {student_id}")
    self.save_data()
```

### GPA Calculation
```python
def calculate_gpa(self, student_id: int) -> float:
    student_enrollments = self.enrollments_df[self.enrollments_df['student_id'] == student_id]
    grades = []
    
    for course_code in student_enrollments['course_code']:
        course_grades = self.students_df.loc[self.students_df['student_id'] == student_id, 'grades'].values
        grades.extend(course_grades)

    return np.mean(grades) if grades else 0.0
```

## Usage
- **Run the system**:
```python
cms = CourseManagementSystem()
cms.add_student('Alice', 101)
cms.add_course('CS101', 'Intro to CS', 3, 30)
cms.enroll_student(101, 'CS101')
print(cms.calculate_gpa(101))
```

## Features
### Logging
- Operations are logged in `operations.log` for traceability.

### Exception Handling
- Handle cases such as:
  - Duplicate student IDs
  - Non-existent courses
  - Full courses

## Explanation
- **Classes and Objects**: Encapsulate functionality and data for reusability.
- **File I/O**: Persist data and log operations.
- **Pandas**: Efficient data manipulation (e.g., filtering, grouping).
- **NumPy**: Numerical computations like GPA calculation.
- **Exception Handling**: Improve robustness and user experience.

## Suggested Improvement
Add a **real-time notification system** using websockets to inform students when they are moved from the waitlist to the enrolled list. This can be implemented using the `websocket` library in Python.
