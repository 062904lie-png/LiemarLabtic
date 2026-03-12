from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ==========================================
# 1. DATA STORAGE (In-Memory for Demo)
# ==========================================
# For a real application (Requirement #3), you would replace this 
# list with SQLite, MySQL, or Firebase database queries.
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# API Key for Authentication (Requirement #6)
SECRET_API_KEY = "super-secret-key-123"

# ==========================================
# 2. HTML VIEWS & FRONT-END (Requirement #5)
# ==========================================

@app.route('/')
def home():
    # Redirect the home page to our interactive dashboard
    return redirect(url_for('list_students'))

@app.route('/students')
def list_students():
    # Calculate Analytics for the Dashboard (Requirement #2)
    grades = [s['grade'] for s in students]
    passed = len([g for g in grades if g >= 75])
    failed = len(grades) - passed
    avg = sum(grades) / len(grades) if grades else 0

    html = """
    <html>
    <head><title>Student Dashboard</title></head>
    <body style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: auto;">
        <h2>📊 Student Dashboard</h2>
        
        <div style="background: #f4f4f9; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3>Analytics Summary</h3>
            <p><strong>Total Students:</strong> {{students|length}}</p>
            <p><strong>Class Average:</strong> {{ "%.2f"|format(avg) }}</p>
            <p><strong>Passed (>=75):</strong> <span style="color: green;">{{passed}}</span></p>
            <p><strong>Failed (<75):</strong> <span style="color: red;">{{failed}}</span></p>
        </div>

        <h3>Student List</h3>
        <a href="/add_student_form" style="display: inline-block; margin-bottom: 10px; padding: 5px 10px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">+ Add New Student</a>
        
        <table border="1" width="100%" cellpadding="8" style="border-collapse: collapse;">
            <tr style="background: #ddd;">
                <th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Actions</th>
            </tr>
            {% for s in students %}
            <tr>
                <td>{{s.id}}</td>
                <td>{{s.name}}</td>
                <td>
                    {{s.grade}} 
                    {% if s.grade >= 75 %} <span style="color:green;">(Pass)</span> 
                    {% else %} <span style="color:red;">(Fail)</span> {% endif %}
                </td>
                <td>{{s.section}}</td>
                <td>
                    <a href="/edit_student/{{s.id}}">Edit</a> | 
                    <form action="/delete_student/{{s.id}}" method="POST" style="display:inline;">
                        <button type="submit" onclick="return confirm('Delete {{s.name}}?')" style="color:red; border:none; background:none; cursor:pointer; text-decoration:underline;">Delete</button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr><td colspan="5">No students found.</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, students=students, avg=avg, passed=passed, failed=failed)

@app.route('/add_student_form')
def add_student_form():
    html = """
    <body style="font-family: Arial, sans-serif; padding: 20px; max-width: 400px; margin: auto;">
        <h2>Add New Student</h2>
        <form action="/add_student" method="POST" style="display: flex; flex-direction: column; gap: 10px;">
            <label>Name:</label> <input type="text" name="name" required autofocus>
            <label>Grade (0-100):</label> <input type="number" name="grade" required>
            <label>Section:</label> <input type="text" name="section" required>
            <input type="submit" value="Add Student" style="background: #28a745; color: white; padding: 10px; border: none; cursor: pointer;">
        </form>
        <br><a href="/students">Back to Dashboard</a>
    </body>
    """
    return render_template_string(html)

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        return "Student not found. <a href='/students'>Go back</a>", 404

    if request.method == 'POST':
        # Apply Data Validation (Requirement #4)
        name = request.form.get("name")
        section = request.form.get("section")
        try:
            grade = int(request.form.get("grade"))
            if grade < 0 or grade > 100:
                return "Error: Grade must be between 0 and 100. <br><a href='/edit_student/{}'>Go back</a>".format(id), 400
        except ValueError:
            return "Error: Grade must be a valid number. <br><a href='/edit_student/{}'>Go back</a>".format(id), 400

        # Update data
        student["name"] = name
        student["grade"] = grade
        student["section"] = section
        return redirect(url_for('list_students'))

    html = """
    <body style="font-family: Arial, sans-serif; padding: 20px; max-width: 400px; margin: auto;">
        <h2>Edit Student</h2>
        <form method="POST" style="display: flex; flex-direction: column; gap: 10px;">
            <label>Name:</label> <input type="text" name="name" value="{{student.name}}" required>
            <label>Grade (0-100):</label> <input type="number" name="grade" value="{{student.grade}}" required>
            <label>Section:</label> <input type="text" name="section" value="{{student.section}}" required>
            <button type="submit" style="background: #007bff; color: white; padding: 10px; border: none; cursor: pointer;">Update Student</button>
        </form>
        <br><a href="/students">Back to Dashboard</a>
    </body>
    """
    return render_template_string(html, student=student)


# ==========================================
# 3. CORE API ENDPOINTS (CRUD & Analytics)
# ==========================================

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    section = request.form.get("section")
    grade_str = request.form.get("grade")

    # Data Validation & Error Handling (Requirement #4)
    if not name or not grade_str or not section:
        return "Error: Missing fields. <br><a href='/add_student_form'>Go back</a>", 400

    try:
        grade = int(grade_str)
    except ValueError:
        return "Error: Grade must be a number. <br><a href='/add_student_form'>Go back</a>", 400

    if grade < 0 or grade > 100:
        return "Error: Grade must be between 0 and 100. <br><a href='/add_student_form'>Go back</a>", 400

    new_id = max([s['id'] for s in students], default=0) + 1
    new_student = {
        "id": new_id,
        "name": name,
        "grade": grade,
        "section": section
    }
    students.append(new_student)
    
    # Redirect back to the interactive UI
    return redirect(url_for('list_students'))

@app.route('/delete_student/<int:id>', methods=['POST'])
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

# --- JSON/API Specific Routes (For external apps to use) ---

@app.route('/api/students', methods=['GET'])
def api_get_students():
    return jsonify(students)

@app.route('/api/student/<int:id>', methods=['GET'])
def api_get_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route('/api/summary', methods=['GET'])
def api_summary():
    if not students:
         return jsonify({"average": 0, "passed": 0, "failed": 0})
    
    grades = [s['grade'] for s in students]
    passed = len([g for g in grades if g >= 75])
    failed = len(grades) - passed
    avg = sum(grades) / len(grades)
    return jsonify({"average": avg, "passed": passed, "failed": failed})

# Authentication Example (Requirement #6)
@app.route('/api/secure_data', methods=['GET'])
def secure_data():
    # Require ?api_key=super-secret-key-123 in the URL
    provided_key = request.args.get('api_key')
    if provided_key != SECRET_API_KEY:
        return jsonify({"error": "Unauthorized. Invalid API Key."}), 401
    
    return jsonify({"message": "Access Granted to secure data!", "data": students})

if __name__ == '__main__':
    app.run(debug=True)
