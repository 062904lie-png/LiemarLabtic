from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    # Get grade from query parameter (default is set to 0) [cite: 27, 28]
    grade = int(request.args.get('grade', 0))
    
    # Determine pass or fail based on the grade [cite: 29, 30]
    remarks = "Pass" if grade >= 75 else "Fail"
    
    return jsonify({
        "name": "Your Name", # You can replace this with your actual name! [cite: 227]
        "grade": grade,
        "section": "Zechariah",
        "remarks": remarks
    })

