from datetime import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import  relationship, DeclarativeBase, Mapped, mapped_column, join
from sqlalchemy import create_engine, Integer, String, Text, func, ForeignKey, Float, DateTime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# Import your forms from the forms.py
#from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
#import requests
from forms import SupplierForm, SupplierItemForm, IngredientForm, MileageForm, CustomerOrderForm
from labels import get_labels, get_label_summary, get_lbl_ingreds,  get_item_ingreds, get_packaging_labels
# , get_cust_order_sched, get_cust_order_summary)
from cust_orders import get_all_cust_order_sched, get_cust_order_summary, get_cust_order_sched

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

class Base(DeclarativeBase):
    pass

# # Replace with your actual database connection details
# engine = create_engine("postgresql://postgres:Gray0225pw@localhost/bakery.db")
#
# # Create a new database
# with engine.connect() as connection:
#     connection.execute("CREATE DATABASE new_database")

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bakery.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Gray0225pw@localhost/bakery.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


label_summary = get_label_summary()
cust_order_summary = get_cust_order_summary()


# TODO develop these tables:
#   Item categories - e.g. cookies, pies, muffins, etc
#   Ingredient categories - Dry Goods, Dairy, Liquied Cleaaning supplier
#   Ingredient classes - Flour, Sugar, Seasonings
#

# posts = relationship("BlogPost", back_populates="author")
# comments = relationship("Comment", back_populates="comment_author")
# This will act like a List of BlogPost objects attached to each User.
# The "author" refers to the author property in the BlogPost class.
# In the user class I had to put the Mapped annotation to make it work:
#
# posts: Mapped[List["BlogPost"]] = relationship("BlogPost", back_populates="author")
# comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="comment_author")


# CONFIGURE DATABASE TABLES
class Suppliers(db.Model):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_name: Mapped[str] = mapped_column(String(100))
    items = relationship("SupplierItems", back_populates="supplier_item")
    #TODO define and add additional supplier contact information

#TODO: Separate supplier costs for tracking cost and average cost. Should costs be in an order table? See option below
# class SupplierCosts(db.Model):
#   __tablename__ = "supplier_cost"
#   id: Mapped[int] = mapped_column(Integer, primary_key=True)
#   supplier_cost_id : Mapped[str] = mapped_column(Integer, ForeignKey("suppliers.id")
#   cost = relationship("SupplierItems", back_populates="supplier_item_cost")
#   supplier_cost_date: Mapped[str] = mapped_column(String(250), nullable=False)  #should/cam this be a date field

class SupplierItems(db.Model):
    __tablename__ = "supplier_item"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id : Mapped[str] = mapped_column(Integer, ForeignKey("suppliers.id"))
    supplier_item = relationship("Suppliers", back_populates="items")
    #    supplier_name : Mapped[str] = mapped_column(Text, nullable=False)
    supplier_item_name : Mapped[str] = mapped_column(Text, nullable=False)
    # The item bar-code or ordering number
    supplier_item_number: Mapped[str] = mapped_column(Text, nullable=True)
    # TODO Change _amt to _size here and below and in supplier_items.html
    supplier_item_size: Mapped[float] = mapped_column(Float)
    supplier_item_uom : Mapped[str] = mapped_column(Text, nullable=False)
    supplier_item_cost: Mapped[float] = mapped_column(Float)
    supplier_cost_updated: Mapped[str] = mapped_column(String(250), nullable=False)
    ingredient_supplier = relationship( "Ingredients", back_populates="supplier_item")


# class SupplierOrders(db.Model):
#   __tablename__ = "supplier_orders"
#   id: Mapped[int] = mapped_column(Integer, primary_key=True)
#   supplier_item_id: Mapped[int] = mapped_column(Integer, ForeignKey('supplier_item.id'))
#   supplier_item = relationship("SupplierItems", back_populates="ingredient_supplier")
#   supplier_inv_num = Mapped[str] = mapped_column(Text, nullable=False)
#   item_order_qty =  Mapped[Int] = mapped_column(Integer)
#   item_order_cost = Mapped[float] = mapped_column(Float)
#   order_date: Mapped[str] = mapped_column(String(250), nullable=False)  #should/cam this be a date field

