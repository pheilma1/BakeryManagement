import pandas as pd

from docx import Document
from docx.shared import Pt
# from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.style import WD_STYLE_TYPE

import csv
from docx.shared import Cm, Inches

#TODO:
    # Enter items and ingredients into a CSV file
    # Read the file
    # Create a CSV file that contains the day, locations and order quantity of each item to print on a label
    # Create an HTML table that contains all the items and is formatted to print on the Avery label stock
    # Fix the Blueberry label misspellings

item_list = [
    {"item" : "Almond Croissants", "ingredients" : "Wheat Flour, Water, Butter (Cream), Sugar, Almonds, Yeast, Egg Whites, Invert Sugar Syrup, Egg, Salt, Wheat Gluten, Egg Yolks, Ascorbic Acid, Enzyme. Topping: Powdered Sugar. Contains Milk, Egg, Tree Nuts"},
    {"item": "Apple Turnovers", "ingredients" : "Apple Filling (Water, Sugar, Glucose, Evaporated Apples, Modified Corn Starch, Spice, Citric Acid, Sodium Benzoate and Potassium Sorbate (preservatives), Enriched Flour (Wheat Flour, Niacin, Iron, Thiamin Mononitrate, Riboflavin, Folic Acid, Water, Palm Oil, Sugar, Soybean Oil, Salt, Monocalcium Phosphate)"},
    {"item": "Blueberry Muffins", "ingredients": "Bleached Wheat Flour, Sugar, Eggs, Soybean Oil, Blueberries, Water, Modified Food Starch, Leavening (Baking Soda, Sodium Aluminum Phosphate, Monocalcium Phosphate), Mono and Diglycerides, Natural Flavor, Buttermilk Solids, Salt, Enzyme, Xanthan Gum."},
    {"item": "Chocolate Chip Muffins", "ingredients": "Need Ingredients"},
    {"item": "Blueberry Scones", "ingredients": "Need Ingredients"},
    {"item": "Raspberry Scones","ingredients": "Need Ingredients"},
    {"item": "Lemon Cheese Danish", "ingredients": "Need Ingredients"},
    {"item": "Spinach Feta", "ingredients": "Need Ingredients"},
    {"item": "Cranberry-Orange Muffins", "ingredients": "Need Ingredients"},
    {"item": "Chocolate Croissannts", "ingredients": "Need Ingredients"},
    {"item": "Cutout Cookies", "ingredients": "Need Ingredients"},
]

# TODO : Make this area a function call or class to for handling orders.
# Item Locations


customer_order_summary = [
    {"customer": "FL - MRB", "order_day": "Monday", "num_items": "8", "order_qty": "124"},
    {"customer": "FL - MRB", "order_day": "Tuesday", "num_items": "8", "order_qty": "116"},
    {"customer": "FL - MRB", "order_day": "Wednesday", "num_items": "0", "order_qty": "0"},
    {"customer": "FL - MRB", "order_day": "Thursday", "num_items": "8", "order_qty": "48"},
    {"customer": "FL - MRB", "order_day": "Friday","num_items": "0", "order_qty": "0"},
    {"customer": "FL - Main", "order_day": "Monday","num_items": "8", "order_qty": "310"},
    {"customer": "FL - Main", "order_day": "Tuesday","num_items": "8", "order_qty": "298"},
    {"customer": "FL - Main", "order_day": "Wednesday","num_items": "0", "order_qty": "0"},
    {"customer": "FL - Main", "order_day": "Thursday","num_items": "8", "order_qty": "78"},
    {"customer": "FL - Main", "order_day": "Friday","num_items": "6", "order_qty": "44"},
    {"customer": "FL - Thompson", "order_day": "Monday", "num_items": "0", "order_qty": "0"},
    {"customer": "FL - Thompson", "order_day": "Tuesday", "num_items": "12", "order_qty": "138"},
    {"customer": "FL - Thompson", "order_day": "Wednesday", "num_items": "0", "order_qty": "0"},
    {"customer": "FL - Thompson", "order_day": "Thursday", "num_items": "0", "order_qty": "0"},
    {"customer": "FL - Thompson", "order_day": "Friday", "num_items": "0", "order_qty": "0"},
    {"customer":"FL - Farmington", "order_day": "Monday", "num_items": "0", "order_qty": "0"},
    {"customer": "FL - Farmington", "order_day": "Tuesday", "num_items": "0", "order_qty": "0"},
    {"customer": "FL - Farmington", "order_day": "Wednesday", "num_items": "0", "order_qty": "0"},
    {"customer": "FL - Farmington", "order_day": "Thursday", "num_items": "28", "order_qty": "172"},
    {"customer": "FL - Farmington", "order_day": "Friday", "num_items": "0", "order_qty": "0"},
    {"customer":"Casa", "order_day": "Monday", "num_items": "0", "order_qty": "0"},
    {"customer": "Casa", "order_day": "Tuesday", "num_items": "3", "order_qty": "290"},
    {"customer": "Casa", "order_day": "Wednesday", "num_items": "0", "order_qty": "0"},
    {"customer": "Casa", "order_day": "Thursday", "num_items": "0", "order_qty": "0"},
    {"customer": "Casa", "order_day": "Friday", "num_items" : "1", "order_qty": "116"}
]


