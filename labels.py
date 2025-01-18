from docx import Document
from docx.shared import Pt
# from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.style import WD_STYLE_TYPE
from cust_orders import get_all_cust_order_sched
import csv
import pandas as pd
from docx.shared import Cm, Inches

#TODO:
    # Enter items and ingredients into a CSV file
    # Read the file
    # Create a CSV file that contains the day, locations and order quantity of each item to print on a label
    # Create an HTML table that contains all the items and is formatted to print on the Avery label stock
    # Fix the Blueberry label misspellings

# item_list = [
#     {"item" : "Almond Croissants", "ingredients" : "Wheat Flour, Water, Butter (Cream), Sugar, Almonds, Yeast, Egg Whites, Invert Sugar Syrup, Egg, Salt, Wheat Gluten, Egg Yolks, Ascorbic Acid, Enzyme. Topping: Powdered Sugar. Contains Milk, Egg, Tree Nuts"},
#     {"item": "Apple Turnovers", "ingredients" : "Apple Filling (Water, Sugar, Glucose, Evaporated Apples, Modified Corn Starch, Spice, Citric Acid, Sodium Benzoate and Potassium Sorbate (preservatives), Enriched Flour (Wheat Flour, Niacin, Iron, Thiamin Mononitrate, Riboflavin, Folic Acid, Water, Palm Oil, Sugar, Soybean Oil, Salt, Monocalcium Phosphate)"},
#     {"item": "Blueberry Muffins", "ingredients": "Bleached Wheat Flour, Sugar, Eggs, Soybean Oil, Blueberries, Water, Modified Food Starch, Leavening (Baking Soda, Sodium Aluminum Phosphate, Monocalcium Phosphate), Mono and Diglycerides, Natural Flavor, Buttermilk Solids, Salt, Enzyme, Xanthan Gum."},
#     {"item": "Chocolate Chip Muffins", "ingredients": "Need Ingredients"},
#     {"item": "Chocolate Chip Cookies", "ingredients": "Need Ingredients"},
#     {"item": "Blueberry Scones", "ingredients": "Need Ingredients"},
#     {"item": "Raspberry Scones","ingredients": "Need Ingredients"},
#     {"item": "Lemon Cheese Danish", "ingredients": "Need Ingredients"},
#     {"item": "Maple Danish", "ingredients": "Need Ingredients"},
#     {"item": "Spinach Feta", "ingredients": "Need Ingredients"},
#     {"item": "Cranberry-Orange Muffins", "ingredients": "Need Ingredients"},
#     {"item": "Chocolate Croissannts", "ingredients": "Need Ingredients"},
#     {"item": "Cutout Cookies", "ingredients": "Flour, Sugar, Eggs, Butter, Vanilla, Baking Powder"},
#     {"item": "Banana Bread", "ingredients": "Sugar, eggs, butter, baking soda, bananas, sour cream, salt, cream cheese, flour *Contains Dairy"},
#     {"item": "Pistachio Muffins", "ingredients": "Sugar, Bleached Wheat Flour, Eggs, Soybean Oil, Water, Walnuts, Modified Food Starch, Leavening (Baking soda, Sodium Aluminum Phosphate), Mono and Diglycerides, Natural and Artificial Flavor, Buttermilk Solids, Salt, Lactic Acid, Enzyme, Xanthan Gum, Artificial Color, F.D.&C Yellow #5. This product is manufactured on equipment exposed to almond, coconut, pecan, pistachio, soy and products. Contains Wheat, Egg, Dairy (Milk), Walnuts"},
# ]


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


products = [
            ['Clean', {'number': '42565', 'name': 'Cleanex', 'price': '01.00', 'description': 'to clean'},
                      {'number': '45217', 'name': 'Toothbrush', 'price': '01.50', 'description': 'oral hygiene'}],
            ['Kitchen', {'number': '47851', 'name': 'Spaguetti', 'price': '01.00', 'description': 'Easy to cook'},
             {'number': '5852', 'name': 'Rice', 'price': '1.00', 'description': 'For all family'}],
            ['House', {'number': '78595', 'name': 'Door', 'price': '25.00', 'description': 'A resistant door'}]]

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