# TODO develop customer orders:
#   Enable edit of orders
#   Print customer order summary for production
#   Allow usage of order to print labels (may have to exclude items (e.g. cutouts)

# A supplier provides items/ingredients that can be ordered and contribute to a recipe. One or more recipes create a sellable item.
# Sellable items can be ordered by customers.

class Ingredients(db.Model):
    __tablename__ = "ingredients"
    ingredient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingredient_name : Mapped[str] = mapped_column(Text, nullable=False)

    #TODO One-to-one relationship with SupplierItems
    supplier_item_id : Mapped[int] = mapped_column(Integer, ForeignKey('supplier_item.id'))
    supplier_item = relationship("SupplierItems", back_populates="ingredient_supplier")

    #TODO One-to-many relationship with Recipes
    ingredient_in_recipe = relationship("Recipes", back_populates="recipe_ingredient")

    # Order quantity really should be based on a supplier->item. E.G. Get 50lbs of FLour from Kecks, 5LB flour from Walmart
    # TODO: Is a supplier-item table required or can a db relationship be used with a supplier->ingredient table
    ingredient_qty: Mapped[float] = mapped_column(Float)
    # TODO: probably should have this be the UOM ID into the UOM table
    ingredient_uom : Mapped[str] = mapped_column(Text, nullable=False)
    #Category and Department are synonymous. EGs are Dry goods (flour, sugar), dairy (eggs),
    #TODO Need a category for wholesale-supplied items such as muffins, pretzel pastries, etc
    #TODO One-to-many relationship with Categories, Classes
    ingredient_category : Mapped[str] = mapped_column(Text, nullable=False)
    ingredient_class : Mapped[str] = mapped_column(Text, nullable=False)

class Recipes(db.Model):
    #TODO : be able to clone a recipe to reuse
    __tablename__ = "recipes"
    recipe_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_name: Mapped[str] = mapped_column(String(100))

    # TODO need a foreign key to the Ingredient table
    #TODO One-to-one relationship with SupplierItems
    recipe_ingredient_id : Mapped[int] = mapped_column(Integer, ForeignKey('ingredients.ingredient_id'))
    recipe_ingredient = relationship("Ingredients", back_populates="ingredient_in_recipe")
    #The number of cups, pounds, grams, ounces, tsps, etc
    uom_quantity: Mapped[float] = mapped_column(Float)
    # TODO need a foreign key to the UOMConversion table
    uom_measurement: Mapped[str] = mapped_column(Text, nullable=False)
#   TODO how do we include a time element?
    #    time_required: ???
    #The number of items that the recipe makes (e.g. 24 Chocolate Chip Cookies
    num_items: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationship to item table
    item_id : Mapped[int] = mapped_column(Integer, ForeignKey('items.id'))
    parent_item = relationship("Item", back_populates="item_recipe")

    recipe_description: Mapped[str] = mapped_column(Text, nullable=False)
    recipe_instructions: Mapped[str] = mapped_column(Text, nullable=False)

class Item(db.Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_name: Mapped[str] = mapped_column(String(100))
    # FK: Recipe
    # TODO One-to-many relationship to the Item Categories
    # FK: Category
    item_description: Mapped[str] = mapped_column(String(100))
    item_retail_price: Mapped[float] = mapped_column(Float)
    item_wholesale_price: Mapped[float] = mapped_column(Float)
    item_special_order_price: Mapped[float] = mapped_column(Float)
    # TODO One-to-many relationship to the Recipes
    item_recipe = relationship("Recipes", back_populates="parent_item")

class CustomerOrders(db.Model):
    __tablename__ = "customer_orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inv_num : Mapped[str] = mapped_column(Text, nullable=False)
    item_id : Mapped[int] = mapped_column(Integer, ForeignKey('items.id'))
    item_order_qty : Mapped[int] = mapped_column(Integer)
    item_order_price : Mapped[float] = mapped_column(Float)


class UOMConversion(db.Model):
    __tablename__ = "uom_conversion"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uom : Mapped[str] = mapped_column(String(100))
    tsps: Mapped[str] = mapped_column(String(100))
    tbsps: Mapped[str] = mapped_column(String(100))
    cups: Mapped[str] = mapped_column(String(100))
    ounces: Mapped[str] = mapped_column(String(100))
    pounds: Mapped[str] = mapped_column(String(100))
    grams: Mapped[str] = mapped_column(String(100))
    pints: Mapped[str] = mapped_column(String(100))
    quarts: Mapped[str] = mapped_column(String(100))
    gallons: Mapped[str] = mapped_column(String(100))


class Mileage(db.Model):
    __tablename__ = "mileage_log"
    mileage_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # ingredient_name : Mapped[str] = mapped_column(Text, nullable=False)
    # mileage_date = Column(DateTime, default=datetime.datetime.now())
    mileage_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))       #, default=datetime.datetime.now())
    # created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()

    # mileage_date: Mapped[str] = mapped_column(String(250), nullable=False)
    starting_mileage: Mapped[float] = mapped_column(Float)
    ending_mileage: Mapped[float] = mapped_column(Float)
    distance = ending_mileage - starting_mileage

