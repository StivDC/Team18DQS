import ast
import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import User
from shop.forms import RegistrationForm, LoginForm, takeTestForm
from flask_login import login_user, current_user, logout_user, login_required
global xTest
xTest = 0

def readDBName():
    tests = []

    with open('testdatabase.txt', 'r') as fo:
        for lines in fo:
            temp = lines.split("'")
            tests.append(temp[1])
    fo.close()
    return tests

@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    tests=readDBName()
    return render_template('home.html', title='Create test', tests=tests)

def FindDuplicates(in_list):
    unique = set(in_list)
    for each in unique:
        count = in_list.count(each)
        if count > 1:
            return True
    return False

@app.route("/viewTest", methods=['GET', 'POST'])
def viewTest():
    global xTest
    testDic = {}
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
                return redirect('/home')

            varA = request.form[varA]
            varQ = request.form[varQ]
            for item in varIAL:
                if str(item).lower() == str(varA).lower():
                    flash("One of you incorrect answers was the same as the correct answers")
                    return redirect('/home')

            testDic[varQ] = varA, varIAL
    TNames = readDBName()
    for names in TNames:
        if str(testName) == str(names):
            flash("There is already a test name like this")
            return redirect('/home')
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
    test = []
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

    return render_template('takeTest.html', test=test, testName=testName)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, first_name=form.first_name.data, surname=form.surname.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created.  You can now log in.')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You are now logged in.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')

        return render_template('login.html', form=form)

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))