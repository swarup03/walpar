import mysql.connector
import bcrypt #used to hash the password
from datetime import datetime, timedelta
import os
from database import fetch_image_name

conn = mysql.connector.connect(host='localhost',
                               database='walpar_nutritions',
                               user='root',
                               password='1234')
cursorObject = conn.cursor()

def newOrder():
    query = "SELECT COUNT(*) FROM orders WHERE DATE(order_date) = CURDATE();"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results[0][0]

def orderPanding():
    query = "SELECT COUNT(*) FROM orders WHERE status = 'pending';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results[0][0]

def orderShipped():
    query = "SELECT COUNT(*) FROM orders WHERE status = 'shipped';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results[0][0]

def pandingAmount():
    query = "SELECT SUM(total_amount) FROM orders WHERE status IN ('shipped', 'pending');"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results[0][0]

def recentOrder():
    query ="SELECT orders.order_id, orders.order_date, orders.total_amount, orders.status,users.user_id, users.email, SUM(order_items.quantity) AS total_quantity FROM orders  JOIN users ON orders.user_id = users.user_id JOIN order_items ON orders.order_id = order_items.order_id GROUP BY orders.order_id, orders.order_date, orders.total_amount, orders.status, users.email ORDER BY order_date DESC LIMIT 5;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def recentUser():
    query ="SELECT user_id,first_name, last_name, email, sex FROM users ORDER BY user_id DESC limit 5;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def fatch_best_seller():
    query = "SELECT name, price, product_id,description, brand_id FROM products LIMIT 6;"
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

def add_admin(name,uname,password):
    query = "SELECT * FROM admin WHERE user_name ='"+str(uname)+"';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    if not results:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        query_insert_into_cart = "INSERT INTO admin (admin_name, user_name, password) VALUES (%s, %s, %s);"
        values = (name,uname,hashed_password)
        cursorObject.execute(query_insert_into_cart, values)
        conn.commit()
        return "success"
    else:
        return "User name is alrody in use :("+uname+") "

def login_user(uname,password):
    query = "SELECT user_name,password FROM admin WHERE user_name ='" + str(uname) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    if len(results) == 1:
        if bcrypt.checkpw(password.encode(), results[0][1].encode()):
            return "success"
        else:
            return "Please enter valid Password."
    else:
        return "Please enter valid Email id."

def adminDetail(uname):
    query = "SELECT admin_id,admin_name,user_name FROM admin WHERE user_name ='" + str(uname) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def fetch_all_users():
    query = "SELECT u.user_id, u.first_name, u.last_name, u.email, u.sex, a.street_address, a.city, (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.user_id) AS order_count, (SELECT COUNT(*) FROM likes l WHERE l.user_id = u.user_id) AS like_count FROM users u JOIN addresses a ON u.user_id = a.user_id WHERE a.address_id = ( SELECT MIN(address_id) FROM addresses WHERE user_id = u.user_id ) ORDER BY u.user_id  DESC LIMIT 12;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def user_profile_details(user_id):
    query = "SELECT u.user_id,u.first_name, u.last_name, u.email, u.sex, (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.user_id) AS order_count, (SELECT COUNT(*) FROM likes l WHERE l.user_id = u.user_id) AS like_count  FROM users u WHERE u.user_id = " + str(user_id) + ";"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results


def user_address_details(user_id):
    query = "SELECT address_id, street_address, city, state, zip_code FROM walpar_nutritions.addresses where user_id = " + str(user_id) + ";"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def user_address_delete(address_id):
    query = "DELETE FROM walpar_nutritions.addresses where address_id = " + str(address_id) + ";"
    cursorObject.execute(query)
    conn.commit()
    return "success"

def fetch_orders_list(user_id):
    query = "SELECT order_id,order_date, total_amount, status, delivery_date FROM walpar_nutritions.orders where user_id = " + str(user_id) + " ORDER BY order_date DESC;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def fetch_user(email):
    query = "SELECT user_id FROM walpar_nutritions.users where email = '" + str(email) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    if len(results) != 0:
            return results[0][0]
    else:
        return "User doesn't exists."

def remove_user(user_id):
    query_user_id = "DELETE FROM users WHERE user_id  = %s;"
    cursorObject.execute(query_user_id, (user_id,))
    conn.commit()
    return "success"

def product_category():
    query = "SELECT brand_id,name FROM walpar_nutritions.categories;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def add_category(name,category_detal,about_category):
    query_insert_into_cart = "INSERT INTO categories (name, categorie_detail, about_categories) VALUES (%s, %s, %s);"
    values = (name,category_detal,about_category)
    cursorObject.execute(query_insert_into_cart, values)
    conn.commit()
    query = "SELECT LAST_INSERT_ID() AS LastID;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    path = "C:\\Users\\HP\\Desktop\\Codes\\coll\\internship\\boot\\static\\brand"
    # Join the path and folder name
    path = os.path.join(path, str(results[0][0]))
    # Create the folder
    os.makedirs(path, exist_ok=True)
    return "success"

def category_name(category_id):
    query = "SELECT name FROM walpar_nutritions.categories WHERE brand_id= '" + str(category_id) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results[0][0]

def category_id(category_name):
    query = "SELECT brand_id,name FROM walpar_nutritions.categories WHERE name= '" + str(category_name) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def prosuct_list():
    query = "SELECT name, price, product_id, brand_id FROM products ORDER BY product_id DESC LIMIT 8;"
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

def add_product_direct(product_name,product_description,product_price,Categories_id):
    query_insert_into_cart = "INSERT INTO products (name, description, price,brand_id) VALUES (%s, %s, %s ,%s);"
    values = (product_name,product_description,product_price,Categories_id)
    cursorObject.execute(query_insert_into_cart, values)
    conn.commit()
    query = "SELECT LAST_INSERT_ID() AS LastID;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results[0][0]