#TODO should I include a total milage column to easily sum the numbers for the current year? I'd rather just select it with a formula.
#TODO it should be easy to get the starting mileage on the 1st date and the ending mileage from the most recent date and subtract the two.

with app.app_context():
    db.create_all()
    # TODO PH: This might be the place to create the admin user when used for the fir
    # new_user = User(
    #      email="pheilma1@gmail.com",
    #      name="Graham",
    #      password=generate_password_hash("Gray0225pw!", method='pbkdf2:sha256', salt_length=8)
    # )

@app.route('/', methods=['POST', 'GET'])
def home():

    if request.method == 'POST':
        print ("Error - you are in home you need to be somewhere else")

    # return render_template("index.html", all_posts=posts)
    result = db.session.execute(db.select(Suppliers))
    suppliers = result.scalars().all()
    return render_template("index.html", all_suppliers=suppliers)
#    return render_template("index.html")

@app.route('/table_test')
def table_test():
    # return render_template("index.html", all_posts=posts)
    return render_template("Button_table_test.html")
#    return render_template("index.html")f


@app.route('/login/')
def login():
    # return render_template("index.html", all_posts=posts)
    return render_template("login.html")

@app.route('/register/')
def register():
    # return render_template("index.html", all_posts=posts)
    return render_template("register.html")

@app.route('/supplier/', methods=['POST', 'GET'])
def add_supplier():
    supplier_form = SupplierForm()
    # return render_template("index.html", all_posts=posts)
    if supplier_form.validate_on_submit():
        supplier_name = request.form['supplier']

        result = db.session.execute(db.select(Suppliers).where(func.lower(Suppliers.supplier_name) == supplier_name))
        supplier = result.scalar()
        # # Note, email in db is unique so will only have one result.
        if supplier:
             # User already exists
             flash("This supplier is already available")
             return redirect(url_for('add_supplier'))

        new_supplier = Suppliers(
            supplier_name=request.form['supplier'],
        )
        # print(f"{request.form['email']}, {request.form['name']}, {request.form['password']}")
        #
        db.session.add(new_supplier)
        db.session.commit()

        print(f"Supplier:{supplier_name}")
        return (redirect(url_for('home')))
    return render_template('supplier.html', form=supplier_form)

# < form class ="form-inline"  method="POST" >
# {{render_field(form.supplier_name)}}
# < div class ="row no-gutters" >
# < div class ="col" >
#   {{form.supitem_name.label}}
# < / div >
# < div class ="col" >
# {{form.supitem_name}}
# < / div >
# < / div >
# < / form >
#
#   <input type="hidden" name="name" value="value" />
#   <a onclick="this.parentNode.submit();">click here</a>

def add_supplier2(new_supplier_name):
    result = db.session.execute(db.select(Suppliers).where(func.lower(Suppliers.supplier_name) == new_supplier_name))
    supplier = result.scalar()
    if supplier:
         # User already exists
         flash("This supplier is already available")
         return

    # print(f"{request.form['email']}, {request.form['name']}, {request.form['password']}")
    #
    new_supplier = Suppliers(
        supplier_name=new_supplier_name
    )
    db.session.add(new_supplier)
    db.session.commit()

    return