order_quantities_by_location = [
    {"location": 'FL - MRB', "day": "Monday", "item": "Almond Croissants", "order_qty" : "2"},
    {"location": 'FL - MRB', "day": "Monday", "item": "Apple Turnovers", "order_qty": "2"},
    {"location": 'FL - MRB', "day": "Monday", "item": "Blueberry Muffins", "order_qty": "8"},
    {"location": 'FL - MRB', "day": "Monday", "item": "Chocolate Chip Muffins", "order_qty": "12"},
    {"location": 'FL - MRB', "day": "Monday", "item": "Blueberry Scones", "order_qty": "2"},
    {"location": 'FL - Main', "day": "Monday", "item": "Almond Croissants", "order_qty" : "3"},
    {"location": 'FL - Main', "day": "Monday", "item": "Apple Turnovers", "order_qty": "1"},
    {"location": 'FL - Main', "day": "Monday", "item": "Blueberry Muffins", "order_qty": "4"},
    {"location": 'FL - Main', "day": "Monday", "item": "lemon Cheese Danish", "order_qty": "2"},
    {"location": 'FL - Main', "day": "Monday", "item": "Spinach Feta", "order_qty": "6"},
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

df_all_items = pd.read_csv('data/item_ingredients.csv', index_col=False)


# class LabelSummary:
#     def __init__(self, item, day, location, quantity):
#         self.item = item
#         self.day = day
#         self.location = location
#         self.quantity = quantity
#         self.print = "True"
#
#     class get_items:
#     def __init__(self):
#
#         cust_days = order_quantities_by_location
#         day_list = []
#
#         for cust_day in cust_days:
#             if not day_list:
#                 self.item[]= LabelSummary(day = cust_day['day'], location = cust_day['location'], quantity=cust_day['order_qty'], item=cust_day['item'])
#                 lbl_dict = {'day': cust_day['day'], 'location': cust_day['location'], 'item_qty': '1',
#                                  'lbl_qty': cust_day['order_qty'], 'on': 'True'}
#                 day_list.append(lbl_dict)
#             else:
#                 if not any(d['day'] == cust_day['day'] and d['location'] == cust_day['location'] for d in day_list):
#                     label_summary = {'day': cust_day['day'], 'location': cust_day['location'], 'item_qty': '0',
#                                      'lbl_qty': '0', 'on': 'True'}
#                     day_list.append(label_summary)
#                 for d in day_list:
#                     # print (f"d['day']:{d['day']}, cust_day:{cust_day['day']}, d-location:{d['location']}, cust_loc: {cust_day['location']}")
#                     if d['day'] == cust_day['day'] and d['location'] == cust_day['location']:
#                         # print(f"{count}. Found record: d['day']:{d['day']}, cust_day:{cust_day['day']}, d-location:{d['location']}, cust_loc: {cust_day['location']}")
#                         lbl_qty = int(d['lbl_qty']) + int(cust_day['order_qty'])
#                         item_qty = int(d['item_qty']) + 1
#                         d['item_qty'] = str(item_qty)
#                         d['lbl_qty'] = str(lbl_qty)
#             count += 1
#         # print(day_list)
#
#         return (day_list)


def get_item_ingredients():
    df_all_items = pd.read_csv('data/item_ingredients.csv', index_col=False)

    item_list = []
    with open("ingredient_data.csv") as item_file:
        # item_data = item_file.readlines()
        item_data = csv.reader(item_file)
        for row in item_data:
            print (f"Row: {row}")
            # item_list =

a = [
    {'main_color': 'red', 'second_color':'blue'},
    {'main_color': 'yellow', 'second_color':'green'},
    {'main_color': 'yellow', 'second_color':'blue'},
]
def in_dictlist(_keys: str, _values: str,  _dict_list = None):
    if _dict_list is None:
        # Initialize a new empty list
        # Because Input is None
        # And set the key value pair
        _dict_list = [{_key: _value}]
        return _dict_list

    # Check for keys in list
    for entry in _dict_list:
        # check if key with value exists
        if _key in entry and entry[_key] == _value:
            # if the pair exits continue
            continue
        else:
            # if not exists add the pair
            entry[_key] = _value
    return _dict_list


def get_label_summary():
    cust_days = order_quantities_by_location

    # Build the summary list of days, locations and total labels

    day_list = []
    # label_summary = {}
    count = 1

    for cust_day in cust_days :
        if not day_list:
            lbl_form_name = f"{cust_day['day']},{cust_day['location']}"
            print (lbl_form_name)
            label_summary = {'day': cust_day['day'], 'location': cust_day['location'], 'item_qty': '1', 'lbl_qty': cust_day['order_qty'], 'on':'True','lbl_form_name':lbl_form_name}
            day_list.append(label_summary)
            print (f"{count}. Starting: {day_list}")
        else:
            if not any(d['day'] == cust_day['day'] and d['location'] == cust_day['location'] for d in day_list):
                lbl_form_name = f"{cust_day['day']},{cust_day['location']}"
                print(lbl_form_name)
                label_summary = {'day': cust_day['day'], 'location': cust_day['location'], 'item_qty': '0', 'lbl_qty': '0', 'on':'True','lbl_form_name':lbl_form_name}
                day_list.append(label_summary)
            for d in day_list:
                # print (f"d['day']:{d['day']}, cust_day:{cust_day['day']}, d-location:{d['location']}, cust_loc: {cust_day['location']}")
                if d['day'] == cust_day['day'] and d['location'] == cust_day['location']:
                    # print(f"{count}. Found record: d['day']:{d['day']}, cust_day:{cust_day['day']}, d-location:{d['location']}, cust_loc: {cust_day['location']}")
                    lbl_qty = int(d['lbl_qty']) + int(cust_day['order_qty'])
                    item_qty = int(d['item_qty']) + 1
                    d['item_qty'] = str(item_qty)
                    d['lbl_qty'] = str(lbl_qty)

        count += 1
    # print(day_list)

    return (day_list)

def get_packaging_labels(lbl_summary):
    item_list = df_all_items.to_dict(orient='records')
    pkg_labels = []
    orders = get_all_cust_order_sched()
    # print (f"everything: {orders}")
    for lbls in lbl_summary:
        for items_ordered in orders:
            if lbls['customer'] == items_ordered['Customer'] and items_ordered['print_lbl'] == True:
                print(f"creating label: {items_ordered['Customer']}/{items_ordered['Item']}")
                lbl_data = {'item': items_ordered['Customer'], 'ingredients': items_ordered['Item']}
                pkg_labels.append(lbl_data)
    return (pkg_labels)


def get_lbl_ingreds(lbl_summary):
    item_list = df_all_items.to_dict(orient='records')
    print (f"the item list: {item_list}")

    labels = []
    orders = get_all_cust_order_sched()
    # print (f"everything: {orders}")
    for lbls in lbl_summary :
        if lbls['print_lbl'] == 'True':
            for items_ordered in orders:
                print (f"items_ordered: {items_ordered}")
                # if lbls['day'] == items_ordered['day']  and lbls['location'] == items_ordered['location']:
                # available: customer, Monday, Tuesday..., Friday, print_lbl
                if lbls['customer'] == items_ordered['Customer'] and items_ordered['print_lbl']==True:
                    print(f"creating label: {items_ordered['Customer']}/{items_ordered['Item']}")
                    # TODO need a loop to only include days that the user wants to print. This will print all labels for the week
                    total_qty = int(items_ordered['Monday']) + int(items_ordered['Tuesday']) + int(items_ordered['Wednesday']) + int(items_ordered['Thursday']) + int(items_ordered['Friday'])
                    # x = range(int(items_ordered['order_qty']))
                    print(f"total_qty {total_qty}")
                    x = range(total_qty)
# TODO add if items in item_list to print error message on the label if item isn't found (which shouldn't happen)
                    for items in item_list:
                        if items_ordered['Item'] == items['item']:
                            # Create a label with the customer name and item name by fudging the dictionary entry
                            #TODO add a parameter to allow inline printing or not
                            lbl_data = {'item': items_ordered['Customer'], 'ingredients' : items_ordered['Item']}
                            labels.append(lbl_data)
                            print ("found an item")
                            for n in x:
                                lbl_data = {'item': items_ordered['Item'], 'ingredients': items['ingredients'] }
                                labels.append(lbl_data)

    # print(labels)
    return(labels)
    # for item in items:
    #     # row = [item["column1"], item["column2"], item["column3"]]
    #     row = [item["item"], item["item"], item["item"]]
    #     rows.append(row)
    #
    # print(rows)

# < td > < img src = "../static/assets/img/LOGO.jpg" > < / td >
#TODO Move this to a .py file for only items/ingredients
def get_item_ingreds():
    print(f"df_all_items: {df_all_items}")
    item_list = df_all_items.to_dict(orient='records')
    # print (f"DF_ALL_ITEMS Dict = {all_items_2} ")

    all_items = []
    for items in item_list:
        item_data = {'item': items['item'], 'ingredients': items['ingredients']}
        all_items.append(item_data)

    return(all_items)



#TODO: move these function to a file/class specific to customer orders
# def get_cust_order_summary():
#     cust_schedule = order_quantities_by_location
#     cust_summary = customer_order_summary_2
#
#     cust_order_summary = []
#     for custs in cust_schedule:
#         if not cust_order_summary:
#             cust_order = {
#                 "customer": custs['location'],
#                 custs['day'] : {
#                     'num_items': '1',
#                     'order_qty': custs['order_qty']
#                 }
#             }
#             # cust_order = { "customer": custs['location'],'num_items':'1', 'order_qty':custs['order_qty']}
#             cust_order_summary.append(cust_order)
#             print(f"cust_order_summary: {cust_order_summary}")
#         else:
#             # for c in cust_order_summary:
#             if not any(c['customer'] == custs['location'] for c in cust_order_summary):
#                 cust_order = {
#                     "customer": custs['location'],
#                     custs['day']: {
#                         'num_items': '1',
#                         'order_qty': custs['order_qty']
#                     }
#                 }
#                 # cust_order = {"customer": custs['location'], 'num_items': '1', 'order_qty': custs['order_qty']}
#                 cust_order_summary.append(cust_order)
#                 print(f"cust_order_summary: {cust_order_summary}")
#             else:
#                 for cust_name in cust_order_summary:
#                     add_item = False
#                     # if cust_name['customer'] == custs['location']:
#                     for x, obj in cust_name.items():
#                         # print(f" X = {x}, {cust_name}, num_items: {obj}")
#                         if x != 'customer':
#                             if x == custs['day']:
#                                 for y in obj:
#                                     pass
#                                     # print(f"y={y}, {obj[y]}")
#                                 #     num_items = int(obj[y])
#                         else:
#                             add_item = True
#                     if add_item == True:
#                         cust_name[custs['day']] = {
#                             'num_items': '1',
#                             'order_qty': custs['order_qty']
#                         }
#
#     print (f"cust_order_summary: {cust_order_summary}")
#     return(cust_summary)


def get_cust_order_sched():
    cust_schedule = order_quantities_by_location
    return cust_schedule

def get_labels():
    get_item_ingredients()

    # Orignal Word Doc code starts here
    doc_name = "Avery Template 5136 WIP.docx"
    document = Document(doc_name)

    with open ('LOGO.jpg', 'rb') as f:
        logo = f.read()

    rows = []
    items = item_list

    for item in items:
        # row = [item["column1"], item["column2"], item["column3"]]
        row = [item["item"], item["item"], item["item"]]
        rows.append(row)

    print(rows)

    # table = document.add_table(
    #     rows=4, cols=3
    # )  # Create a new table with the correct number of rows and columns

       # table_count = len(document.tables)
    # print (f"num tables = {table_count}")
    # table = document.tables
    # table = document.tables(1)

    for table in document.tables:
        # font_styles = document.styles
        # font_charstyle = font_styles.add_style('IngredientStyle', WD_STYLE_TYPE.CHARACTER)
        # font_object = font_charstyle.font
        # font_object.size = Pt(8\2qs
        # font_object.name = 'Calibri'

        # table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # table.cell(0, 0).text = "Column 1"  # Add the column headers to the first row
        # table.cell(0, 2).text = "Column 2"
        # table.cell(0, 4).text = "Column 3"

        i = 0
        column_idx = 0
        for item in items:
            # row = [item["column1"], item["column2"], item["column3"]]
            # row = [item["item"], item["item"], item["item"]]
            # rows.append(row)

            # width = Inches(4.0), height = Inches(.7)
            # table.cell(i + 1, 0).text = ""  # Add the row data to the table
            p = table.cell(i + 1, 0).add_paragraph()
            # p2 = table.cell(i+1, 0).add_paragraph()
            r = p.add_run()
            cell_text = item["item"] + "\n" + item["ingredients"]

            item_qty = int(item["item_qty"])
            x = range(item_qty)
            print(f"x={x}, item_qty={item_qty}")
            for qty in x:
                # 1 = 0, 2 = 2, 3 = 4,
                # 4 = 0, 5 = 2, 6 = 4,
                # 7 = 0, 8 = 2, 9 = 4

                # table.cell(i + 1, 0).text = item["item"]
                # table.cell(i + 1, 0).paragraphs[0].runs[0].add_picture(logo)
                table.cell(i, column_idx).text = cell_text
                table.cell(i, column_idx).paragraphs[0].runs[0].font.size = Pt(6)  # Add the row data to the table
                table.cell(i, column_idx).vertical_alignment = WD_ALIGN_VERTICAL.CENTER  # Add the row data to the table
                # table.cell(i + 1, column_idx).paragraphs[0].runs[0].text.center()
                column_idx += 2
                if column_idx > 4:
                    column_idx = 0
                    i += 1
                    print(f"row:{i}")
                # if not qty % 3 and qty != 0:
                #     i += 1
                #     column_idx = 0

            # # table.cell(i + 1, 0).text = item["item"]
            # # table.cell(i + 1, 0).paragraphs[0].runs[0].add_picture(logo)
            # table.cell(i + 1, 0).text = cell_text
            # table.cell(i + 1, 0).paragraphs[0].runs[0].font.size = Pt(6)  # Add the row data to the table
            # table.cell(i + 1, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER  # Add the row data to the table
            # table.cell(i + 1, 0).paragraphs[0].runs[0].text.center()
            # table.cell(i + 1, 2).text = cell_text
            # # table.cell(i + 1, 2).text = item["item"]
            # table.cell(i + 1, 2).paragraphs[0].runs[0].font.size = Pt(6)  # Add the row data to the table
            # # table.cell(i + 1, 4).text = row[2]
            # table.cell(i + 1, 4).text = cell_text
            # table.cell(i + 1, 4).paragraphs[0].runs[0].font.size = Pt(6)  # Add the row data to the table
            # i += 1


#         for i, row in enumerate(rows):
#             # width = Inches(4.0), height = Inches(.7)
#             # table.cell(i + 1, 0).text = ""  # Add the row data to the table
#             p = table.cell(i+1, 0).add_paragraph()
#             # p2 = table.cell(i+1, 0).add_paragraph()
#             r = p.add_run()
#             # r.add_picture('LOGO.jpg', width=Inches(1.0), height=Inches(.7))
#             # for item in items:
#             #     # row = [item["column1"], item["column2"], item["column3"]]
#             #     row = [item["item"], item["item"], item["item"]]
#             #     rows.append(row)
# #tHIS NEXT LINE WORKS, TRYING SOMETHING BELOW
#             # r.add_text("ABC")
#             # p2.text = "ABC"
#             # r.text = row[0]
#             # r.font.size = Pt(6)
#             # p.alignment = WD_ALIGN_PARAGRAPH.CENTER
#
#             # r.add_text(row[0])
#             # table.cell(i + 1, 0) = row[0]  # Add the row data to the table
#             # table.cell(i + 1, 0).text = row[0]  # Add the row data to the table
#             # table.cell(i + 2, 0).paragraphs[0].runs[0].add_picture('LOGO.jpg', width=Inches(1.0), height=Inches(.7))  # Add the row data to the table
#             # table.cell(i + 1, 0).paragraphs[0].runs[0].font.size = Pt(6)  # Add the row data to the table
#             # table.cell(i + 1, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER   # Add the row data to the table
#             pauls_text = "DEF"
#             table.cell(i + 1, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER   # Add the row data to the table
#             # table.cell(i + 1, 2).text = "def" #row[1]
#             # table.cell(i + 1, 2).text = "ABC" + pauls_text
#
#             table.cell(i + 1, 2).text = "ABC" + pauls_text
#             table.cell(i + 1,
    #
    #             4).text = row[2]
#             table.cell(i + 1, 4).paragraphs[0].runs[0].font.size = Pt(6)  # Add the row data to the table

    # parag.add_run("Python", style='CommentsStyle').italic = True


    document.save(doc_name)
    return (items)

    # ORIGINAL CODE ENDS HERE


    # print ("make_table")
    # make_table("demo.docx")  # create document with tri0cks table
    # print ("template.docx")
    # doc = DocxTemplate("template.docx")  # do docxtpl template for main document
    # print ("demo.docx")
    # sd = doc.new_subdoc("demo.docx")  # do subdocument
    # # place the table in the word main document at a specific placeholder location.
    # context = {
    #     "mysubdoc": sd,
    # }
    #
    # doc.render(context)
    #
    # print ("doc.save output.docx")
    # doc.save("output.docx")

