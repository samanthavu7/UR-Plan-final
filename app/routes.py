from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
# import firebase_admin
# from firebase_admin import credentials, firestore, initialize_app
# import pyrebase

# config = {
#     "apiKey": "AIzaSyAITqYy9_z2PlI_MICO1Ob-Ay18mWx6qmk",
#     "authDomain": "ur-plan.firebaseapp.com",
#     "databaseURL": "https://ur-plan.firebaseio.com",
#     "projectId": "ur-plan",
#     "storageBucket": "ur-plan.appspot.com",
#     "messagingSenderId": "893010591089",
#     "appId": "1:893010591089:web:c039574c91b33876768ad0",
#     "measurementId": "G-HRDWGFW0QW"
# }

# firebase = pyrebase.initialize_app(config)
# db = firebase.database()
# db_classes = db.child("classes").get().val().values()

# print(db_events)
# auth = firebase.auth()

#cred = credentials.Certificate("key.json")
#firebase_admin.initialize_app(cred)
# db = firestore.client()
# firebase.analytics()

@app.route('/student', methods=['GET', 'POST'])
def student():
    user = {'username': 'Chok'}

    if request.method == 'POST':
        days=request.form.getlist('days')
        time=request.form.getlist('time')
        classes=request.form.get('classes')
        courses="CS010" #hardcoded cos firebase does not work
        # database querying
        return render_template('termplan.html', days=days, time=time, classes=classes, courses=courses)
    return render_template('student.html', title='Home', user=user)

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

# if __name__ == '__main__':
app.run(debug=True)