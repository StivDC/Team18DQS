import os
import random
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Author, Book, User
from shop.forms import RegistrationForm, LoginForm, cardEntry
from flask_login import login_user, current_user, logout_user, login_required

def sortings(s1, books):
    if s1 == 'PAsc':
        books = sorted(books, key=lambda x : x.price)
    elif s1 == 'PDsc':
        books = sorted(books, key=lambda x : x.price, reverse=True)
    elif s1 == 'Afn':
        books = sorted(books, key=lambda x : x.author.first_name)
    elif s1 == 'Asn':
        books = sorted(books, key=lambda x : x.author.last_name)
    elif s1 == 'Ais':
        books = sorted(books, key=lambda x : x.stock_level)
    else:
        return books
    return books

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    s1=''
    books = Book.query.all()
    if request.method == 'POST':
        s1 = request.form['sbp']
    books = sortings(s1, books)
    return render_template('home.html', books=books, title='My Wonderful Book Shop')

@app.route("/search", methods=['GET', 'POST'])
#Source for SQLAlchemy search like https://stackoverflow.com/questions/3325467/elixir-sqlalchemy-equivalent-to-sql-like-statement
def search():
    s2=""   
    books = Book.query.all()
    if request.method == 'POST':
        s2 = request.form['searchEntry']
    if s2 == "":
        flash("Your query matched no results")
        return render_template('home.html', books=books)
    books = Book.query.filter(Book.title.like("%" + s2 + "%"))
    return render_template('search.html', books=books)

@app.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)

    return render_template('book.html', book=book)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
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

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    form = cardEntry()
    if form.validate_on_submit():
        flash('Payment completed.')
        return redirect(url_for('order_number'))    
    return render_template('checkout.html', title='Checkout', form=form)


@app.route("/order_number", methods=["GET", "POST"])
def order_number():
    x=""
    for i in range(10):
        x+=str(random.randint(0,10))
    return render_template('/order_number.html', title='Order number', x=x)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/add_wishlist/<int:book_id>")
def add_wishlist(book_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].append(book_id)
    flash("This book has been added to your wishlist")
    return redirect('/wishlist')

@app.route("/add_to_basket_wishlist/<int:book_id>", methods=['GET', 'POST'])
def add_to_basket_wishlist(book_id):
    if "basket" not in session:
        session["basket"] = []

    session["basket"].append(book_id)


    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].remove(book_id)

    flash("The book is added to your shopping basket!")
    session.modified=True
    
    return redirect("/basket")


@app.route("/add_to_basket/<int:book_id>")
def add_to_basket(book_id):
    if "basket" not in session:
        session["basket"] = []

    session["basket"].append(book_id)

    session.modified=True
    return redirect("/basket")

@app.route("/delete_book_wishlist/<int:book_id>", methods=['GET', 'POST'])
def delete_book_wishlist(book_id):
    if "wishlist" not in session:
        session["wishlist"] = []

    session["wishlist"].remove(book_id)

    flash("This book has been removed from your wishlist!")

    session.modified = True

    return redirect("/wishlist")

@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist():
    if "wishlist" not in session:
        flash('There is nothing in your wishlist.')
        return render_template("wishlist.html", display_wishlist = {}, total = 0)
    else:
        items = session["wishlist"]
        wishlist = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            book = Book.query.get_or_404(item)

            total_price += book.price
            if book.id in wishlist:
                wishlist[book.id]["quantity"] += 1
            else:
                wishlist[book.id] = {"quantity":1, "title": book.title, "price":book.price}
            total_quantity = sum(item['quantity'] for item in wishlist.values())


        return render_template("wishlist.html", title='Your wishlist', display_wishlist = wishlist, total = total_price, total_quantity = total_quantity)

    return render_template('wishlist.html')



@app.route("/basket", methods=['GET', 'POST'])
def basket_display():
    if "basket" not in session:
        flash('There is nothing in your basket.')
        return render_template("basket.html", display_basket = {}, total = 0)
    else:
        items = session["basket"]
        basket = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            book = Book.query.get_or_404(item)

            total_price += book.price
            if book.id in basket:
                basket[book.id]["quantity"] += 1
            else:
                basket[book.id] = {"quantity":1, "title": book.title, "price":book.price}
            total_quantity = sum(item['quantity'] for item in basket.values())


        return render_template("basket.html", title='Your Shopping basket', display_basket = basket, total = total_price, total_quantity = total_quantity)

    return render_template('basket.html')



@app.route("/delete_book/<int:book_id>", methods=['GET', 'POST'])
def delete_book(book_id):
    if "basket" not in session:
        session["basket"] = []

    session["basket"].remove(book_id)

    flash("The book has been removed from your shopping basket!")

    session.modified = True

    return redirect("/basket")


