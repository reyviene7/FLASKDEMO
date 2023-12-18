from flask import render_template, redirect, request, jsonify, url_for, flash
from . import user_bp
import app.models as models
from app.models import m_college, m_course, m_student
from app.user.forms import UserForm


@user_bp.route('/')
def index():
    return render_template('index.html', title='Home')

@user_bp.route('/college', methods=['GET', 'POST'])
def college_db():
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        m_college.create(code, name)
        flash('College created Successfully!')
        return redirect(url_for('user.college'))

    colleges = m_college.get_colleges()     
    print(colleges)
    return render_template('college.html', colleges=colleges, title='College',something='something')

@user_bp.route('/college/delete_college/<string:college_code>', methods=['DELETE'])
def delete_college(college_code):
    if request.method == 'DELETE':
        flash('College has been deleted Successfully!')
        result = m_college.delete_college(college_code)
        response = jsonify(result)
        return response
    
@user_bp.route('/college/<string:college_code>', methods=['GET', 'POST'])
def update_college(college_code):
    if request.method == 'POST':
        new_code = request.form.get('code')
        new_name = request.form.get('name')
        m_college.update_college(college_code, new_code, new_name)
        return redirect(url_for('user.college'))
    college = m_college.get_college_by_code(college_code)
    return render_template('college.html', college=college)
     
@user_bp.route('/user/register', methods=['POST','GET'])
def register():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = models.m_college(code=form.code.data, name=form.name.data)
        user.add()
        return redirect('/user')
    else:
        return render_template('signup.html', form=form)

@user_bp.route("/user/delete", methods=["POST"])
def delete():
    id = request.form['id']
    if models.Users.delete(id):
        return jsonify(success=True,message="Successfully deleted")
    else:
        return jsonify(success=False,message="Failed")          
    
@user_bp.route('/search_college', methods=['GET'])
def search_college():
    search_query = request.args.get('search')
    filter_by = request.args.get('filter_by')
    
    if filter_by == 'code':
        colleges = m_college.search_colleges_by_code(search_query)
    else:
        colleges = m_college.search_colleges_by_name(search_query)
    
    return render_template('college.html', colleges=colleges)

@user_bp.route('/course', methods=['GET' , 'POST'])
def course():
    colleges = m_college.get_colleges()
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        college = request.form.get('college')
        
        print(f"Received data - Code: {code}, Name: {name}, College: {college}")

        m_course.create_course(code, name, college)
        flash('Course created Successfully!')
        return redirect(url_for('user.course'))

    courses = m_course.get_courses()
    print(courses)
    return render_template('course.html', courses=courses, title="Course", colleges=colleges)

@user_bp.route('/delete_course/<string:course_code>', methods=['DELETE'])
def delete_course(course_code):
    if request.method == 'DELETE':
        flash('College has been deleted Successfully!')
        result = m_course.delete_course(course_code)
        response = jsonify(result)
        return response
    
@user_bp.route('/update_course/<string:course_code>', methods=['POST'])
def update_course(course_code):
    new_code = request.form.get('code')
    new_name = request.form.get('name')
    new_college = request.form.get('college')
    m_course.update_course(course_code, new_code, new_name, new_college)
    courses = m_course.get_courses()
    colleges = m_college.get_colleges()
    return render_template('course.html', courses=courses, colleges=colleges)

@user_bp.route('/search_course', methods=['GET'])
def search_course():
    search_query = request.args.get('search')
    filter_by = request.args.get('filter_by')
    
    colleges = m_college.get_colleges()

    if filter_by == 'code':
        courses = m_course.search_courses_by_code(search_query)
    elif filter_by == 'name':
        courses = m_course.search_courses_by_name(search_query)
    elif filter_by == 'college':
        courses = m_course.search_courses_by_college(search_query)
    else:
        courses = m_course.get_courses()
    
    return render_template('course.html', courses=courses, colleges=colleges)


@user_bp.route('/student', methods=['GET', 'POST'])
def student():
    courses = m_course.get_courses()

    if request.method == 'POST':
        id = request.form.get('id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        course = request.form.get('course')
        year = request.form.get('year')
        gender = request.form.get('gender')
        m_student.add_student(id, firstname, lastname, course, year, gender)
        print(f"Received data - id: {id}, Name: {firstname} {lastname}, Course: {course}, Year: {year}, Gender: {gender} ")

    students = m_student.get_students()
    print(students)
    return render_template('student.html', students=students, title="Student", courses=courses)

@user_bp.route('/delete_student/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        result = m_student.delete_student(student_id)
        flash("Student is deleted")
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    
@user_bp.route('/update_student/<string:student_id>', methods=['POST'])
def update_student(student_id):
    new_id = request.form['id']
    new_firstname = request.form['firstname']
    new_lastname = request.form['lastname']
    new_course = request.form['course']
    new_year = request.form['year']
    new_gender = request.form['gender']
    m_student.update_student(student_id, new_id, new_firstname, new_lastname, new_course, new_year, new_gender)
    
    return redirect(url_for('user.student', student_id=student_id))

@user_bp.route('/search_student', methods=['GET'])
def search_student():
    courses = m_course.get_courses()

    search_query = request.form.get('search')
    filter_by = request.form.get('filter_by')
    
    if filter_by == 'id':
        students = m_student.search_students_by_id(search_query)
    elif filter_by == 'firstname':
        students = m_student.search_students_by_firstname(search_query)
    elif filter_by == 'lastname':
        students = m_student.search_students_by_lastname(search_query)
    elif filter_by == 'course':
        students = m_student.search_students_by_course(search_query)
    elif filter_by == 'year':
        students = m_student.search_students_by_year(search_query)
    elif filter_by == 'gender':
        students = m_student.search_students_by_gender(search_query)
    else:
        students = m_student.get_students()
    
    return render_template('student.html', students=students, courses=courses)
