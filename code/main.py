from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import admin_database as adb
import database as db
from downloadPDF import generate_invoice_pdf
from admin.admin_routes import admin_bp
app = Flask(__name__, static_folder="static")
app.register_blueprint(admin_bp)
app.secret_key = 'Walpar-Nutritions_session_key'
@app.route("/")
def home():
    cate_name=db.fatch_category_name()
    best_product = db.fatch_best_seller()
    brand_product = db.fatch_category_product(2)
    return render_template("index.html",best_product=best_product, brand_product=brand_product,cate_name=cate_name)

@app.route("/ContactUs")
def contactus():
    cate_name=db.fatch_category_name()
    return render_template("ContactUs.html",cate_name=cate_name)

@app.route("/checkout")
def checkout():
    session_user_email = session.get('Walpar-Nutritions_email_session')
    if session_user_email:
        cate_name=db.fatch_category_name()
        user_detail,address_detail= db.fatch_profile_details(session_user_email)
        cart_product = db.fetch_checkout_cart_products(session_user_email)
        return render_template("checkout.html",user_detail=user_detail,address_detail=address_detail,cart_product=cart_product,cate_name=cate_name)
    else:
        return redirect(url_for('home'))

@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "POST":
        cate_name=db.fatch_category_name()
        search_text = request.form.get("search")
        search_results = db.search_result(search_text)
        return render_template("search.html",search_results=search_results,cate_name=cate_name)

@app.route("/products/<brandId>/<productId>")
def products(brandId,productId):
    cate_name=db.fatch_category_name()
    file_names =db.fetch_image_name(productId)
    brand_product = db.fatch_category_product(brandId)
    product_detail = db.get_product_detail(productId)
    return render_template("product.html", file_names=file_names, brandId=brandId, productId=productId, brand_product=brand_product, product_detail=product_detail,cate_name=cate_name)

@app.route("/category/<categori_id>")
def category(categori_id):
    cate_name=db.fatch_category_name()
    brand_product = db.fatch_category_product(categori_id)
    category_details = db.fatch_category_details(categori_id)
    return render_template("brand.html", brand_product=brand_product, category_details=category_details,cate_name=cate_name)

@app.route("/cart")
def cart_list():
    session_user_email = session.get('Walpar-Nutritions_email_session')
    if session_user_email:
        cate_name=db.fatch_category_name()
        cart_product =db.fatch_user_cart_products(session_user_email)
        return render_template("cart_list.html",active="cart_active",cart_product=cart_product,cate_name=cate_name)

    else:
        return redirect(url_for('profile_login'))

@app.route("/profile")
def profile():
    session_user_email = session.get('Walpar-Nutritions_email_session')
    if session_user_email:
        cate_name=db.fatch_category_name()
        user_detail,address_detail = db.fatch_profile_details(session_user_email)
        order_history = db.fetch_order_history(user_detail[0])
        return render_template("profile.html", active="profile_active", user_detail=user_detail, address_detail=address_detail, order_history=order_history,cate_name=cate_name)
    else:
        return redirect(url_for('profile_login'))

@app.route("/profile/login")
def profile_login():
    return render_template("login.html", active="profile_active")

@app.route("/profile/signup")
def profile_signup():
    return render_template("signup.html", active="profile_active")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/orderSuccess")
def success_order():
    return render_template("success_order.html")

@app.route("/order/<order_id>")
def order(order_id):
    session_user_email = session.get('Walpar-Nutritions_email_session')
    if db.verify_user(order_id,session_user_email) == "success":
        cate_name=db.fatch_category_name()
        order_details=db.order_detail(order_id)
        bill_details=db.bill_detail(order_id)
        product_list = db.ordered_product_list(order_id)
        return render_template("order_page.html",bill_details=bill_details,order_details=order_details, product_list=product_list,cate_name=cate_name)
    else:
        return render_template("error.html")

@app.route("/orderFailed")
def failed_order():
    return render_template("failed_order.html")

@app.route("/signupreq",methods=["GET","POST"])
def signup_request():
    if request.method == "POST":
        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        email = request.form.get("email")
        passw= request.form.get("password")
        address1 = request.form.get("address1")
        city = request.form.get("cityName")
        state = request.form.get("stateName")
        zip = request.form.get("zipCode")
        sex= request.form.get("inlineRadioOptions")
        status = db.signup_user(fname,lname,email,passw,address1,city,state,zip,sex)

        if status == "success":
            return redirect(url_for('profile_login'))
        else:
            return render_template("signup.html", active="profile_active",error=status)

@app.route("/loginreq",methods=["GET","POST"])
def loginreq():
    if request.method == "POST":
        email = request.form.get("email")
        passw= request.form.get("password")
        status = db.login_user(email, passw)
        if status == "success":
            # After successful login
            session['Walpar-Nutritions_email_session'] = email
            # return redirect(url_for('welcome',email=email))
            return redirect(url_for('profile'))
        else:
            return render_template("login.html", active="profile_active", error=status)

