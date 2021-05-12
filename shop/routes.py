import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Item, User
from shop.forms import RegistrationForm, LoginForm, SearchForm, CheckoutForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods= ['GET', 'POST'])

@app.route("/home", methods= ['GET', 'POST'])
def home():
	form = SearchForm()
	search = SearchForm(request.form)
	search_string = ""
	if request.method == 'POST':
		search_string = search.items['search']
		items = Item.query.filter_by(Item.title == search_string).first()
		return render_template('home.html', items=item, form=form)
	return render_template('home.html', items = Item.query.all(), title='Home')

@app.route("/about")
def about():
	return render_template('about.html', title='About')


@app.route("/Asc")
def Asc():
	return render_template('home.html', items = Item.query.order_by("price"), title='Home')

@app.route("/Desc")
def Desc():
	return render_template('home.html', items = Item.query.order_by("price")[::-1], title='Home')

@app.route("/item/<int:item_id>")
def item(item_id):
	item = Item.query.get_or_404(item_id)
	return render_template('item.html', item=item)

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


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
    	session["basket"] = []
    	return redirect(url_for('thankyou'))
    return render_template('checkout.html', title='Checkout', form=form)

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
		db.session.commit()
		session.clear()
		logout_user()
		return redirect(url_for('home'))

@app.route("/add_to_basket/<int:item_id>")
def add_to_basket(item_id):
	if "basket" not in session:
		session["basket"] = []
	session["basket"].append(item_id)
	flash("The item is added to your shopping basket!")
	return redirect("/basket")

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
            item = Item.query.get_or_404(item)

            total_price += item.price
            if item.id in basket:
                basket[item.id]["quantity"] += 1
            else:
                basket[item.id] = {"quantity":1, "title": item.title, "price":item.price}
            total_quantity = sum(item['quantity'] for item in basket.values())


        return render_template("basket.html", title='Your Shopping basket', display_basket = basket, total = total_price, total_quantity = total_quantity)

    return render_template('basket.html')

@app.route("/delete_item/<int:item_id>", methods=['GET', 'POST'])
def delete_item(item_id):
    if "basket" not in session:
        session["basket"] = []

    session["basket"].remove(item_id)

    flash("The item has been removed from your shopping basket!")

    session.modified = True

    return redirect("/basket")

@app.route("/add_to_wishlist/<int:item_id>")
def add_to_wishlist(item_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].append(item_id)
    flash("The item has been added to your wishlist")
    return redirect("/wishlist")

@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist_display():
    if "wishlist" not in session:
        flash('Your wishlist is empty.')
        return render_template("wishlist.html", display_wishlist = {}, total = 0)
    else:
        items = session["wishlist"]
        wishlist = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            item = Item.query.get_or_404(item)

            total_price += item.price
            if item.id in wishlist:
                wishlist[item.id]["quantity"] += 1
            else:
                wishlist[item.id] = {"quantity":1, "title": item.title, "price":item.price}
            total_quantity_wishlist = sum(item_id['quantity'] for item_id in wishlist.values())

        return render_template("wishlist.html", title= "Your Shopping Basket", display_wishlist = wishlist, total = total_price, total_quantity_wishlist = total_quantity_wishlist)

@app.route("/delete_item_wishlist/<int:item_id>", methods=['GET', 'POST'])
def delete_item_wishlist(item_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].remove(item_id)

    flash("The item has been removed from your wishlist")
    session.modified = True
    return redirect("/wishlist")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html", title='Thank You')
