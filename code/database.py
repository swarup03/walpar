import mysql.connector
import bcrypt #used to hash the password
from datetime import datetime, timedelta

conn = mysql.connector.connect(host='localhost',
                               database='walpar_nutritions',
                               user='root',
                               password='1234')
cursorObject = conn.cursor()

def fetch_image_name(product_id):
    query = "SELECT image_name FROM images WHERE product_id='" + str(product_id) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    file_names = [result[0] for result in results]
    return file_names

def fatch_category_name():
    query = "select brand_id,name from categories;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def signup_user(fname,lname,email,passw,address1,city,state,zip,sex):
    query = "SELECT * FROM users WHERE email ='"+str(email)+"';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    if not results:
        # Prepare the SQL query
        # Hash the password
        hashed_password = bcrypt.hashpw(passw.encode(), bcrypt.gensalt()).decode()
        query ="INSERT INTO users (first_name, last_name, email, password,sex) VALUES (%s, %s, %s, %s, %s);"
        values = (fname,lname,email,hashed_password,sex)
        cursorObject.execute(query, values)
        conn.commit()
        query ="SELECT LAST_INSERT_ID() AS LastID;"
        cursorObject.execute(query)
        results = cursorObject.fetchall()
        query = "INSERT INTO `addresses` (`user_id`, `street_address`, `city`,`state`,`zip_code`)VALUES(%s,%s,%s,%s,%s);"
        values = (results[0][0], address1, city, state, zip)
        cursorObject.execute(query, values)
        conn.commit()
        return "success"
    else:
        return "You have already created account using this Email :("+email+") "

def login_user(email, password):
    query = "SELECT email,password FROM users WHERE email ='" + str(email) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    if len(results) == 1:
        if bcrypt.checkpw(password.encode(), results[0][1].encode()):
            return "success"
        else:
            return "Please enter valid Password."
    else:
        return "Please enter valid Email id."

def fatch_profile_details(email):
    query = "SELECT user_id,first_name,last_name,email FROM users WHERE email ='" + str(email) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    query = "SELECT address_id,street_address,city,state,zip_code FROM addresses WHERE user_id ='" + str(results[0][0]) + "';"
    cursorObject.execute(query)
    results1 = cursorObject.fetchall()
    return results[0],results1

def fatch_best_seller():
    query = "SELECT name, price, product_id, brand_id FROM products LIMIT 6;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()

    # Create a new list of tuples with the additional file_names
    results_with_file_names = []
    for result in results:
        product_id = result[2]
        files_in_folder = fetch_image_name(product_id)
        # Create a new tuple with the additional file_names
        result_with_files = result + (files_in_folder,)

        # Add the new tuple to the list
        results_with_file_names.append(result_with_files)

    return results_with_file_names



def fatch_category_product(brand_id):
    query = "SELECT name,price,product_id,brand_id FROM products WHERE brand_id='" + str(brand_id) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    # Create a new list of tuples with the additional file_names
    results_with_file_names = []
    for result in results:
        product_id = result[2]
        files_in_folder = fetch_image_name(product_id)
        # Create a new tuple with the additional file_names
        result_with_files = result + (files_in_folder,)
        # Add the new tuple to the list
        results_with_file_names.append(result_with_files)
    return results_with_file_names

def fatch_category_details(brand_id):
    query = "SELECT * FROM categories WHERE brand_id='" + str(brand_id) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def get_product_detail(product_id):
    query = "SELECT name, description, price FROM products WHERE product_id ='" + str(product_id) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def add_product_to_likes(user_email,product_id):
    # Get user ID from the provided email
    query_user_id = "SELECT user_id FROM users WHERE email = %s;"
    cursorObject.execute(query_user_id, (user_email,))
    user_id = cursorObject.fetchone()
    # Check if the product is already in the user's cart
    query_check_cart = "SELECT * FROM likes WHERE user_id = %s AND product_id = %s;"
    cursorObject.execute(query_check_cart, (user_id[0], product_id,))
    existing_cart_entry = cursorObject.fetchone()
    if existing_cart_entry:
        return "error"
    # If the product is not in the cart, insert it
    query_insert_into_cart = "INSERT INTO likes (user_id, product_id) VALUES (%s, %s);"
    values = (user_id[0], product_id)
    cursorObject.execute(query_insert_into_cart, values)
    conn.commit()
    return "success"


def insert_into_cart(user_email, product_id, quantity):
    # Get user ID from the provided email
    query_user_id = "SELECT user_id FROM users WHERE email = %s;"
    cursorObject.execute(query_user_id, (user_email,))
    user_id = cursorObject.fetchone()
    # Check if the product is already in the user's cart
    query_check_cart = "SELECT * FROM carts WHERE user_id = %s AND product_id = %s;"
    cursorObject.execute(query_check_cart, (user_id[0], product_id,))
    existing_cart_entry = cursorObject.fetchone()
    if existing_cart_entry:
        # Product is already in the cart, return an error
        return "error"
    # If the product is not in the cart, insert it
    query_insert_into_cart = "INSERT INTO carts (user_id, product_id, quantity) VALUES (%s, %s, %s);"
    values = (user_id[0], product_id, quantity)
    cursorObject.execute(query_insert_into_cart, values)
    conn.commit()

    return "success"