@app.route("/like")
def like():
    session_user_email = session.get('Walpar-Nutritions_email_session')
    if session_user_email:
        cate_name=db.fatch_category_name()
        user_liked_product_detail = db.fatch_user_liked_product(session_user_email)
        return render_template("like.html", active="like_active", user_liked_product_detail=user_liked_product_detail,cate_name=cate_name)
    else:
        return redirect(url_for('profile_login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('profile'))


@app.route("/like_product", methods=["POST"])
def like_product():
    try:
        data = request.get_json()
        productId = data.get('productId')
        user_email = data.get('User_Email')
        status = db.add_product_to_likes(user_email, productId)
        if status == "success":
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'product already liked'})
    except Exception as e:
        print(f"Error in add_to_cart: {str(e)}")
        return jsonify({'error': 'internal server error'})


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()

        productId = data.get('productId')
        quantity = data.get('quantity')
        user_email = data.get('User_Email')
        status = db.insert_into_cart(user_email, productId, quantity)
        if status == "success":
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'product already in the cart'})
    except Exception as e:
        # Log the exception
        print(f"Error in add_to_cart: {str(e)}")
        return jsonify({'error': 'internal server error'})

@app.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    try:
        data = request.get_json()
        cart_id = data.get('cartId')
        new_quantity = data.get('quantity')

        quantity_updated = db.update_product_quantity_from_cart(cart_id, new_quantity)
        if quantity_updated == "success":
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Unable to update quantity'})

    except Exception as e:
        print(f"Error updating quantity in the database: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'})

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    try:
        data = request.get_json()
        cart_id = data.get('cartId')

        status = db.delete_product_from_cart(cart_id)
        if status == "success":
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Unable to update quantity'})

    except Exception as e:
        print(f"Error removing product from cart: {str(e)}")
        return jsonify({'error': 'internal server error'})

@app.route('/remove_from_like', methods=['POST'])
def remove_from_like():
    try:
        data = request.get_json()
        like_id = data.get('likeId')

        status = db.delete_product_from_like(like_id)
        if status == "success":
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Unable to update quantity'})

    except Exception as e:
        print(f"Error removing product from cart: {str(e)}")
        return jsonify({'error': 'internal server error'})

@app.route('/add_address/<user_id>', methods=["GET","POST"])
def add_address(user_id):
    if request.method == "POST":
        address = request.form.get("Address")
        city = request.form.get("City")
        state = request.form.get("State")
        zip = request.form.get("Zip")
        status = db.insert_address(user_id, address, city, state, zip)
        if status == "success":
            return redirect(url_for('profile'))


@app.route("/edit_address/<address_id>",methods=["GET","POST"])
def editAddress(address_id):
    if request.method == "POST":
        address = request.form.get("updatedAddress")
        city= request.form.get("updatedCity")
        state = request.form.get("updatedState")
        zip = request.form.get("updatedZip")
        status = db.update_address(address, city, state, zip,address_id)
        if status == "success":
            return redirect(url_for('profile'))

@app.route('/remove_address/<address_id>', methods=['POST'])
def remove_address_fromDB(address_id):
    try:
        status = db.remove_address(address_id)
        if status == "success":
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Unable to delete address'})

    except Exception as e:
        return jsonify({'error': 'internal server error'})

@app.route('/placeOrderProcess/<user_id>', methods=['POST'])
def place_order(user_id):
    if request.method == "POST":
        name_on_bill = request.form.get("nameOnBill")
        email_on_bill = request.form.get("emailOnBill")
        phoneNo_on_bill = request.form.get("phoneOnBill")
        address_id_on_bill = request.form.get("orderAddress")
        subtotal = db.totalAmountInCart(user_id)
        order_id = db.add_order(user_id, subtotal)
        db.add_bill(order_id,name_on_bill,phoneNo_on_bill,email_on_bill,address_id_on_bill)
        status = db.add_product_to_order(user_id,order_id)
        if status == "success":
            return render_template("success_order.html", order_id =order_id, order_status="success")
        else:
            return render_template("success_order.html",order_status = "false")

from flask import send_file

@app.route('/download_invoice/<int:order_id>')
def download_invoice(order_id):
    # Retrieve order details from the database based on order_id
    # You may need to modify this part to fit your database structure and queries
    order_details = db.order_detail(order_id)
    bill_details = db.bill_detail(order_id)
    ordered_products = db.ordered_product_list(order_id)

    if order_details:
        # Generate PDF
        pdf_filename = f"invoice_order_{order_id}.pdf"
        generate_invoice_pdf(order_details, bill_details, ordered_products, pdf_filename)

        # Serve the PDF for download
        return send_file(pdf_filename, as_attachment=True)

    return "Order not found", 404

app.run(debug=True)