# products = [
#             ['Clean', {'number': '42565', 'name': 'Cleanex', 'price': '01.00', 'description': 'to clean'},
#                       {'number': '45217', 'name': 'Toothbrush', 'price': '01.50', 'description': 'oral hygiene'}],
#             ['Kitchen', {'number': '47851', 'name': 'Spaguetti', 'price': '01.00', 'description': 'Easy to cook'},
#              {'number': '5852', 'name': 'Rice', 'price': '1.00', 'description': 'For all family'}],
#             ['House', {'number': '78595', 'name': 'Door', 'price': '25.00', 'description': 'A resistant door'}]]

customer_order_summary_2 = [
    ["FL - MRB",
        {"order_day": "Monday", "num_items": "8", "order_qty": "124"},
        {"order_day": "Tuesday", "num_items": "8", "order_qty": "116"},
        {"order_day": "Wednesday", "num_items": "0", "order_qty": "0"},
        {"order_day": "Thursday", "num_items": "8", "order_qty": "48"},
        {"order_day": "Friday", "num_items": "0", "order_qty": "0"},
    ],
    ["FL - Main",
        {"order_day": "Monday","num_items": "8", "order_qty": "310"},
        {"order_day": "Tuesday","num_items": "8", "order_qty": "298"},
        {"order_day": "Wednesday","num_items": "0", "order_qty": "0"},
        {"order_day": "Thursday","num_items": "8", "order_qty": "78"},
        {"order_day": "Friday","num_items": "6", "order_qty": "44"},
    ],
    ["FL - Thompson",
        {"order_day": "Monday", "num_items": "0", "order_qty": "0"},
        {"order_day": "Tuesday", "num_items": "12", "order_qty": "138"},
        {"order_day": "Wednesday", "num_items": "0", "order_qty": "0"},
        {"order_day": "Thursday", "num_items": "0", "order_qty": "0"},
        {"order_day": "Friday", "num_items": "0", "order_qty": "0"},
    ],
    ["FL - Farmington",
        {"order_day": "Monday", "num_items": "0", "order_qty": "0"},
        {"order_day": "Tuesday", "num_items": "0", "order_qty": "0"},
        {"order_day": "Wednesday", "num_items": "0", "order_qty": "0"},
        {"order_day": "Thursday", "num_items": "28", "order_qty": "172"},
        {"order_day": "Friday", "num_items": "0", "order_qty": "0"},
    ],
    ["Casa",
        {"order_day": "Monday", "num_items": "0", "order_qty": "0"},
        {"order_day": "Tuesday", "num_items": "3", "order_qty": "290"},
        {"order_day": "Wednesday", "num_items": "0", "order_qty": "0"},
        {"order_day": "THursday", "num_items": "0", "order_qty": "0"},
        {"order_day": "Friday", "num_items" : "1", "order_qty": "116"}
    ]
]

