import ast
import os
from flask import render_template, url_for, request, redirect, flash
from shop import app
global xTest
xTest = 0
global nmOfTest
nmOfTest = 0
global testName
testName = ''
global attemptsAtTest

def loginLS(userInput, userInput2):
    if userInput == '' and userInput2 == '':
        return "/home"
    if userInput.startswith("s"):

        with open('StudentAccounts.txt') as f:
            studentFile = f.readlines()
            for student in studentFile:
                stdId, stdPass = student.strip().split(" ",1)        
    
            with open('StudentAccounts.txt') as f:
                for line in f:
                    stdId, stdPass = line.strip().split()
                    if userInput == stdId:
                        if userInput2 == stdPass:
                            flash("Access Granted")
                            return "/studentP"
                    else:
                        flash("--Wrong Username or Password--")
                        return "/home"

    else:

        with open('LecturerAccounts.txt') as h:
            lecturerFile = h.readlines()
            for lecturer in lecturerFile:
                lctId, lctPass = lecturer.strip().split(" ",1)
    
            with open('LecturerAccounts.txt') as h:
                for line in h:
                    lctId, lctPass = line.strip().split()
                    if userInput == lctId:
                        if userInput2 == lctPass:
                            flash("Access Granted")
                            return "/lecturerP"
                    else:
                        flash("--Wrong Username or Password--")
                        return "/home"


def readDBA():
    answ=[]
    global testName
    with open('testdatabase.txt') as fo:
        for lines in fo:
            temp = lines.split("'")
            if temp[1] == testName:
                answers = lines
    start = answers.find('{')
    end = answers.find('}')

    answers = answers[start:end+1]
    answers = ast.literal_eval(answers)
    for i in answers.values():
        answ.append(i)
    return answ

def readDBName():
    tests = []

    with open('testdatabase.txt', 'r') as fo:
        for lines in fo:
            temp = lines.split("'")
            tests.append(temp[1])
    fo.close()
    return tests

@app.route("/advancedresults", methods=['GET','POST'])
def advancedresults():

    return render_template('advancedresults.html')

@app.route("/feedback", methods=['GET','POST'])
def feedback():
    global attemptsAtTest
    global nmOfTest
    global testDic
    s1=[]
    count=0

    if request.method == 'POST':
        for i in range(nmOfTest):
            i = str(i)
            s1.append(request.form[i])
    a1 = readDBA()

    for l in range(len(a1)):
        for j in s1:
            if str(j) == str(a1[l][0]):
                count+=1
    attemptsAtTest +=1
    return render_template('feedback.html', i=s1, count=count, totalmark=len(s1))

@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    userinput = ''
    userinput2 = ''
    LSF = ""
    if request.method == 'POST':
        userinput = request.form['userinput']
        userinput2 = request.form['userinput2']
    LSF = loginLS(userinput, userinput2)
    if LSF == "/studentP":
        return redirect('/studentP')
    elif LSF == "/lecturerP":
        return redirect('/lecturerP')

    return render_template('home.html', title='Create test', page=LSF)

def FindDuplicates(in_list):
    unique = set(in_list)
    for each in unique:
        count = in_list.count(each)
        if count > 1:
            return True
    return False

@app.route("/lecturerP", methods=['GET', 'POST'])
def lecturerP():
    return render_template('lecturerP.html')

@app.route("/studentP", methods=['GET', 'POST'])
def studentP():
    tests=readDBName()

    return render_template('studentP.html', tests=tests)

@app.route("/viewTest", methods=['GET', 'POST'])
def viewTest():
    testDic = {}
    global xTest
    testType = ""
    testName = ""
    startDate = ""
    endDate = ""
    checkDup = False
    varQL = []

    if request.method == 'POST':
        # Pushes questions and answers into a dictionary
        testName = request.form['testName']
        testType = request.form['TTest']
        startDate = request.form['startDateTest']
        endDate = request.form['endDateTest']
        for i in range(0, int(xTest)):

            varQ = ""
            varA = ""
            varQ += "Q"+str(i)
            varA += "A"+str(i)
            varIAL =[]

            for j in range(1,4):

                varIA = ""
                varIA += "IA"+str(i)
                varIA+=str(j)
                varIAL.append(request.form[varIA])
            checkDup = FindDuplicates(varIAL)

            if checkDup == True:
                flash("Two of your incorrect answers were the same")
                return redirect('/lecturerP')

            varA = request.form[varA]
            varQ = request.form[varQ]
            for item in varIAL:
                if str(item).lower() == str(varA).lower():
                    flash("One of you incorrect answers was the same as the correct answers")
                    return redirect('/lecturerP')

            testDic[varQ] = varA, varIAL
    TNames = readDBName()
    for names in TNames:
        if str(testName) == str(names):
            flash("There is already a test name like this")
            return redirect('/lecturerP')
    test = testDic

    row = [testName, testType, startDate, endDate, testDic]
    with open('testdatabase.txt', 'a') as fo:
        fo.write("\n")
        fo.write(str(row))
    fo.close()

    return render_template('viewTest.html', test=test, TTest=testType, testName=testName,
            startDate=startDate, endDate=endDate, xTest=int(xTest))

@app.route("/createTest", methods=['GET', 'POST'])
def createTest():
    s1=''
    if request.method == 'POST':
        # request.form.get("symbol")
        s1 = request.form['nmTests']
        if int(s1) == 0:
            flash("Cannot have 0 questions")
            return redirect('/home')
    global xTest
    xTest = s1
    return render_template('createTest.html', xTest=int(xTest))

@app.route("/taketest", methods=['GET', 'POST'])
def taketest():
    global nmOfTest
    test = []
    global testName
    # take test testName
    # load test from file
    # display test
    # on submit record studentID testID results etc to file
    if request.method == 'POST':
        testName = request.form['testChoice']

        with open('testdatabase.txt') as fo:
            for lines in fo:
                temp = lines.split("'")
                if temp[1] == testName:
                    test = lines
        start = test.find('{')
        end = test.find('}')

    test = test[start:end+1]
    test = ast.literal_eval(test)
    nmOfTest = len(test)
    return render_template('takeTest.html', test=test, testName=testName, numbertest=len(test), zip=zip)