def fatch_user_liked_product(user_email):
    query_user_id = "SELECT user_id FROM users WHERE email = %s;"
    cursorObject.execute(query_user_id, (user_email,))
    user_id = cursorObject.fetchone()

    query = "SELECT likes.like_id,products.product_id, products.name, products.description, products.price, products.brand_id FROM likes JOIN products ON likes.product_id = products.product_id WHERE likes.user_id = %s;"
    cursorObject.execute(query, (user_id[0],))
    results = cursorObject.fetchall()

    # Create a new list of tuples with the additional file_names
    results_with_file_names = []
    for result in results:
        product_id = result[1]
        files_in_folder = fetch_image_name(product_id)
        # Create a new tuple with the additional file_names
        result_with_files = result + (files_in_folder,)

        # Add the new tuple to the list
        results_with_file_names.append(result_with_files)
    return results_with_file_names


def fatch_user_cart_products(user_email):
    query_user_id = "SELECT user_id FROM users WHERE email = %s;"
    cursorObject.execute(query_user_id, (user_email,))
    user_id = cursorObject.fetchone()

    query = "SELECT products.product_id, products.name, products.price, products.brand_id, carts.quantity, carts.cart_id FROM carts JOIN products ON carts.product_id = products.product_id WHERE carts.user_id = %s;"
    cursorObject.execute(query, (user_id[0],))
    results = cursorObject.fetchall()

    # Create a new list of tuples with the additional file_names
    results_with_file_names = []
    for result in results:
        product_id = result[0]
        files_in_folder = fetch_image_name(product_id)

        # Create a new tuple with the additional file_names
        result_with_files = result + (files_in_folder,)

        # Add the new tuple to the list
        results_with_file_names.append(result_with_files)
    return results_with_file_names

def fetch_checkout_cart_products(user_email):
    query_user_id = "SELECT user_id FROM users WHERE email = %s;"
    cursorObject.execute(query_user_id, (user_email,))
    user_id = cursorObject.fetchone()

    query = "SELECT  products.product_id,products.name, products.price, products.brand_id, carts.cart_id, carts.quantity FROM products JOIN carts ON products.product_id = carts.product_id where carts.user_id = %s;"
    cursorObject.execute(query, (user_id[0],))
    results = cursorObject.fetchall()

    # Create a new list of tuples with the additional file_names
    results_with_file_names = []
    for result in results:
        product_id = result[0]
        files_in_folder = fetch_image_name(product_id)

        # Create a new tuple with the additional file_names
        result_with_files = result + (files_in_folder,)

        # Add the new tuple to the list
        results_with_file_names.append(result_with_files)
    return results_with_file_names

def update_product_quantity_from_cart(cart_id,new_quantity):
    query_user_id = "UPDATE carts SET quantity = %s WHERE cart_id = %s;"
    cursorObject.execute(query_user_id, (new_quantity,cart_id,))
    conn.commit()
    return "success"

def delete_product_from_cart(cart_id):
    query_user_id = "DELETE FROM carts WHERE cart_id  = %s;"
    cursorObject.execute(query_user_id, (cart_id,))
    conn.commit()
    return "success"

def delete_product_from_like(like_id):
    query_user_id = "DELETE FROM likes WHERE like_id  = %s;"
    cursorObject.execute(query_user_id, (like_id,))
    conn.commit()
    return "success"

def search_result(search_content):
    query = "SELECT products.product_id, products.name, products.description, products.price, products.brand_id, categories.name FROM products JOIN categories ON products.brand_id = categories.brand_id WHERE products.name LIKE '%" + str(search_content) + "%' OR products.description LIKE '%" + str(search_content) + "%' OR categories.name LIKE '%" + str(search_content) + "%' OR categories.categorie_detail LIKE '%" + str(search_content) + "%' OR categories.about_categories LIKE '%" + str(search_content) + "%';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()

    # Create a new list of tuples with the additional file_names
    results_with_file_names = []
    for result in results:
        product_id = result[0]
        files_in_folder = fetch_image_name(product_id)
        # Create a new tuple with the additional file_names
        result_with_files = result + (files_in_folder,)

        # Add the new tuple to the list
        results_with_file_names.append(result_with_files)
    return results_with_file_names

def remove_address(address_id):
    query_user_id = "DELETE FROM addresses WHERE address_id = %s;"
    cursorObject.execute(query_user_id, (address_id,))
    conn.commit()
    return "success"

