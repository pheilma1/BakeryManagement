from docx import Document
from docx.shared import Pt
# from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.style import WD_STYLE_TYPE

import csv
from docx.shared import Cm, Inches

# from docx import Document

#
# from docxtpl import DocxTemplate
#
#

def get_item_ingredients():
    item_list = []
    with open("ingredient_data.csv") as item_file:
        # item_data = item_file.readlines()
        item_data = csv.reader(item_file)
        for row in item_data:
            print (row)
            # item_list =

def make_table(name):
    """Make table document."""
    sd = Document()


get_item_ingredients()


#Orignal Word Doc code starts here
doc_name = "Avery Template 5136 WIP.docx"
document = Document(doc_name)

# TODO Set the FONT for the text in the table
# font_styles = document.styles
# font_charstyle = font_styles.add_style('IngredientStyle',  WD_STYLE_TYPE.CHARACTER)
# font_object = font_charstyle.font
# font_object.size = Pt(8)
# font_object.name = 'Calibri'

#
# parag.add_run("this word document, was created using Times New Roman", style='CommentsStyle').bold = True
# parag.add_run("Python", style='CommentsStyle').italic = True
# doc.save("test.docx")

with open ('LOGO.jpg', 'rb') as f:
    logo = f.read()


items = [
    {"column1": "Almond Croissant\nWheat Flour, Water, Butter (Cream), Sugar, Almonds, Yeast, Egg Whites, Invert Sugar Syrup, Egg, Salt, Wheat Gluten, Egg Yolks, Ascorbic Acid, Enzyme. Topping: Powdered Sugar. Contains Milk, Egg, Tree Nuts\nWe are not a nut-free facility\n16 W Main St. Shortsville NY 14548", "column2": "Almond Croissant\nWheat Flour, Water, Butter (Cream), Sugar, Almonds, Yeast, Egg Whites, Invert Sugar Syrup, Egg, Salt, Wheat Gluten, Egg Yolks, Ascorbic Acid, Enzyme. Topping: Powdered Sugar. Contains Milk, Egg, Tree Nuts\nWe are not a nut-free facility\n16 W Main St. Shortsville NY 14548", "column3": "Almond Croissant\nWheat Flour, Water, Butter (Cream), Sugar, Almonds, Yeast, Egg Whites, Invert Sugar Syrup, Egg, Salt, Wheat Gluten, Egg Yolks, Ascorbic Acid, Enzyme. Topping: Powdered Sugar. Contains Milk, Egg, Tree Nuts\nWe are not a nut-free facility\n16 W Main St. Shortsville NY 14548"},
    {"column1": "Almond Croissant", "column2": "Item 1-2", "column3": "Almond Croissant\nWheat Flour, Water, Butter (Cream), Sugar, Almonds, Yeast, Egg Whites, Invert Sugar Syrup, Egg, Salt, Wheat Gluten, Egg Yolks, Ascorbic Acid, Enzyme. Topping: Powdered Sugar. Contains Milk, Egg, Tree Nuts\nWe are not a nut-free facility\n16 W Main St. Shortsville NY 14548"},
    {"column1": "Almond Croissant", "column2": "Almond Croissant\nWheat Flour, Water, Butter (Cream), Sugar, Almonds, Yeast, Egg Whites, Invert Sugar Syrup, Egg, Salt, Wheat Gluten, Egg Yolks, Ascorbic Acid, Enzyme. Topping: Powdered Sugar. Contains Milk, Egg, Tree Nuts\nWe are not a nut-free facility\n16 W Main St. Shortsville NY 14548", "column3": "Item 1-3"},
    # {"column1": "Item 2-1", "column2": "Item 2-2", "column3": "Item 2-3"},
    # {"column1": "Item 3-1", "column2": "Item 3-2", "column3": "Item 3-3"},
]
# Almond Croissant
# Wheat Flour, Water, Butter (Cream), Sugar, Almonds, Yeast, Egg
# Whites, Invert Sugar Syrup, Egg, Salt, Wheat Gluten, Egg
# Yolks, Ascorbic Acid, Enzyme. Topping: Powdered Sugar.
# Contains Milk, Egg, Tree Nuts
# We are not a nut-free facility
# 16 W Main St. Shortsville NY 14548
rows = []
for item in items:
    # row = [item["column1"], item["column2"], item["column3"]]
    row = [item["column1"], item["column2"], item["column3"]]
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

    table.cell(0, 0).text = "Column 1"  # Add the column headers to the first row
    table.cell(0, 2).text = "Column 2"
    table.cell(0, 4).text = "Column 3"
    for i, row in enumerate(rows):
        # width = Inches(4.0), height = Inches(.7)
        # table.cell(i + 1, 0).text = ""  # Add the row data to the table
        p = table.cell(i+1, 0).add_paragraph()
        # p2 = table.cell(i+1, 0).add_paragraph()
        r = p.add_run()
        r.add_picture('LOGO.jpg', width=Inches(1.0), height=Inches(.7))
        r.add_text("ABC")
        # p2.text = "ABC"
        # r.text = row[0]
        # r.font.size = Pt(6)
        # p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # r.add_text(row[0])
        # table.cell(i + 1, 0) = row[0]  # Add the row data to the table
        # table.cell(i + 1, 0).text = row[0]  # Add the row data to the table
        # table.cell(i + 2, 0).paragraphs[0].runs[0].add_picture('LOGO.jpg', width=Inches(1.0), height=Inches(.7))  # Add the row data to the table
        # table.cell(i + 1, 0).paragraphs[0].runs[0].font.size = Pt(6)  # Add the row data to the table
        # table.cell(i + 1, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER   # Add the row data to the table
        pauls_text = "DEF"
        table.cell(i + 1, 0).vertical_alignment = WD_ALIGN_VERTICAL.CENTER   # Add the row data to the table
        # table.cell(i + 1, 2).text = "def" #row[1]
        table.cell(i + 1, 2).text = "ABC" + pauls_text
        table.cell(i + 1, 2).paragraphs[0].runs[0].font.size = Pt(6)  # Add the row data to the table
        table.cell(i + 1, 4).text = row[2]
        table.cell(i + 1, 4).paragraphs[0].runs[0].font.size = Pt(6)  # Add the row data to the table

# parag.add_run("Python", style='CommentsStyle').italic = True


document.save(doc_name)
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