#TODO Tie the supplier-items to the suppliers in the supplier table.
@app.route('/supplier_item/', methods=['POST', 'GET'])
def supplier_item():
    supplier_item_form = SupplierItemForm()
#TODO: Add a button to the SupplierItem Form to add the Supplier before enetering the rest of the data
    # result = db.session.execute(db.select(SupplierItems).order_by(SupplierItems.supplier_item_name))
    # supplier_items = result.scalars().all()
    # for sup_item in supplier_items:
    #     print (f"#1: {sup_item.supplier_item_name}")

    choices = []

    result = db.session.execute(db.select(SupplierItems).join(Suppliers.items).order_by(SupplierItems.supplier_item_name))
    # result = db.session.execute(db.select(Suppliers)).orderby(Suppliers.supplier_name)
    supplier_items = result.scalars().all()
    for sup_item in supplier_items:
        print (f"#2: {sup_item}, {sup_item.supplier_item.supplier_name}, {sup_item.supplier_item_name}, {sup_item.supplier_item_uom}, {sup_item.supplier_item_cost}")
        # result = db.session.execute(db.select(Suppliers).orderby(Suppliers.supplier_name))
        # supplier_items = result.scalars().all()

        seen = set()
        if sup_item.supplier_item.supplier_name not in seen:  # faster than `word not in output`
            seen.add(sup_item.supplier_item.supplier_name)
            choices.append(sup_item.supplier_item.supplier_name)
        supplier_item_form.supplier_name.choices = choices


    if supplier_item_form.validate_on_submit():
        supplier_name = request.form['supplier_name']
        print(supplier_name)
        result = db.session.execute(db.select(Suppliers).where(Suppliers.supplier_name == supplier_name))
        supplier = result.scalar()
        if not supplier:
            add_supplier2(supplier_name)
            result = db.session.execute(db.select(Suppliers).where(Suppliers.supplier_name == supplier_name))
            supplier = result.scalar()
        #print (supplier.id)

        # supitem_name = request.form['supitem_name']
        #
        # #TODO Check to see if the supplier/item combination already is in the database
        # result = db.session.execute(db.select(Suppliers, SupplierItems).where((func.lower(Suppliers.supplier_name) == supplier_name) and
        #                                                 (func.lower(SupplierItems.supplier_item_name) == supitem_name)))
        #
        # #TODO Make this more production-ready. Find out how to combine these 2 queries. Check for errors if the supplier isn't found.

#      result = db.session.execute(db.select(Suppliers).where( (func.lower(Suppliers.supplier_name) == supplier_name)))
#        result = db.session.execute(db.select(SupplierItems).where( (Suppliers.supplier_id) == supplier_name) and
#                                                                    (func.lower(SupplierItems.supplier_item_name) == supitem_name) ))

        # supplier_item = result.scalar()
        # print (supplier_item)
        # if supplier_item:
        #      # Supplier/item combination already exists
        #      flash("This supplier already has this item")
        #      return redirect(url_for('supplier_item'))

        requested_supplier = db.get_or_404(Suppliers, supplier.id)
        new_supplier_item = SupplierItems(
            supplier_item_name=request.form['supitem_name'],
            supplier_item_number=request.form['supitem_number'],
            supplier_item_size=request.form['supitem_size'],
            supplier_item_uom=request.form['supitem_uom'],
            supplier_item_cost=request.form['supitem_cost'],
            supplier_item = requested_supplier,
            supplier_cost_updated = date.today().strftime("%B %d, %Y")
        )

        db.session.add(new_supplier_item)
        db.session.commit()
        return (redirect(url_for('supplier_item')))
    return render_template('supplier_items.html', supplier_items=supplier_items, form=supplier_item_form)

    # TODO Render two forms in the HTML
    # return render_template('index.html', register_form=register_form, login_form=login_form)


#------------------------------------------------------

#TODO There will be 2 methods
# 1. "GET" the Suppliers and List of Items to display
# 2. "POST" LTie the supplier-items to the suppliers in the supplier table.
@app.route('/supplier_item_backup/<int:supplier_id>', methods=['POST', 'GET'])
def supplier_item_backup(supplier_id):
    supplier_item_form = SupplierItemForm()