def update_address(address, city, state, zip,address_id):
    query_user_id = "UPDATE addresses SET street_address = %s, city = %s, state = %s, zip_code = %s WHERE address_id = %s;"
    cursorObject.execute(query_user_id, (address, city, state, zip,address_id,))
    conn.commit()
    return "success"

def insert_address(user_id, address, city, state, zip):
    query_insert_into_cart = "INSERT INTO addresses (user_id, street_address, city, state,zip_code) VALUES (%s, %s, %s, %s, %s);"
    values = (user_id, address, city, state, zip)
    cursorObject.execute(query_insert_into_cart, values)
    conn.commit()
    return "success"

def add_order(user_id, total_amount):
    query_insert_into_cart = "INSERT INTO orders (user_id, total_amount, delivery_date) VALUES (%s, %s, %s);"
    delivery_date = datetime.now().date() + timedelta(days=2)
    values = (user_id, total_amount,delivery_date)
    cursorObject.execute(query_insert_into_cart, values)
    conn.commit()
    query = "SELECT LAST_INSERT_ID() AS LastID;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results[0][0]

def totalAmountInCart(user_id):
    query = "select sum(price * quantity) from carts INNER JOIN products ON carts.product_id=products.product_id where user_id = %s ;"
    cursorObject.execute(query,(user_id,))
    results = cursorObject.fetchall()
    return results[0][0]

def add_bill(order_id, custom_name, custom_mobile_number, custom_email, billing_address_id):
    query ="INSERT INTO `walpar_nutritions`.`bill_details` (order_id, custom_name, custom_mobile_number, custom_email, billing_address_id) VALUES (%s, %s, %s, %s, %s);"
    values = (order_id, custom_name, custom_mobile_number, custom_email, billing_address_id)
    cursorObject.execute(query, values)
    conn.commit()
    return "success"

def add_product_to_order(user_id,order_id):
    query = "SELECT carts.product_id, carts.quantity, products.price FROM carts JOIN products ON carts.product_id = products.product_id where carts.user_id = %s;"
    cursorObject.execute(query, (user_id,))
    results = cursorObject.fetchall()
    for result in results:
        query = "INSERT INTO `walpar_nutritions`.`order_items` ( `order_id`, `product_id`, `quantity`, `price`) VALUES (%s, %s, %s, %s);"
        values = (order_id, result[0], result[1], result[2])
        cursorObject.execute(query, values)
        conn.commit()
    query_user_id = "DELETE FROM carts WHERE user_id = %s;"
    cursorObject.execute(query_user_id, (user_id,))
    conn.commit()
    return "success"

def fetch_order_history(user_id):
    query = "select orders.order_id, orders.order_date, orders.delivery_date,orders.total_amount, orders.status,sum(order_items.quantity) from orders join order_items ON orders.order_id=order_items.order_id where orders.user_id = %s group by order_items.order_id order by orders.order_date desc;"
    cursorObject.execute(query, (user_id,))
    results = cursorObject.fetchall()
    return results

def verify_user(order_id,user_email):
    query1="select user_id from walpar_nutritions.users where email = %s;"
    cursorObject.execute(query1, (user_email,))
    results1 = cursorObject.fetchall()
    query2 = "select user_id FROM `walpar_nutritions`.`orders` where order_id = %s;"
    cursorObject.execute(query2, (order_id,))
    results2 = cursorObject.fetchall()
    if results2 == results1:
        return "success"
    else:
        return "false"

def order_detail(order_id):
    query1 = "select order_id, order_date, total_amount, status, delivery_date from orders where order_id = %s;"
    cursorObject.execute(query1, (order_id,))
    results1 = cursorObject.fetchall()
    return results1

def bill_detail(order_id):
    query1 = "select bill_details.bill_detail_id, bill_details.custom_name, bill_details.custom_mobile_number, bill_details.custom_email, bill_details.billing_date,addresses.street_address,addresses.city,addresses.state,addresses.zip_code FROM bill_details join addresses on bill_details.billing_address_id = addresses.address_id where bill_details.order_id = %s;"
    cursorObject.execute(query1, (order_id,))
    results1 = cursorObject.fetchall()
    return results1
def ordered_product_list(order_id):
    query = "select order_items.order_item_id, order_items.product_id, order_items.quantity, order_items.price, products.name,products.brand_id from order_items join products on products.product_id = order_items.product_id where order_id = %s ;"
    cursorObject.execute(query, (order_id,))
    results = cursorObject.fetchall()
    # Create a new list of tuples with the additional file_names
    results_with_file_names = []
    for result in results:
        product_id = result[1]
        files_in_folder = fetch_image_name(product_id)
        # Create a new tuple with the additional file_names
        result_with_files = result + (files_in_folder,)
        # Add the new tuple to the list
        results_with_file_names.append(result_with_files)
    return results_with_file_names
