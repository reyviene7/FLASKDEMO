from app import mysql


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
        cur.execute("SELECT * FROM college")
        colleges = cur.fetchall()
        cur.close()
        return colleges 
    
    @classmethod
    def delete_college(cls, college_code):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM college WHERE code = %s", (college_code,))
            print(f"DELETE FROM college WHERE code = {college_code}")
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
        cur.execute("SELECT * FROM college WHERE code = %s", (code,))
        college = cur.fetchone()
        cur.close()
        return college
    
    @classmethod
    def search_colleges_by_code(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM college WHERE code LIKE %s", (f"%{search_query}%",))
        colleges = cur.fetchall()
        cur.close()
        return colleges

    @classmethod
    def search_colleges_by_name(cls, search_query):
        cur = mysql.new_cursor(dictionary=True)
        cur.execute("SELECT * FROM college WHERE name LIKE %s", (f"%{search_query}%",))
        colleges = cur.fetchall()
        cur.close()
        return colleges