#TODO: Add a button to the SupplierItem Form to add the Supplier before entering the rest of the data
    # result = db.session.execute(db.select(SupplierItems).order_by(SupplierItems.supplier_item_name))
    # supplier_items = result.scalars().all()
    # for sup_item in supplier_items:
    #     print (f"#1: {sup_item.supplier_item_name}")


    result = db.session.execute(db.select(SupplierItems).join(Suppliers.items).orderbySupplierItems.supplier_item_name)
    supplier_items = result.scalars().all()
    for sup_item in supplier_items:
        print (f"#2: {sup_item}, {sup_item.supplier_item.supplier_name}, {sup_item.supplier_item_name}, {sup_item.supplier_item_uom}, {sup_item.supplier_item_cost}")


    if supplier_item_form.validate_on_submit():
        supplier_name = request.form['supplier_name']
        supitem_name = request.form['supitem_name']

        #TODO Check to see if the supplier/item combination already is in the database
        result = db.session.execute(db.select(Suppliers, SupplierItems).where((func.lower(Suppliers.supplier_name) == supplier_name) and
                                                        (func.lower(SupplierItems.supplier_item_name) == supitem_name)))

        #TODO Make this more production-ready. Find out how to combine these 2 queries. Check for errors if the supplier isn't found.

#      result = db.session.execute(db.select(Suppliers).where( (func.lower(Suppliers.supplier_name) == supplier_name)))
#        result = db.session.execute(db.select(SupplierItems).where( (Suppliers.supplier_id) == supplier_name) and
#                                                                    (func.lower(SupplierItems.supplier_item_name) == supitem_name) ))

        supplier_item = result.scalar()
        print (supplier_item)
        if supplier_item:
             # Supplier/item combination already exists
             flash("This supplier already has this item")
             return redirect(url_for('supplier_item'))



        requested_supplier = db.get_or_404(Suppliers, 1)

        new_supplier_item = SupplierItems(
            supplier_item_name=request.form['supitem_name'],
            supplier_item_number=request.form['supitem_number'],
            supplier_item_size=request.form['supitem_size'],
            supplier_item_uom=request.form['supitem_uom'],
            supplier_item_cost=request.form['supitem_cost'],
            supplier_item = requested_supplier,
            supplier_cost_updated = date.today().strftime("%B %d, %Y")
        )


        # @app.route("/post/<int:post_id>", methods=["POST", "GET"])
        # def show_post(post_id):
        # requested_post = db.get_or_404(BlogPost, post_id)
        #
        # new_comment = Comment (
        #     text=comment_form.comment.data,
        #     comment_author=current_user,
        #     parent_post=requested_post
        # )
        # db.session.add(new_comment)

        # print(f"{request.form['email']}, {request.form['name']}, {request.form['password']}")
        #
        db.session.add(new_supplier_item)
        db.session.commit()
        return (redirect(url_for('supplier_item')))
    return render_template('supplier_items.html', supplier_items=supplier_items, form=supplier_item_form)



#------------------------------------------------------

#    return render_template("supplier.html", form=supplier_form)

# @app.route("/about/")
# def about():
#     return render_template("about.html")
#
#
# @app.route("/contact")
# def contact():
#     return render_template("contact.html")
#
#
# @app.route("/post/<int:index>")
# def show_post(index):
#     requested_post = None
#     for blog_post in posts:
#         if blog_post["id"] == index:
#             requested_post = blog_post
#     return render_template("post.html", post=requested_post)
#

@app.route('/recipes/')
def recipes():
    # return render_template("index.html", all_posts=posts)
    result = db.session.execute(db.select(Recipes))
    recipes = result.scalars().all()
    return render_template("index.html", all_posts=recipes)
    return render_template("recipes.html")

