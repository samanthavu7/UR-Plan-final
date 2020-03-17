from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app.forms import LoginForm
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

from app import URPlanClasses
from app.URPlanClasses import Class, Student
from app.designProjectScratch import ClassInfo, initCSCoreClass, initCSNonCoreClasses
from app.firebaseQueryTest01 import updateClassesToTake
from app.firebaseQueryTest02 import getClassesBasedOnDays, getClassesBasedOnTime
import google.cloud.exceptions

# import pyrebase

cred = credentials.Certificate('app/key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
# firebase.analytics()

@app.route('/student', methods=['GET', 'POST'])
def student():
    testList = []
    
    currentEmail = "svu008@ucr.edu"
    doc_refStudent = db.collection(u'students').where(u'studentEmail', u'==', currentEmail)
    try:
        docStudent = doc_refStudent.stream()
        for doc in docStudent:
            testList.append(Student.from_dict(doc.to_dict()))
        currentStudent = testList[0]
        currentCoursesTaken = currentStudent.coursesList[:]
        coreClasses = initCSCoreClass()
        nonCoreClasses = initCSNonCoreClasses()
        classesToQuery = []
        coreClasses = updateClassesToTake(currentCoursesTaken, coreClasses)
        nonCoreClasses = updateClassesToTake(currentCoursesTaken, nonCoreClasses)

        # print("Core classes that you can take after classes removal: ")
        # for classObj in coreClasses:
        #     if(not classObj.preReqtoTake):
        #         print(classObj.className + " can now be taken!")
        #         classesToQuery.append(classObj.className)

        # print("Classes in nonCore that can be taken")

        # for classObj2 in nonCoreClasses:
        #     if(not classObj2.preReqtoTake):
        #         print(classObj2.className + " can now be taken!")
        #         classesToQuery.append(classObj2.className)

    except google.cloud.exceptions.NotFound:
        print("Document Not Found")

    if request.method == 'POST':
        days=request.form.getlist('days')
        daysToBoolean = [False, False, False, False, False]
        for d in days:
            if d == 'Monday':
                daysToBoolean[0] = True
            elif d == 'Tuesday':
                daysToBoolean[1] = True
            elif d == 'Wednesday':
                daysToBoolean[2] = True
            elif d == 'Thursday':
                daysToBoolean[3] = True
            elif d == 'Friday':
                daysToBoolean[4] = True
        matchingClassesDays = getClassesBasedOnDays(
            db,
            daysToBoolean[0],
            daysToBoolean[1],
            daysToBoolean[2],
            daysToBoolean[3],
            daysToBoolean[4]
        )

        # Find classes that meet time preferences
        time=request.form.getlist('time')
        matchingClassesTime = getClassesBasedOnTime(db, int(time[0].replace(':','')), int(time[1].replace(':','')))

        #Intersection of matchingClassesDays and matchingClassesTime
        intersectList = [] #holds the intersection of the lists 
        for class1 in matchingClassesDays:
            for class2 in matchingClassesTime:
                if(class1.CRN == class2.CRN):
               	    intersectList.append(class2)

        coreList = initCSCoreClass() #has to have a fresh copy of coreClasses
        nonCoreList = initCSNonCoreClasses() #has to have a fresh copy of nonCoreClasses
        tupleList = []
        passedOnce = True
        for item in intersectList:
            passedOnce = True
            for classItem in coreList:
                if((item.courseName == classItem.className) and (passedOnce)):
                    passedOnce = False
                    tupleList.append((item, classItem.numDescendants()))
        for item in intersectList:
            passedOnce = True
            for classItem in nonCoreList:
                if((item.courseName == classItem.className) and (passedOnce)):
                    passedOnce = False
                    tupleList.append((item, classItem.numDescendants()))
        tupleList.sort(key=lambda x: x[1], reverse=True)
        print("Tuples:")
        for item5 in tupleList:
            print(item5)

        classes=request.form.get('classes')

        return render_template('schedule.html', tupleList=tupleList, classes=classes)

    return render_template('student.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

# if __name__ == '__main__':
app.run(debug=True)