def add_image(product_id,image_name):
    query = "INSERT INTO images (product_id,image_name) VALUES (%s, %s);"
    values = (product_id,image_name)
    cursorObject.execute(query, values)
    conn.commit()
    return "success"

def fetch_brandId(product_id):
    query = "SELECT brand_id FROM walpar_nutritions.products WHERE product_id= '" + str(product_id) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results[0][0]

def fetch_productDetails_Edit(product_id):
    query = "SELECT name, description, price, brand_id FROM walpar_nutritions.products WHERE product_id= '" + str(product_id) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def fetch_image_Edit(product_id):
    query = "SELECT image_name from walpar_nutritions.images WHERE product_id= '" + str(product_id) + "';"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def edit_product_direct(product_id,product_name,product_description, product_price,Categories_id):
    query_insert_into_cart = "UPDATE products SET name = %s, description = %s, price = %s, brand_id = %s WHERE product_id = %s;"
    values = (product_name,product_description,product_price,Categories_id, product_id)
    cursorObject.execute(query_insert_into_cart, values)
    conn.commit()
    
    return 'success'

def delete_image_All(product_id):
    query = "DELETE FROM walpar_nutritions.images WHERE product_id ='" + str(product_id) + "';"
    cursorObject.execute(query)
    conn.commit()
    return 'success'

def fetch_product_category(product_id):
    query = "SELECT brand_id FROM products WHERE product_id = %s"
    cursorObject.execute(query, (product_id,))
    result = cursorObject.fetchone()
    if result:
        return result[0]
    else:
        return None

def delete_images(product_id):
    query = "DELETE FROM images WHERE product_id = %s"
    cursorObject.execute(query, (product_id,))
    conn.commit()

def delete_product(product_id):
    query = "DELETE FROM images WHERE product_id = %s"
    cursorObject.execute(query, (product_id,))
    conn.commit()

    query = "DELETE FROM products WHERE product_id = %s"
    cursorObject.execute(query, (product_id,))
    conn.commit()

    return "success"

def search_product_by_id(product_id):
    query = "SELECT name, price, product_id, brand_id FROM products WHERE product_id = %s"
    cursorObject.execute(query, (product_id,))
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

def search_product_by_name(product_name):
    query = "SELECT name, price, product_id, brand_id FROM products WHERE name LIKE %s"
    cursorObject.execute(query, ('%' + product_name + '%',))
    results = cursorObject.fetchall()
    results_with_file_names = []
    for result in results:
        product_id = result[2]
        files_in_folder = fetch_image_name(product_id)
        # Create a new tuple with the additional file_names
        result_with_files = result + (files_in_folder,)

        # Add the new tuple to the list
        results_with_file_names.append(result_with_files)

    return results_with_file_names

def totoal_product_ordered(product_id):
    query = "select sum(quantity) from walpar_nutritions.order_items group by product_id having product_id=%s"
    cursorObject.execute(query,(product_id,))
    results = cursorObject.fetchall()
    return results

def totoal_product_inorder(product_id):
    query = "select sum(oi.quantity) from walpar_nutritions.order_items oi join walpar_nutritions.orders o on oi.order_id = o.order_id where status in ('shipped','pending') group by product_id having product_id =%s"
    cursorObject.execute(query,(product_id,))
    results = cursorObject.fetchall()
    return results

def totoal_completed_order(product_id):
    query = "select sum(oi.quantity) from walpar_nutritions.order_items oi join walpar_nutritions.orders o on oi.order_id = o.order_id where status in ('completed') group by product_id having product_id =%s"
    cursorObject.execute(query,(product_id,))
    results = cursorObject.fetchall()
    return results

def all_orders():
    query="select u.first_name, u.last_name, u.email, o.order_id, o.order_date,o.total_amount,o.status, sum(oi.quantity) from orders o join users u on o.user_id = u.user_id join order_items oi on oi.order_id = o.order_id group by oi.order_id order by o.order_date desc;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def panding_orders():
    query="select u.first_name, u.last_name, u.email, o.order_id, o.order_date,o.total_amount,o.status, sum(oi.quantity) from orders o join users u on o.user_id = u.user_id join order_items oi on oi.order_id = o.order_id group by oi.order_id having status in ('shipped','pending') ;"
    cursorObject.execute(query)
    results = cursorObject.fetchall()
    return results

def order_padeDetail_one(order_id):
    query="select o.order_id, u.first_name, u.last_name, u.email, o.order_date, o.total_amount, o.status, o.delivery_date from orders o join users u on o.user_id = u.user_id where o.order_id=%s;"
    cursorObject.execute(query,(order_id,))
    results = cursorObject.fetchall()
    return results

def order_padeDetail_two(order_id):
    query="select bd.custom_name, bd.custom_mobile_number, bd.custom_email, bd.billing_date, a.street_address, a.city, a.state, a.zip_code from bill_details bd join addresses a on a.address_id = bd.billing_address_id where bd.order_id=%s;"
    cursorObject.execute(query,(order_id,))
    results = cursorObject.fetchall()
    return results

def update_order_status(order_id,new_status):
    query="UPDATE `walpar_nutritions`.`orders` SET `status` = %s WHERE `order_id` = %s;"
    cursorObject.execute(query,(new_status,order_id,))
    conn.commit()
    return "success"

def cancel_order_status(order_id):
    new_status="cancel"
    query="UPDATE `walpar_nutritions`.`orders` SET `status` = %s WHERE `order_id` = %s;"
    cursorObject.execute(query,(new_status,order_id,))
    conn.commit() 
    return "success"