@app.route('/ingredients/', methods=['POST', 'GET'])
def ingredients():
    ingredient_form = IngredientForm()
    result = db.session.execute(db.select(Ingredients).order_by(Ingredients.ingredient_name))

    ingredients = result.scalars().all()

    if ingredient_form.validate_on_submit():
        new_ingredient = Ingredients(
            ingredient_name=ingredient_form.ingredient_name.data,
            ingredient_qty=ingredient_form.ingredient_qty.data,
            ingredient_uom=ingredient_form.ingredient_uom.data,
            ingredient_category=ingredient_form.ingredient_category.data,
            ingredient_class=ingredient_form.ingredient_class.data,
        )

        db.session.add(new_ingredient)
        db.session.commit()
        return (redirect(url_for('ingredients')))
    else:
        return render_template('ingredients.html', all_ingredients=ingredients, form=ingredient_form)

@app.route('/cust_order_items/', methods=['POST', 'GET'])
def cust_order_items():
    # cust_order_schedule = get_all_cust_order_sched()
    cust_order_summary = get_cust_order_summary()
    cust_order_form = CustomerOrderForm()
    customer_orders = []

    print("In Customer Order Items")
    if request.method == 'POST':
        print("In select cust_orders post")

        # print (request.form.items())

        tmp_data = {}
        for key, val in request.form.items():
            print(f"key, val: {key}, {val}")
            tmp_data[key] = val
            print(f"tmp_data = {tmp_data}")
            customer_orders = get_cust_order_sched(val)
            print(f"customer Orders for {val}: {customer_orders}")

            for items in customer_orders:
                print (f"items-{items}")
                cust_order_form.customer_name.data = val
                cust_order_form.item.data = items['Item']
                # if items['day'] == 'Monday':
                cust_order_form.monday_qty.data = items['Monday']
                # if items['day'] == 'Tuesday':
                cust_order_form.tuesday_qty.data = items['Tuesday']
                # if items['day'] == 'Wednesday':
                cust_order_form.wednesday_qty.data = items['Wednesday']
                # if items['day'] == 'Thursday':
                cust_order_form.thursday_qty.data = items['Thursday']
                # if items['day'] == 'Friday':
                cust_order_form.friday_qty.data = items['Friday']

            # tuesday_qty = IntegerField('Tuesday', validators=[DataRequired()])
            # wednesday_qty = IntegerField('Wednesday', validators=[DataRequired()])
            # thursday_qty = IntegerField('Thursday', validators=[DataRequired()])
            # friday_qty = IntegerField('Friday', validators=[DataRequired()])

        return render_template("customer_orders.html", form=cust_order_form, cust_orders=cust_order_summary, cust_items=customer_orders)
        # return redirect(url_for("cust_orders"))

    all_items = get_item_ingreds()
    # return render_template("customer_orders.html", items=all_items, days=day_list, cust_scheds=cust_order_schedule,
    #                        form=cust_order_form, cust_orders=cust_order_summary)
    return render_template("customer_orders.html",form=cust_order_form, cust_orders=cust_order_summary, cust_items=customer_orders)


@app.route('/cust_orders/', methods=['POST', 'GET'])
def cust_orders():

# TODO:
#   Display the customer's orders for each day, the items and order quantities
#   who have deliveries for today with a summary of the items and labels
#   Allow the user to change the day, select/unselect the customers
#       or select the day and show all customers who have orders for that day
#       What about printing all labels for all customers for the day? Separate each customer with a row - 1st label has the customer name?
#   Edit the number of labels for each item (tying this into the customer order would be great.)
#   Create a printable html file formatted with all the labels.
#   Maybe show total items and total labels for each item and overall for each customer as a santity check?

    cust_order_schedule = get_all_cust_order_sched()
    cust_order_summary = get_cust_order_summary()
    cust_order_form = CustomerOrderForm()


    # label_summary = get_label_summary()
    # print(label_summary)
    #
    print ("In Customer Orders")
    if request.method == 'POST':
        print("In select cust_orders post")

        # print (request.form.items())

        tmp_data = {}
        for key, val in request.form.items():
            print(f"key, val: {key}, {val}")
            tmp_data[key] = val
            print(f"tmp_data = {tmp_data}")
            customer_orders = get_cust_order_sched(val)
            print (f"customer Orders for {val}: {customer_orders}")

            for items in customer_orders:
                cust_order_form.customer_name.data = val
                cust_order_form.item.data = items['item']
                if items['day'] == 'Monday':
                    cust_order_form.monday_qty.data = items['order_qty']

            # tuesday_qty = IntegerField('Tuesday', validators=[DataRequired()])
            # wednesday_qty = IntegerField('Wednesday', validators=[DataRequired()])
            # thursday_qty = IntegerField('Thursday', validators=[DataRequired()])
            # friday_qty = IntegerField('Friday', validators=[DataRequired()])

        return redirect(url_for("cust_orders"))
        # return render_template("select_labels.html", all_custs=label_summary)

    day_list = []
    cust_list = []
    # day_dict = {}
    for x in label_summary:
        if not day_list:
            day_dict = {'day': x['day']}
            day_list.append(day_dict)
        else:
            if not any(d['day'] == x['day'] for d in day_list):
                day_dict = {'day': x['day']}
                day_list.append(day_dict)

        if not cust_list:
            cust_dict = {'cust': x['location']}
            cust_list.append(cust_dict)
        else:
            if not any(d['cust'] == x['location'] for d in cust_list):
                cust_dict = {'cust': x['location']}
                cust_list.append(cust_dict)

    print (f"day_list: {day_list}")
    # result = db.session.execute(db.select(Suppliers))
    # suppliers = result.scalars().all()


