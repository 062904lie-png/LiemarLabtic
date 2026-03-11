from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    # This creates a simple web form for the user to type in their info [cite: 63-70]
    html = """
    <h2>Enter Student Details</h2>
    <form action="/student" method="POST">
        Name: <input type="text" name="name" required><br><br>
        Grade: <input type="number" name="grade" required><br><br>
        Section: <input type="text" name="section" required><br><br>
        <input type="submit" value="Check Grade">
    </form>
    """
    return render_template_string(html)

@app.route('/student', methods=['POST'])
def get_student():
    # This grabs the exact data the user typed into the form 
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")
    
    # Calculate pass/fail
    remarks = "Pass" if grade >= 75 else "Fail"
    
    # Return the results as JSON
    return jsonify({
        "name": name,
        "grade": grade,
        "section": section,
        "remarks": remarks
    })