order_quantities_by_item_by_day = [
    {"item": "Almond Croissants","day": "Monday", "Location": 'MRB', "Quantity" : "6"},
    {"item": "Almond Croissants","day": "Monday", "Location": 'Main', "Quantity" : "12"},
    {"item": "Apple Turnovers","day": "Monday", "Location": 'MRB', "Quantity" : "6"},
    {"item": "Apple Turnovers","day": "Monday", "Location": 'Main', "Quantity" : "12"},
    {"item": "Blueberry Muffins", "day": "Monday", "Location": 'MRB', "Quantity": "36"},
    {"item": "Blueberry Muffins", "day": "Monday", "Location": 'Main', "Quantity": "48"},
    {"item": "Blueberry Scones", "day": "Monday", "Location": 'MRB', "Quantity": "5"},
    {"item": "Blueberry Scones", "day": "Monday", "Location": 'Main', "Quantity": "16"},
    {"item": "Chocolate Chip Muffins", "day": "Monday", "Location": 'MRB', "Quantity": "36"},
    {"item": "Chocolate Chip Muffins", "day": "Monday", "Location": 'Main', "Quantity": "48"},
    {"item": "Lemon Creme Cheese Danish", "day": "Monday", "Location": 'MRB', "Quantity": "6"},
    {"item": "Lemon Creme Cheese Danish", "day": "Monday", "Location": 'Main', "Quantity": "6"},
]

item_dictionary = {
    "item" : "Almond Croissant",
    "ingredients" : "Wheat Flour, Water, Butter (Cream), Sugar, Almonds, Yeast, Egg Whites, Invert Sugar Syrup, Egg, Salt, Wheat Gluten, Egg Yolks, Ascorbic Acid, Enzyme. Topping: Powdered Sugar. Contains Milk, Egg, Tree Nuts"
}

notes = "We are not a nut-free facility\n16 W Main St. Shortsville NY 14548"

df_all_cust_orders = pd.read_csv('data/customer_orders.csv', index_col=False)

def set_cust_order(customer):
    cust_dict = {
        "customer": customer['Customer'],
        custs['Monday']: {
            'num_items': '1',
            'order_qty': custs['order_qty']
        }
    }
#TODO: move these function to a file/class specific to customer orders
def get_cust_order_summary():

    # print (f"df_all_cust_orders: {df_all_cust_orders}")
    df_cust_orders = df_all_cust_orders
    cust_orders = df_cust_orders.to_dict(orient='records')
    print (f"cust Orders Dict = {cust_orders} ")
    summary_df = df_cust_orders.groupby(['Customer'], as_index=False)[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']].sum()
    print (f"summary_df={summary_df}")

    # Using iterrows()
    # for index, row in summary_df.iterrows():
    #     print(row['A'], row['B'])

#TODO : Evaluate the print_lbl column. If not items contain True, set print_lbl to False.
    # Using itertuples() (faster)
    cust_order_summary = []
    for row in summary_df.itertuples():
        cust_order = {
            "customer": row.Customer,
            "Monday" : row.Monday,
            "Tuesday": row.Tuesday,
            "Wednesday": row.Wednesday,
            "Thursday": row.Thursday,
            "Friday": row.Friday,
            "print_lbl" : "True"
        }
        cust_order_summary.append(cust_order)

#This was in the HTML
#     { %
#     for i in range(1, 6) %}
#     { % if cust[i].num_items == '0' %}
#     < td > - < / td >
#
#
# { % else %}
# < td > {{cust[i].num_items}} < / td >
# { % endif %}
# { % if cust[i].order_qty == '0' %}
# < td > - < / td >
# { % else %}
# < td > {{cust[i].order_qty}} < / td >
# { % endif %}
# < td >$10.00 < / td >
# { % endfor %}
#


    return(cust_order_summary)

def get_all_cust_order_sched():
    cust_schedule = df_all_cust_orders.sort_values(['Customer', 'Item'])
    cust_schedule = cust_schedule.to_dict(orient='records')
    return cust_schedule

def get_cust_order_sched(customer):
    # for custs in cust_schedule:
    #     if not cust_order_summary:
    #         cust_order = {
    #             "customer": custs['cust_name'],
    # TODO: Note how custs['day'] (e.g. Mon, Tues, etc) becomes a dictionary to the num_items and order_qty
    #             custs['day']: {
    #                 'num_items': '1',
    #                 'order_qty': custs['order_qty']
    #             }
    #         }
    #         # cust_order = { "customer": custs['location'],'num_items':'1', 'order_qty':custs['order_qty']}
    #         cust_order_summary.append(cust_order)

    # print (f"df_cust_orders: {df_all_cust_orders}")
    df_cust_orders = df_all_cust_orders[df_all_cust_orders['Customer'] == customer]
    print (f"df_cust_orders: {df_cust_orders}")
    cust_orders = df_cust_orders.to_dict(orient='records')
    # cust_orders = df_cust_orders.to_dict()
    return(cust_orders)

