import pandas 
import logging
from typing import List
logging.basicConfig(filename="cms_logs.txt", level=logging.INFO, format="%(asctime)s:%(message)s")
class CourseManagementSystem:
    def __init__(self):
        self.Students = pandas.DataFrame(columns=["name", "student_id"])
        self.courses = pandas.DataFrame(columns=["code", "name", "credits", "capacity", "enrolled_students"])
        self.enrolls = pandas.DataFrame(columns=["student_id", "course_code"])
        self.waitlist = pandas.DataFrame(columns=["student_id", "course_code"])
        self.getData()
    def save_data(self):
        self.Students.to_csv("student.csv", index=False)
        self.courses.to_csv("course.csv", index=False)
        self.enrolls.to_csv("enroll.csv", index=False)
        self.waitlist.to_csv("waitlist.csv", index=False)
        logging.info("data saved")
    def getData(self):
        try:
            self.Students = pandas.read_csv("student.csv")
            assert list(self.Students.columns) == ["name", "student_id"]
            logging.info("data found ")
        except FileNotFoundError:
            logging.warning("file students.csv not found")
        except AssertionError:
            logging.error("columns must be (name, student_id)")
    def add_student(self, Name, s_id):
        if s_id in self.Students["student_id"].values:
            logging.warning(f"student with id {s_id} already exists")
            return None
        self.Students = pandas.concat([self.Students, (pandas.DataFrame([{"name": Name, "student_id": s_id}]))], ignore_index=True)
        self.Students.to_csv("student.csv", index=False)
        logging.info(f"student added ")
    def enroll_student(self, s_id, c_id):
        if c_id not in self.courses["code"].values:
            logging.error(f"course does not exist")
            return None
        if s_id not in self.Students["student_id"].values:
            logging.error(f"Student ID {s_id} does not exist")
            return None
        course = self.courses.loc[self.courses["code"] == c_id]
        if course["enrolled_students"].values[0] < course["capacity"].values[0]:
            self.enrolls = pandas.concat([self.enrolls, pandas.DataFrame([{"student_id": s_id, "course_code": c_id}])], ignore_index=True)
            self.courses.loc[self.courses["code"] == c_id, "enrolled_students"] += 1
            self.save_data()
            logging.info(f"student Enrolled ")
        else:
            self.add_to_waitlist(s_id, c_id)
            logging.info(f"student Added to waitlist")
    def add_course(self, id, name, credits, capacity):
        if id in self.courses["code"].values:
            logging.warning(f"Course  already exists")
            return None
        self.courses = pandas.concat([self.courses, pandas.DataFrame([{"code": id, "name": name, "credits": credits, "capacity": capacity, "enrolled_students": 0}])], ignore_index=True)
        (self.courses.drop(columns=["enrolled_students"])).to_csv("course.csv", index=False)
        logging.info(f"course Added")
    def remove_course(self, c_id):
        if c_id not in self.courses["code"].values:
            logging.error(f"Course doesn't exist")
            return None
        self.courses = self.courses[self.courses["code"] != c_id]
        self.enrolls = self.enrolls[self.enrolls["course_code"] != c_id]
        self.waitlist = self.waitlist[self.waitlist["course_code"] != c_id]
        self.save_data()
        logging.info(f"course Removed")
    def add_to_waitlist(self, s_id, c_id):
        if not ((self.waitlist["student_id"] == s_id) & (self.waitlist["course_code"] == c_id)).any():
            self.waitlist = pandas.concat([self.waitlist, pandas.DataFrame([{"student_id": s_id, "course_code": c_id}])], ignore_index=True)
            self.save_data()
            logging.info(f"student Added student  to waitlist for course ")
    def get_student_courses(self, s_id) :
        return self.courses[self.courses["code"].isin(self.enrolls[self.enrolls["student_id"] == s_id]["course_code"])]["name"].tolist()
    def find_students_in_course(self, c_id) :
        return self.Students[self.Students["student_id"].isin(self.enrolls[self.enrolls["course_code"] == c_id]["student_id"])]["name"].tolist()
    def get_most_popular_course(self) :
        return None if self.enrolls.empty else self.courses.loc[self.courses["code"] == self.enrolls["course_code"].value_counts().idxmax(), "name"].values[0]
