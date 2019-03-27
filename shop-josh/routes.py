import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Author, Book, User, Cart, Wishlist
from shop.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=['GET','POST'])

@app.route("/home", methods=['GET','POST'])
def home():
    books = Book.query.all()
    return render_template('home.html', books=books, title='My Wonderful Book Shop')

@app.route("/home_author_sort_asc", methods=['GET','POST'])
def home_author_sort_asc():
    books = Book.query.order_by(Book.title.asc())
    return render_template('home.html', books=books, title='My Wonderful Book Shop')

@app.route("/home_author_sort_desc", methods=['GET','POST'])
def home_author_sort_desc():
    books = Book.query.order_by(Book.title.desc())
    return render_template('home.html', books=books, title='My Wonderful Book Shop')

@app.route("/home_price_sort_asc", methods=['GET','POST'])
def home_price_sort_asc():
    books = Book.query.order_by(Book.price.asc())
    return render_template('home.html', books=books, title='My Wonderful Book Shop')

@app.route("/home_price_sort_desc", methods=['GET','POST'])
def home_price_sort_desc():
    books = Book.query.order_by(Book.price.desc())
    return render_template('home.html', books=books, title='My Wonderful Book Shop')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)

    return render_template('book.html', book=book)

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

@app.route("/add_to_cart/<int:book_id>")
def add_to_cart(book_id):
    user_id=current_user.id
    add_cart= Cart(book_id = book_id, user_id = user_id)
    db.session.add(add_cart)
    db.session.commit()

    flash("The book is added to your shopping cart!")
    return redirect("/cart")

@app.route("/add_to_wishlist/<int:book_id>")
def add_to_wishlist(book_id):
    user_id=current_user.id
    add_cart= Wishlist(book_id = book_id, user_id = user_id)
    db.session.add(add_cart)
    db.session.commit()

    flash("The book is added to your wishlist!")
    return redirect("/wishlist")

@app.route("/cart", methods=['GET', 'POST'])
def cart_display():
    if current_user.is_authenticated:
        carts = Cart.query.filter_by(user_id = current_user.id).all()
        items = {}
        totalPrice = 0
        totalQuantity = 0

        for cart in carts:
            book = Book.query.get_or_404(cart.book_id)
            totalPrice += book.price
            if book.id in items:
                items[book.id]["quantity:"] += 1
            else:
                items[book.id] = {"quantity":1, "title": book.title, "price": book.price}
        return render_template("cart.html", title = "Shopping Cart", display_cart = items, total = totalPrice, totalQuantity = totalQuantity)
    else:
        flash("You must be logged in to do that.")
        return redirect('/home')

@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist_display():
    if current_user.is_authenticated:
        wishlists = Wishlist.query.filter_by(user_id = current_user.id).all()
        items = {}
        totalPrice = 0
        totalQuantity = 0

        for wishlist in wishlists:
            book = Book.query.get_or_404(wishlist.book_id)
            totalPrice += book.price
            if book.id in items:
                items[book.id]["quantity:"] += 1
            else:
                items[book.id] = {"quantity":1, "title": book.title, "price": book.price}
        return render_template("wishlist.html", title = "Wishlist", display_wishlist = items, total = totalPrice, totalQuantity = totalQuantity)
    else:
        flash("You must be logged in to do that.")
        return redirect('/home')

@app.route("/delete_book/<int:book_id>", methods=['GET', 'POST'])
def delete_book(book_id):
    carts = Cart.query.filter_by(user_id = current_user.id, photo_id= photo_id).first()
    db.session.delete(carts)
    db.session.commit()

    flash("The book has been removed from your shopping cart!")

    return redirect("/cart")

@app.route("/delete_wishlist/<int:book_id>", methods=['GET', 'POST'])
def delete_book_w(book_id):
    wishlists = Wishlist.query.filter_by(user_id = current_user.id, photo_id= photo_id).first()
    db.session.delete(wishlist)
    db.session.selete

    flash("The book has been removed from your wishlist!")

    return redirect("/wishlist")

@app.route("/search", methods=['GET', 'POST'])

def search():
    search=""
    books = Book.query.all()
    if request.method == 'POST':
        search = request.form['searchEntry']
    if search == "":
        flash("Your query found no results")
        return render_template('home.html', books=books, title="Search")
    books = Book.query.filter(Book.title.like("%" + search + "%"))
    return render_template('search.html', books=books, title="Search")
