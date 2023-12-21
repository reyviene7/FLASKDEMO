from app import mysql
from flask import flash

class Users(object):

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email

    def add(self):
        cursor = mysql.connection.cursor()

        sql = f"INSERT INTO users(username,user_password,email) \
                VALUES('{self.username}',md5('{self.password}'),'{self.email}')" 

        cursor.execute(sql)
        mysql.connection.commit()

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * from users"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls,id):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE from users where id= {id}"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False

class m_college(object):
    @classmethod
    def create(cls, code, name):
        try: 
            cur =mysql.new_cursor(dictionary=True)
            cur.execute("INSERT INTO College (code, name) VALUES (%s,%s)", (code, name))
            mysql.connection.commit()
            cur.close()
            return "College created successfully"
        except Exception as e:
            return f"Failed to create College: {str(e)}"
    
    @classmethod
    def get_colleges(cls):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM College")
        colleges = cur.fetchall()
        cur.close()
        return colleges 
    
    @classmethod
    def delete_college(cls, college_code):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM College WHERE code = %s", (college_code,))
            mysql.connection.commit()
            cur.close()
            return "College deleted successfully"
        except Exception as e:
            return f"Failed to delete College: {str(e)}"

    @classmethod
    def update_college(cls, college_code, new_code, new_name):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("UPDATE College SET code = %s, name = %s WHERE code = %s", (new_code, new_name, college_code))
            mysql.connection.commit()
            cur.close()
            return "College updated successfully"
        except Exception as e:
            return f"Failed to update College: {str(e)}"

    @classmethod
    def get_college_by_code(cls, code):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM College WHERE code = %s", (code,))
        college = cur.fetchone()
        cur.close()
        return college
    
    @classmethod
    def search_colleges_by_code(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM College WHERE code LIKE %s", (f"%{search_query}%",))
        colleges = cur.fetchall()
        cur.close()
        return colleges

    @classmethod
    def search_colleges_by_name(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM College WHERE name LIKE %s", (f"%{search_query}%",))
        colleges = cur.fetchall()
        cur.close()
        return colleges


class m_course:
    @classmethod
    def create_course(cls, code, name, College):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("INSERT INTO course (code, name, College) VALUES (%s, %s, %s)", (code, name, College))
            mysql.connection.commit()
            return "Course created successfully"
        
        except Exception as e:
            return f"Failed to create course: {str(e)}"

    @classmethod
    def get_courses(cls):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM course")
        courses = cur.fetchall()
        return courses

    @classmethod
    def delete_course(cls, code):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM course WHERE code = %s", (code,))
            mysql.connection.commit()
            cur.close()
            return {"success": True, "message": "Course deleted successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @classmethod
    def update_course(cls, course_code, new_code, new_name, new_college):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("UPDATE course SET code = %s, name = %s, College = %s WHERE code = %s", (new_code, new_name, new_college, course_code))
            mysql.connection.commit()
            cur.close()
            return "Course updated successfully"
        except Exception as e:
            return f"Failed to update course: {str(e)}"
    
    @classmethod
    def search_courses_by_code(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM course WHERE code LIKE %s", (f"%{search_query}%",))
        courses = cur.fetchall()
        cur.close()
        return courses

    @classmethod
    def search_courses_by_name(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM course WHERE name LIKE %s", (f"%{search_query}%",))
        courses = cur.fetchall()
        cur.close()
        return courses

    @classmethod
    def search_courses_by_college(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM course WHERE College LIKE %s", (f"%{search_query}%",))
        courses = cur.fetchall()
        cur.close()
        return courses

class m_student:
    @classmethod
    def add_student(cls, id, firstname, lastname, course_code, year, gender):
        try:
            cur = mysql.new_cursor(dictionary=True)

            # Check if the ID is already taken
            cur.execute("SELECT id FROM student WHERE id = %s", (id,))
            existing_id = cur.fetchone()
            if existing_id:
                flash("ID is already taken.", "error")
                return "Failed to create student"

            # Insert the new student record
            cur.execute("INSERT INTO student (id, firstname, lastname, course, year, gender) VALUES ( %s, %s, %s, %s, %s, %s)",
                        (id, firstname, lastname, course_code, year, gender))
            mysql.connection.commit()
            
            return "Student created successfully"
        
        except Exception as e:
            flash("Failed to create student(models 1).", "error")
            return "Failed to create student"
    
    @classmethod
    def get_students(cls):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student")
        course = cur.fetchall()
        return course
    
    @classmethod
    def search_students_by_id(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE id LIKE %s", (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_firstname(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE firstname LIKE %s", (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_lastname(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE lastname LIKE %s", (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_course(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE course LIKE %s", (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_year(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE year LIKE %s", (f"%{search_query}%",))
        students = cur.fetchall()
        cur.close()
        return students

    @classmethod
    def search_students_by_gender(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM student WHERE gender = %s", (search_query,))
        students = cur.fetchall()
        cur.close()
        return students
    
    @classmethod
    def update_student(cls, student_id, new_id, new_firstname, new_lastname, new_course, new_year, new_gender):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("SELECT id FROM student WHERE id = %s AND id != %s", (new_id, student_id))
            existing_id = cur.fetchone()
            if existing_id:
                flash("ID is already taken.", "error")
                return "Failed to update student"
            cur.execute("UPDATE student SET id=%s, firstname=%s, lastname=%s, course=%s, year=%s, gender=%s WHERE id=%s",
                        (new_id, new_firstname, new_lastname, new_course, new_year, new_gender, student_id))

            mysql.connection.commit()
            cur.close()
            return "Student updated successfully"
        except Exception as e:
            return "Failed to update student"

    @classmethod
    def get_student_by_id(cls, student_id):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
            student = cur.fetchone()
            cur.close()
            return student
        except Exception as e:
            flash("Failed to get student by ID.", "error")
            return None
        
    @classmethod
    def delete_student(cls, student_id):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM student WHERE id = %s", (student_id,))
            mysql.connection.commit()
            cur.close()
            return {"success": True, "message": "Course deleted successfully"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
