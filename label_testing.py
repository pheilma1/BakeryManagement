from pylabels import Label, Page

label = Label('5136', default_fontSize=12)

# Add text to the label
label.add_text('Hello, World!', 10, 10)

# Create a page with 30 labels (3 columns, 10 rows)
page = Page('5136', 3, 10)

# Add the label to the page
page.add_label(label)

# Generate the PDF
page.save('my_labels.pdf')
page.save('my_labels.html')
