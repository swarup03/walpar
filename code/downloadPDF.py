# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter


# # def generate_invoice_pdf(order_details, bill_details, ordered_products, pdf_filename):
#     # Use reportlab to generate the PDF
#     # You'll need to customize this part based on your specific invoice structure

#     # Create a PDF document
#     pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)

#     # Set font
#     pdf_canvas.setFont("Helvetica", 12)

#     # Add content to the PDF
#     pdf_canvas.drawString(100, 750, f"Invoice for Order #{order_details[0][0]}")
#     pdf_canvas.drawString(100, 730, f"Order Date: {order_details[0][1].strftime('%d-%m-%Y')}")
#     pdf_canvas.drawString(100, 710, f"Total Amount: ₹{order_details[0][2]}")

#     # Customer Details
#     pdf_canvas.drawString(100, 690, "Customer Details:")
#     pdf_canvas.drawString(120, 670, f"Name: {bill_details[0][1]}")
#     pdf_canvas.drawString(120, 650, f"Mobile Number: {bill_details[0][2]}")
#     pdf_canvas.drawString(120, 630, f"Email: {bill_details[0][3]}")

#     # Billing Address
#     pdf_canvas.drawString(100, 610, "Billing Address:")
#     pdf_canvas.drawString(120, 590, f"Street: {bill_details[0][5]}")
#     pdf_canvas.drawString(120, 570, f"City: {bill_details[0][6]}")
#     pdf_canvas.drawString(120, 550, f"State: {bill_details[0][7]}")
#     pdf_canvas.drawString(120, 530, f"Zip Code: {bill_details[0][8]}")

#     # Ordered Products Table
#     pdf_canvas.drawString(100, 500, "Ordered Products:")
#     col_widths = [30, 200, 70, 70, 70]
#     row_height = 20
#     col_positions = [100, 130, 330, 400, 470]

#     # Header
#     pdf_canvas.drawString(col_positions[0], 480, "ID")
#     pdf_canvas.drawString(col_positions[1], 480, "Product Name")
#     pdf_canvas.drawString(col_positions[2], 480, "Quantity")
#     pdf_canvas.drawString(col_positions[3], 480, "Price")
#     pdf_canvas.drawString(col_positions[4], 480, "Total")

#     # Table content
#     current_y = 460
#     for product in ordered_products:
#         pdf_canvas.drawString(col_positions[0], current_y, str(product[0]))
#         pdf_canvas.drawString(col_positions[1], current_y, str(product[1]))  # Assuming product name is at index 0 in the list
#         pdf_canvas.drawString(col_positions[2], current_y, str(product[2]))
#         pdf_canvas.drawString(col_positions[3], current_y, f"₹{product[3]}")
#         pdf_canvas.drawString(col_positions[4], current_y, f"₹{product[2] * product[3]}")

#         current_y -= row_height

#     # Save the PDF
#     pdf_canvas.save()
    
    
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_invoice_pdf(invoice_data, pdf_filename):
    # Use reportlab to generate the PDF based on HTML template
    # Create a PDF document
    pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)

    # Set font
    pdf_canvas.setFont("Helvetica", 12)

    # Add content to the PDF
    pdf_canvas.drawString(100, 750, f"Invoice for Order #{invoice_data['invoice_number']}")
    pdf_canvas.drawString(100, 730, f"Order Date: {invoice_data['order_date']}")
    pdf_canvas.drawString(100, 710, f"Total Amount: ${invoice_data['total_amount']}")

    # Customer Details
    pdf_canvas.drawString(100, 690, "Customer Details:")
    pdf_canvas.drawString(120, 670, f"Name: {invoice_data['customer_name']}")
    pdf_canvas.drawString(120, 650, f"Mobile Number: {invoice_data['customer_mobile']}")
    pdf_canvas.drawString(120, 630, f"Email: {invoice_data['customer_email']}")

    # Billing Address
    pdf_canvas.drawString(100, 610, "Billing Address:")
    pdf_canvas.drawString(120, 590, f"Street: {invoice_data['billing_street']}")
    pdf_canvas.drawString(120, 570, f"City: {invoice_data['billing_city']}")
    pdf_canvas.drawString(120, 550, f"State: {invoice_data['billing_state']}")
    pdf_canvas.drawString(120, 530, f"Zip Code: {invoice_data['billing_zip']}")

    # Ordered Products Table
    pdf_canvas.drawString(100, 500, "Ordered Products:")
    col_widths = [30, 200, 70, 70, 70]
    row_height = 20
    col_positions = [100, 130, 330, 400, 470]

    # Header
    pdf_canvas.drawString(col_positions[0], 480, "ID")
    pdf_canvas.drawString(col_positions[1], 480, "Product Name")
    pdf_canvas.drawString(col_positions[2], 480, "Quantity")
    pdf_canvas.drawString(col_positions[3], 480, "Price")
    pdf_canvas.drawString(col_positions[4], 480, "Total")

    # Table content
    current_y = 460
    for product in invoice_data['ordered_products']:
        pdf_canvas.drawString(col_positions[0], current_y, str(product['id']))
        pdf_canvas.drawString(col_positions[1], current_y, str(product['name']))
        pdf_canvas.drawString(col_positions[2], current_y, str(product['quantity']))
        pdf_canvas.drawString(col_positions[3], current_y, f"${product['price']}")
        pdf_canvas.drawString(col_positions[4], current_y, f"${product['total']}")

        current_y -= row_height

    # Save the PDF
    pdf_canvas.save()
