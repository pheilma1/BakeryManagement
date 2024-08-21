from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FieldList, FormField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, URL, Email
from wtforms.fields import DateField
from flask_ckeditor import CKEditorField


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
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    starting_mileage = IntegerField('Starting Mileage', validators=[DataRequired()])
    ending_mileage = IntegerField('Ending Mileage', validators=[DataRequired()])
    submit = SubmitField(label="Save Mileage")


