from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    # Grab name, grade, and section from the URL parameters
    name = request.args.get('name', 'Liemar Labtic')
    grade = int(request.args.get('grade', 96))
    section = request.args.get('section', 'Zechariah')
    
    remarks = "Pass" if grade >= 75 else "Fail"
    
    return jsonify({
        "name": name,
        "grade": grade,
        "section": section,
        "remarks": remarks
    })