# if request.method == 'POST':
# # Then get the data from the form
# tag = request.form['tag']

    # return render_template("select_labels.html", all_custs=label_summary, all_days = day_list)
    all_items = get_item_ingreds()
    return render_template("customer_orders.html",form=cust_order_form, cust_orders=cust_order_summary)
    # return render_template("customer_orders.html", items=all_items, days=day_list, cust_scheds=cust_order_schedule, form=cust_order_form, cust_orders=cust_order_summary)



@app.route('/mileage/', methods=['POST', 'GET'])
def mileage():
    mileage_form = MileageForm()
    result = db.session.execute(db.select(Mileage).order_by(Mileage.mileage_date))

    mileage_entries = result.scalars().all()
    if not mileage_entries:
        print ("No entries yet")

    if mileage_form.validate_on_submit():
        # error = None
        print("checking mileage")
        # %Y - %m - %d
        # print(f"Date: {date.today().strftime('%B %d, %Y')}"),
        print(f"Date: {mileage_form.mileage_date.data}"),

        print(f"Starting: {mileage_form.starting_mileage.data}"),
        print(f"Ending:{mileage_form.ending_mileage.data}"),
        # mileage_date = (datetime.strptime(mileage_form.date, %Y-%m-%d)),

        mileage_str = str(mileage_form.mileage_date.data)
        print (mileage_str)
        if mileage_form.starting_mileage.data > mileage_form.ending_mileage.data:
            flash('Ending Milage Starting Mileage', 'error')
            # error = "Ending Mileage > Starting Mileage"
            return (redirect(url_for('mileage')))

        new_mileage_log = Mileage(
            mileage_date=(datetime.strptime(mileage_str, "%Y-%m-%d")),
            # datetime.strptime(datetime_str,
                              # "%d%m%y%H%M%S")datetime.strptime(datetime_str,
                              #    "%d%m%y%H%M%S")
            starting_mileage=mileage_form.starting_mileage.data,
            ending_mileage=mileage_form.ending_mileage.data,
        )

        print(new_mileage_log)
        db.session.add(new_mileage_log)
        db.session.commit()
        return (redirect(url_for('mileage')))
    else:
        total_mileage = 0
        for entry in mileage_entries:
            # print (f"Mileage entry: {entry.mileage_date}, {entry.starting_mileage}, {entry.ending_mileage}, {entry.distance}")
            total_mileage = total_mileage + (entry.ending_mileage - entry.starting_mileage)
            # curr_date = datetime.strptime("%y_%m_%d", localtime(time.time()))
            curr_date = datetime.today().date()
            print (f"curr date {curr_date}")
            # form_date = (datetime.strptime(mileage_str, "%Y-%m-%d")),
            #
            # my_user = Users.get(...)  # get your user object or whatever you need
            # if request.method == 'GET':
            #     form.username.data = my_user.username
            #     form.email.data = my_user.email
            #     # and on

        # mileage_form.set_starting_mileage(entry.ending_mileage)
        # print (f"total miles = {total_mileage}")
        if not mileage_entries:
            mileage_form.starting_mileage.data=0
        else:
            mileage_form.starting_mileage.data=entry.ending_mileage
        # mileage_form.mileage_date = curr_date
        return render_template('mileage.html', mileage_entries=mileage_entries, form=mileage_form, total_miles=total_mileage)

