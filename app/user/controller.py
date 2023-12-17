from flask import render_template, redirect, request, jsonify, url_for, flash
from . import user_bp
import app.models as models
from app.models import m_college
from app.user.forms import UserForm


@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/college', methods=['GET', 'POST'])
def college():
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

    # Fetch the current college data
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
    
@user_bp.route('/course')
def course():
    return render_template('course.html')

@user_bp.route('/student')
def student():
    return render_template('student.html')
