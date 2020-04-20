from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from app.forms import CustomerRegForm, LoginForm
from app.models import Customer, Goods, Orders, OrderLineItem
import config
import random
import datetime

# Enable flask config
app = Flask(__name__)
# apply config to config.py
app.config.from_object(config)
# applies SQLAlchemy to db (database)
db = SQLAlchemy(app)


# route to registration page
@app.route('/reg', methods=['GET', 'POST'])
def register():
    # Refer to forms.py CustomerRegForm function
    form = CustomerRegForm()
    if request.method == 'POST':
        if form.validate():
            # Extract data from forms.py and insert into models.py database Customer(base)
            new_customer = Customer()
            new_customer.id = form.userid.data
            new_customer.name = form.name.data
            new_customer.password = form.password.data
            new_customer.address = form.address.data
            new_customer.birthday = form.birthday.data
            new_customer.phone = form.phone.data

            # Call Database SQLAlchemy lib, add record into DBMS
            db.session.add(new_customer)
            db.session.commit()
            print('registration success')
            return render_template('customer_reg_success.html', form=form)
    return render_template('customer_reg.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Refer to forms.py
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            c = db.session.query(Customer).filter_by(id=form.userid.data).first()
            if c is not None and c.password == form.password.data:
                print('Login success')
                print('!!! DEBUG c.id !!!', c.id)
                flash('Login success')
                flash('Welcome, ' + c.name)
                customer = {}
                customer['id'] = c.id
                customer['name'] = c.name
                customer['password'] = c.password
                customer['address'] = c.address
                customer['phone'] = c.phone
                customer['birthday'] = c.birthday
                # keep customer http session alive 
                session['customer'] = customer

                return redirect(url_for('main'))
            else:
                flash('Wrong UserID or Password, please try again !')
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)

# Logout the system, delete the session key
@app.route('/logout')
def logout():
    if 'customer' not in session.keys():
        flash('Please login to access this page')
        return redirect(url_for('login'))
    else:
        session.clear()
        flash('Logout Success')
    return redirect(url_for('login'))

# My account page
@app.route('/account')
def account():
    form = LoginForm()
    if 'customer' not in session.keys():
        flash('Please login to access this page')
        print('Logout')
        return redirect(url_for('login'))

    # Search goodsid and get details from DBMS DB_Files 
    cust = session['customer']
    list = []
    print('!!! DEBUG cust !!!', cust)
        # Item[0] = Fund ID
        # Item[1] = Fund name
        # Item[2] = Fund Price
        # Item[3] = Fund order quantity
        # subtotal = Fund total amount 
    print('!!! DEBUG address !!!', cust['address'])
    list.append((cust['id']))
    list.append((cust['name']))
    list.append((cust['address']))
    list.append((cust['phone']))
    list.append((cust['birthday']))

    print('!!! DEBUG list !!!', list[0])
    # Redirect to that product after fetching details from DBMS 
    return render_template('account.html', list=list)

# Website Stock Main Page
# Default redirect to home page after typing ip
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Shows the home page of the website, provide user option to choose 
@app.route('/main')
def main():
    # Redirect to login page if not yet logn, session not valid
    if 'customer' not in session.keys():
        flash('Please login to access this page')
        return redirect(url_for('login'))
    return render_template('main.html')

# Fund product list page 
@app.route('/list')
def show_goods_list():
    if 'customer' not in session.keys():
        flash('Please login to access this page')
        return redirect(url_for('login'))

    goodslist = db.session.query(Goods).all()
    return render_template('goods_list.html', list=goodslist)


# Display goods detail, links to goods_detail 
@app.route('/detail')
def show_goods_detail():
    if 'customer' not in session.keys():
        flash('Please login to access this page')
        print('Logout')
        return redirect(url_for('login'))

    # Connects goods_detail: goods, get all goods. info (eg. id, name, brand ...)
    goodsid = request.args['id']
    # Search goodsid and get details from DBMS DB_Files 
    goods = db.session.query(Goods).filter_by(id=goodsid).first()

    # Redirect to that product after fetching details from DBMS 
    return render_template('goods_detail.html', goods=goods)


