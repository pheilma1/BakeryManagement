from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FieldList, FormField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, URL, Email
from wtforms.fields import DateField
from flask_ckeditor import CKEditorField
from datetime import date

class SupplierForm(FlaskForm):
    supplier = StringField('Supplier Name', validators=[DataRequired()])
    submit = SubmitField(label="Add Supplier")

class SupplierItemForm(FlaskForm):
#    supplier_name = SelectField('Choose a supplier',  [DataRequired()], coerce=str)
    supplier_name = StringField('Supplier Name', validators=[DataRequired()])
    supitem_name = StringField('Item Name', validators=[DataRequired()])
    supitem_number = StringField('Item Number')
    supitem_size = DecimalField('Size', validators=[DataRequired()])
    supitem_uom = StringField('UOM (e.g. weight)', validators=[DataRequired()])
    supitem_cost = DecimalField('Cost', places=2)
    submit = SubmitField(label="Add Item")


# Category : Cutouts, Drop Cookes, Bars, Nuffins
# Item: Small Cutout Cookies, Large Cutout Cookies,
# Ingredient
# Ingredient Measurement (how much and what size of measuring device (e.g 1 cup, 9.5 pounds)

class RecipeForm(FlaskForm):
    recipe_name = StringField('Item Name', validators=[DataRequired()])
    ingredient_name = StringField('Ingredient', validators=[DataRequired()])
    ingredient_amount = IntegerField('Ingredient', validators=[DataRequired()])
    ingredient_uom = StringField('Measurement (e.g. Lbs, cups)', validators=[DataRequired()])
    submit = SubmitField(label="Add Supplier")

class Items(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    recipes = FieldList(FormField(RecipeForm), min_entries=1)

# class UOMForm(FlaskForm):
#     ingredient_qty = IntegerField('Ingredient Quantity', validators=[DataRequired()])
#     ingredient_uom = StringField('Measurement (e.g. Lbs, cups)', validators=[DataRequired()])

class IngredientForm(FlaskForm):
    # item_name = StringField('Item Name', validators=[DataRequired()])
    ingredient_name = StringField('Ingredient Name', validators=[DataRequired()])
    # ingredient_measure = FormField(UOMForm)
    # Order quantity really should be based on a supplier->item. E.G. Get 50lbs of FLour from Kecks, 5LB flour from Walmart
    ingredient_qty = IntegerField('Ingredient Quantity', validators=[DataRequired()])
    ingredient_uom = StringField('Measurement (e.g. Lbs, cups)', validators=[DataRequired()])
    ingredient_cost = DecimalField('Cost', places=2)
    ingredient_category = StringField('Category', validators=[DataRequired()])
    ingredient_class = StringField('Class', validators=[DataRequired()])
    submit = SubmitField(label="Add Ingredient")


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# Note: In PyCharm, had to run pip install email_validator for this to work
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField(label="Sign Me Up")


# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField(label="Let Me In")


# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField(label="Submit Comment")

class MileageForm(FlaskForm):
    # item_name = StringField('Item Name', validators=[DataRequired()])
    # date = DateField('Date', format='%m/%d/%y') #, validators=[DataRequired()])
    mileage_date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    starting_mileage = IntegerField('Starting Mileage', validators=[DataRequired()])
    ending_mileage = IntegerField('Ending Mileage', validators=[DataRequired()])
    submit = SubmitField(label="Save Mileage")


#TODO: May need to add starting mileage into the INIT in order for it to be seen in the form.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.mileage_date.data:
            self.mileage_date.data = date.today()

    def set_starting_mileage(self, value):
        self.starting_mileage = value

#TODO need a way to change the customer name?
# Customer Name, Day, Items, Quantities

#TODO The form needs to show the item name and the order quantity.
# Allow the items/order qty to be copied and applied to another day
# how do they add a new item to the order? Add a button in the header - add item then a pop-up with checkboxes to add multiple items
class CustomerOrderForm(FlaskForm):
#    supplier_name = SelectField('Choose a supplier',  [DataRequired()], coerce=str)
    customer_name = StringField('Customer', validators=[DataRequired()])
    item = StringField('Item Name', validators=[DataRequired()])
    monday_qty = IntegerField('Monday', validators=[DataRequired()])
    tuesday_qty = IntegerField('Tuesday', validators=[DataRequired()])
    wednesday_qty = IntegerField('Wednesday', validators=[DataRequired()])
    thursday_qty = IntegerField('Thursday', validators=[DataRequired()])
    friday_qty = IntegerField('Friday', validators=[DataRequired()])
    # supitem_number = StringField('Item Number')
    # supitem_size = DecimalField('Size', validators=[DataRequired()])
    # supitem_uom = StringField('UOM (e.g. weight)', validators=[DataRequired()])
    # supitem_cost = DecimalField('Cost', places=2)
    # submit = SubmitField(label="Add Item")

class OrderScheduleForm(FlaskForm):
    customer_name = StringField('Supplier Name', validators=[DataRequired()])
    #TODO Is it possible to select days in a checkbox format and items too?
    order_day = StringField('Item Name', validators=[DataRequired()])
    customer_name = StringField('Supplier Name', validators=[DataRequired()])



