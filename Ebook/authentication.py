from app import *

app.config['SESSION_TYPE'] = 'sqlalchemy'  # Use SQLAlchemy as the session storage backend
app.config['SESSION_SQLALCHEMY'] = db 

# Initialize the session extension
Session(app)


# AUTHENTICATION
@app.route('/authentication')
def index():
    return render_template("authentication.html")

@app.route('/signup' , methods=['POST' , 'GET'])
def signup():
    if request.method == 'POST':
        data=request.get_json()
        name=data.get("sname")
        student_id=data.get("sstud_id")
        password=data.get("spassword")
        exist_id=Student.query.filter_by(student_id=student_id).first()
        if exist_id:
            return jsonify({"success":False})
        new_student=Student(name=name,student_id=student_id)
        new_student.set_password(password)
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'success':'True'})
    
@app.route('/login' , methods=['POST','GET'])
def login():
    if request.method=='POST':
        admin=False
        data=request.get_json()
        student_id=data.get("lstud_id")
        if student_id == '808132':
            admin=True
        password=data.get("lpassword")
        exist_id=Student.query.filter_by(student_id=student_id).first()
        if not exist_id:
            return jsonify({"success":False})
        elif exist_id and exist_id.check_password(password):
            session["user_id"]=exist_id.student_id
            session["username"]=exist_id.name
            if admin:
                session['role']='Admin'
                return jsonify({"success":True , "admin":1})
            else:
                session['role']='user'
                return jsonify({"success":True})
        else:
            return jsonify({"success":False})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('redirection'))