# Add fund to cart, transfer data to add page
@app.route('/add')
def add_cart():
    if 'customer' not in session.keys():
        flash('Please login to access this page')
        return redirect(url_for('login'))

    # Get fund id, name, price from customer input in goods_list
    goodsid = int(request.args['id'])
    goodsname = request.args['name']
    goodsprice = float(request.args['price'])

    # Check any cart items in session 
    if 'cart' not in session.keys():
        session['cart'] = []  # Cart is list type

    # Get data from cart list 
    cart = session['cart']
    # Flag = 0 -> No previous add cart record
    # Flag = 1 -> Add to cart before, need n+1 action 
    flag = 0
    for item in cart:
        # Item[0] = Fund ID
        # Item[1] = Fund name
        # Item[2] = Fund Price
        # Item[3] = Fund order quantity
        # If same fund has been added already, add quantity to n+1
        if item[0] == goodsid:  # item[0] -> Fund ID
            item[3] += 1  # Fund Quantity +1 
            flag = 1
            break
        
    # Flag = 0 means the fund has not yet been added before, now add 
    if flag == 0:
        # System only allows one click add items, so the quantity must be +1 
        cart.append([goodsid, goodsname, goodsprice, 1])

    # Put the record in cart global session
    session['cart'] = cart

    print(cart)

    flash('Fund item(s) added【' + goodsname + '】to subscription cart')
    # Redirect to goods_list page by default after clicking the add to cart button 
    return redirect(url_for('show_goods_list'))


# Fund cart page 
@app.route('/cart')
def show_cart():
    if 'customer' not in session.keys():
        flash('Please login to access this page')
        return redirect(url_for('login'))

    if 'cart' not in session.keys():
        return render_template('cart.html', list=[], total=0.0)

    cart = session['cart']
    list = []
    total = 0.0
    print(cart)
    for item in cart:
        # Item[0] = Fund ID
        # Item[1] = Fund name
        # Item[2] = Fund Price
        # Item[3] = Fund order quantity
        # subtotal = Fund total amount 
        subtotal = item[2] * item[3]
        # total = grandtotal pending to pay amount 
        total += subtotal
        # Update cart function 
        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)
    # Pass the list and total to cart.html 
    return render_template('cart.html', list=list, total=total)


# Submit order
@app.route('/submit_order', methods=['POST'])
def submit_order():
    # Get data from form and insert into Orders() models.py
    orders = Orders()
    # Generate Order ID, capture current date time + random gen num
    n = random.randint(0, 9)
    d = datetime.datetime.today()
    print('Date and Time: ', d)
    orderid = str(int(d.timestamp() * 1e6)) + str(n)
    orders.id = orderid
    orders.orderdate = d.strftime('%Y-%m-%d %H:%M:%S')
    # status = 1 -> Pending for payment
    # status = 0 -> Paid already 
    orders.status = 1  

    db.session.add(orders)
    cart = session['cart']
    total = 0.0
    for item in cart:
        # Get the order quantity from cart.html quantity_
        quantity = request.form['quantity_' + str(item[0])]
        try:
            quantity = int(quantity)
        except:
            quantity = 0

        # calculte subtotal 
        subtotal = item[2] * quantity
        total += subtotal

        # Get data from form and insert into OrderLineItem() models.py
        order_line_item = OrderLineItem()
        order_line_item.quantity = quantity
        order_line_item.goodsid = item[0]
        order_line_item.orderid = orderid
        order_line_item.subtotal = subtotal
        db.session.add(order_line_item)
    orders.total = total
    # Submit current request to DBMS 
    db.session.commit()
    # Clear the fund cart 
    session.pop('cart', None)
    # After order submitted, redirect user to order_finish page 
    # Pass orderid to order_finish.html to show Order.No there
    return render_template('order_finish.html', orderid=orderid)