@app.route('/select_labels/', methods=['POST', 'GET'])
def select_labels():

# TODO:
#   Display the customers who have deliveries for today with a summary of the items and labels
#   Allow the user to change the day, select/unselect the customers
#       or select the day and show all customers who have orders for that day
#       What about printing all labels for all customers for the day? Separate each customer with a row - 1st label has the customer name?
#   Edit the number of labels for each item (tying this into the customer order would be great.)
#   Create a printable html file formatted with all the labels.
#   Maybe show total items and total labels for each item and overall for each customer as a santity check?

    # label_summary = get_label_summary()
    # print(label_summary)
    #
    # cust_order_schedule = get_all_cust_order_sched()
    # cust_order_summary = get_cust_order_summary()
    print (f"cust_order_summary: {cust_order_summary}")
    # cust_order_form = CustomerOrderForm()

    print ("In select labels")
    if request.method == 'POST':
        print("In select labels post")
        # print (request.form.items())

        tmp_data = {}
        for key, val in request.form.items():
            print(f"key, val: {key}, {val}")
            tmp_data[key] = val
            print(f"tmp_data = {tmp_data}")

            for custs in cust_order_summary:
                if custs["customer"] == key: #or racedict["league"] == key or racedict['section'] == key:
                    print("checking if it's on or off")
                    if val=="off":
                        if custs["print_lbl"] == "True":
                            print("Changing to False")
                            custs["print_lbl"] = 'False'
                    else:
                        if custs["print_lbl"] == "False":
                            print("Changing to True")
                            custs["print_lbl"] = 'True'

        return redirect(url_for("select_labels"))
        # return render_template("select_labels.html", all_custs=label_summary)

    day_list = []
    # day_dict = {}
    for x in label_summary:
        if not day_list:
            day_dict = {'day': x['day']}
            day_list.append(day_dict)
        else:
            if not any(d['day'] == x['day'] for d in day_list):
                day_dict = {'day': x['day']}
                day_list.append(day_dict)
    #
    # print (f"day_list: {day_list}")
    # result = db.session.execute(db.select(Suppliers))
    # suppliers = result.scalars().all()


# if request.method == 'POST':
# # Then get the data from the form
# tag = request.form['tag']

    # return render_template("select_labels.html", all_custs=label_summary, all_days = day_list)
    all_items = get_item_ingreds()
    return render_template("select_labels.html", all_custs=label_summary, items=all_items, days=day_list, cust_orders=cust_order_summary)

@app.route('/print_labels/', methods=['POST', 'GET'])
def print_labels():
    print("entered print labels 3")
    for labels in label_summary:
        print (f"{labels['location']}, {labels['day']}, {labels['on']}")

    # lbls_to_print = get_lbl_ingreds(label_summary)
    #TODO only get the packaging and item labels if the parameter is set
    packaging_labels = get_packaging_labels(cust_order_summary)
    print ( f"packaging labels = {packaging_labels}")
    lbls_to_print = get_lbl_ingreds(cust_order_summary)
    print (f" total labels {len(lbls_to_print)}")
    print(lbls_to_print)

    return render_template("print_lbls.html", all_labels=lbls_to_print)
    # return redirect(url_for("select_labels"))

@app.route('/labels/', methods=['POST', 'GET'])
def labels():

# TODO:
#   Select the customer (use today as the default?)
#       or select the day and show all customers who have orders for that day
#       What about printing all labels for all customers for the day? Separate each customer with a row - 1st label has the customer name?
#   Edit the number of labels for each item (tying this into the customer order would be great.)
#   Create a printable html file formatted with all the labels.
#   Maybe show total items and total labels for each item and overall for each customer as a santity check?

    labels = get_labels()
    print (labels)

    # result = db.session.execute(db.select(Suppliers))
    # suppliers = result.scalars().all()
    return render_template("labels.html", all_labels=labels)

@app.template_filter('length')
def length(s):
    return len(s)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
