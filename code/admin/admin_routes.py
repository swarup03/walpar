from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
import admin_database as adb
import database as db
import os
# from admin_database import newOrder,orderPanding,orderShipped, adminDetail,pandingAmount,recentOrder,recentUser,fatch_best_seller,add_admin,login_user,fetch_all_users,user_profile_details,user_address_details,user_address_delete,fetch_orders_list
import bcrypt
from werkzeug.utils import secure_filename
from PIL import Image
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def validate_image_dimensions(file):
    try:
        image = Image.open(file)
        width, height = image.size
        print(width,height)
        return width == 2000 and height == 600
    except Exception as e:
        print(e)
        return False

@admin_bp.route("/")
def dashboard():
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        new_orders= adb.newOrder()
        panding_order =adb.orderPanding()
        order_shipped = adb.orderShipped()
        panding_amount = adb.pandingAmount()
        if panding_amount == None:
            panding_amount=0
        recent_order=adb.recentOrder()
        new_user= adb.recentUser()
        best_product =adb.fatch_best_seller()
        return render_template("admin/index.html",best_product=best_product,new_orders=new_orders,admin_detail=admin_detail,panding_order=panding_order,order_shipped=order_shipped,panding_amount = panding_amount,recent_order=recent_order, new_user=new_user)
    else:
        return redirect(url_for('admin.verifyAdmin'))

@admin_bp.route("/allUser")
def allUSer():
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        all_users =adb.fetch_all_users()
        return render_template("admin/user-card.html", all_users=all_users,admin_detail=admin_detail)
    else:
        return redirect(url_for('admin.verifyAdmin'))

@admin_bp.route("/pendingOrders")
def pandingOrders():
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        panding_order= adb.panding_orders()
        return render_template("admin/order-history.html",admin_detail=admin_detail,order_list=panding_order, header="Pending Orders")

@admin_bp.route("/viewOrders")
def viewOrders():
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        view_ordrs = adb.all_orders( )
        return render_template("admin/order-history.html",admin_detail=admin_detail,order_list=view_ordrs, header="All Orders")

@admin_bp.route("/order/<order_id>")
def Orders(order_id):
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        user_detail = adb.order_padeDetail_one(order_id)
        bill_detail = adb.order_padeDetail_two(order_id)
        product_list=db.ordered_product_list(order_id)
        return render_template("admin/order-detail.html",admin_detail=admin_detail,user_detail=user_detail,bill_detail=bill_detail,product_list=product_list)

@admin_bp.route("/user/<user_id>")
def userProfile(user_id):
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        user_details = adb.user_profile_details(user_id)
        user_add = adb.user_address_details(user_id)
        order_list = adb.fetch_orders_list(user_id)
        return render_template("admin/user-profile.html",user_details=user_details,user_add = user_add,order_list=order_list,admin_detail=admin_detail)
    else:
        return redirect(url_for('admin.verifyAdmin'))

@admin_bp.route("/category")
def category():
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        category_name =adb.product_category()
        return render_template("admin/main-category.html",category_name=category_name,admin_detail=admin_detail)
    else:
        return redirect(url_for('admin.verifyAdmin'))

@admin_bp.route("/category/<category_id>")
def product_category(category_id):
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        category_product =db.fatch_category_product(category_id)
        category_name = adb.category_name(category_id)
        return render_template("admin/category_product.html",category_product=category_product,category_name=category_name,admin_detail=admin_detail)
    else:
        return redirect(url_for('admin.verifyAdmin'))

@admin_bp.route("/products")
def products():
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        product_list = adb.prosuct_list()
        return render_template("admin/product-grid.html", product_list=product_list,admin_detail=admin_detail)
    else:
        return redirect(url_for('admin.verifyAdmin'))
    

@admin_bp.route("/addProduct")
def addproducts():
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        category_name =adb.product_category()
        return render_template("admin/product-add.html",category_name=category_name,admin_detail=admin_detail)
    else:
        return redirect(url_for('admin.verifyAdmin'))
    
@admin_bp.route("/addProduct/<category_name>")
def addCategoryproducts(category_name):
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        default_category= adb.category_id(category_name)
        return render_template("admin/product-add.html",default_category=default_category,admin_detail=admin_detail)
    else:
        return redirect(url_for('admin.verifyAdmin'))
    
@admin_bp.route("/product/<product_id>")
def viewProduct(product_id):
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        file_names =db.fetch_image_name(product_id)
        brandId=adb.fetch_brandId(product_id)
        product_detail = db.get_product_detail(product_id)
        total_orders = adb.totoal_product_ordered(product_id)
        total_inorder = adb.totoal_product_inorder(product_id)
        toal_completed_order = adb.totoal_completed_order(product_id)
        if total_inorder == []:
            total_inorder=0
        else:
            total_inorder=total_inorder[0][0]
            
        if total_orders == []:
            total_orders=0
        else:
            total_orders=total_orders[0][0]
            
        if toal_completed_order == []:
            toal_completed_order=0
        else:
            toal_completed_order=toal_completed_order[0][0]
        print(total_inorder,total_orders,toal_completed_order)
        return render_template("admin/product-detail.html",file_names=file_names,product_detail=product_detail,brandId=brandId,product_id=product_id,total_orders=total_orders,total_inorder=total_inorder,toal_completed_order=toal_completed_order,admin_detail=admin_detail)
    else:
        return redirect(url_for('admin.verifyAdmin'))
    
@admin_bp.route("/editProduct/<product_id>")
def editProducts(product_id):
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        admin_detail =adb.adminDetail(session_user_id)
        category_name =adb.product_category()
        images=adb.fetch_image_Edit(product_id)
        details=adb.fetch_productDetails_Edit(product_id)
        return render_template("admin/product-edit.html",category_name=category_name,details=details,images=images,product_id=product_id,admin_detail=admin_detail)
    else:
        return redirect(url_for('admin.verifyAdmin'))

@admin_bp.route("/addAdmin")
def addAdmin():
    return render_template("admin/sign-up.html")

@admin_bp.route("/loginAdmin")
def verifyAdmin():
    return render_template("admin/sign-in.html")

@admin_bp.route("/addAdminRequest",methods=["POST"])
def add_admin_request():
    if request.method == "POST":
        fname = request.form.get("name")
        uname = request.form.get("username")
        passw= request.form.get("password")
        cpassw = request.form.get("confirmpassword")
        if passw == cpassw:
            status = adb.add_admin(fname,uname,passw)
            if status == "success":
                
                return redirect(url_for('verifyAdmin'))
            else:
                return render_template("admin/sign-up.html",status=status)
        else:
            return render_template("admin/sign-up.html",status="Both password are different.")
    else:
        return render_template("admin/sign-in.html")
        

@admin_bp.route("/verifyUserRequest",methods=["POST"])
def verify_admin_request():
    if request.method == "POST":
        uname = request.form.get("uname")
        passw= request.form.get("password")
        status = adb.login_user(uname, passw)
        if status == "success":
            # After successful login
            session['Walpar-Nutritions_admin_session'] = uname
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template("admin/sign-in.html", error=status)
    else:
        return render_template("admin/404.html")

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.verifyAdmin'))

@admin_bp.route('/deleteAddress/<user_id>/<address_id>',methods=["POST"])
def deleteAddress(user_id,address_id):
    if request.method == "POST":
        session_user_id = session.get('Walpar-Nutritions_admin_session')
        if session_user_id:
            admin_detail =adb.adminDetail(session_user_id)
            delete_address = adb.user_address_delete(address_id)
            if delete_address == "success":
                return redirect(url_for("admin.userProfile",user_id=user_id))

@admin_bp.route("/createUser",methods=["POST"])
def signup_request():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        passw= request.form.get("password")
        address1 = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zip = request.form.get("zipCode")
        sex= request.form.get("inlineRadioOptions")
        status = db.signup_user(fname,lname,email,passw,address1,city,state,zip,sex)

        if status == "success":
            return redirect(url_for('admin.allUSer'))
        else:
            return render_template("signup.html", active="profile_active",error=status)
        
@admin_bp.route("/findUser",methods=["POST"])
def find_user():
    if request.method == "POST":
        email = request.form.get("email")
        status = adb.fetch_user(email)
        if status == "User doesn't exists.":
            return render_template("admin/user-card.html",error=status)
        else:
            return redirect(url_for("admin.userProfile",user_id=status))
        
@admin_bp.route('/removeUser/<user_id>',methods=["POST"])
def deleteUser(user_id):
    session_user_id = session.get('Walpar-Nutritions_admin_session')
    if session_user_id:
        if request.method == "POST":
            admin_detail =adb.adminDetail(session_user_id)
            delete_user = adb.remove_user(user_id)
            if delete_user == "success":
                return redirect(url_for("admin.allUSer"))

@admin_bp.route("/addCategory",methods=["POST"])
def add_category():
    if request.method == "POST":
        name = request.form.get("category-name")
        category_detail = request.form.get("category-detail")
        about_category = request.form.get("category-about")
        file = request.files.get('file')
        print(file)
        if file:
            # Validate the image dimensions
            if not validate_image_dimensions(file):
                return "Image dimensions must be 2000x600 pixels."
        else:
            return "Image file not found."

        # Save the file with the specified name and location
        filename = f"{name}_banner.jpeg"
        file.save(os.path.join("C:\\Users\\HP\\Desktop\\Codes\\coll\\internship\\boot\\static", filename))
        status = adb.add_category(name,category_detail,about_category)
        if status == "success":
            return redirect(url_for("admin.category"))
        else:
            return redirect(url_for("admin.category",error=status))

@admin_bp.route("/addProductRequest",methods=["POST"])
def add_product_request():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        Categories_id = request.form.get("Categories")
        product_description = request.form.get("product_description")
        product_price = request.form.get("product_price")
        # get the file from the request
        files = request.files.getlist('file')
        status = adb.add_product_direct(product_name,product_description,product_price,Categories_id)
        if status == "error":
            return redirect(url_for("admin.category",error=status))
        else:
            for index, file in enumerate(files):
                if file:
                    # Generate the new filename based on category_id and count
                    new_filename = f"{status}{index + 1}.{file.filename.split('.')[-1]}"
                    # Save the file to the preferred directory
                    file.save(f"C:\\Users\\HP\\Desktop\\Codes\\coll\\internship\\boot\\static\\brand\\{Categories_id}\\{new_filename}")
                    adb.add_image(status,new_filename)
            return redirect(url_for("admin.viewProduct",product_id=status))

@admin_bp.route("/editProductRequest/<product_id>", methods=["POST"])
def edit_product_request(product_id):
    if request.method == "POST":
        product_name = request.form.get("product_name")
        Categories_id = request.form.get("Categories")
        product_description = request.form.get("product_description")
        product_price = request.form.get("product_price")
        # get the file from the request
        files = request.files.getlist('file')

        # Fetch old category ID before updating
        old_categories_id = adb.fetch_product_category(product_id)

        # Update product details
        status = adb.edit_product_direct(product_id, product_name, product_description, product_price, Categories_id)
        if status != "success":
            return redirect(url_for("admin.category", error=status))
        else:
            # Check if files were uploaded
            existing_images = adb.fetch_image_Edit(product_id)
            if any(files):
                # Fetch existing images for the product
                # Delete existing images from database and filesystem
                adb.delete_images(product_id)
                for image in existing_images:
                    image_filename = image[0]
                    image_path = os.path.join("C:\\Users\\HP\\Desktop\\Codes\\coll\\internship\\boot\\static\\brand\\", str(old_categories_id), image_filename)
                    if os.path.exists(image_path):
                        os.remove(image_path)

                # Save new images to filesystem and add to database
                for index, file in enumerate(files):
                    if file:
                        new_filename = f"{product_id}{index + 1}.{file.filename.split('.')[-1]}"
                        file.save(f"C:\\Users\\HP\\Desktop\\Codes\\coll\\internship\\boot\\static\\brand\\{Categories_id}\\{new_filename}")
                        adb.add_image(product_id, new_filename)
            else:
                # If no new files were uploaded, move existing images to new category folder
                for image in existing_images:
                    image_filename = image[0]
                    old_image_path = os.path.join("C:\\Users\\HP\\Desktop\\Codes\\coll\\internship\\boot\\static\\brand\\", str(old_categories_id), image_filename)
                    new_image_path = os.path.join("C:\\Users\\HP\\Desktop\\Codes\\coll\\internship\\boot\\static\\brand\\", str(Categories_id), image_filename)
                    os.rename(old_image_path, new_image_path)

            return redirect(url_for("admin.viewProduct", product_id=product_id))

@admin_bp.route("/removeProduct/<product_id>", methods=["POST"])
def removeProduct(product_id):
    if request.method == "POST":
        # Fetch category ID before deleting the product
        category_id = adb.fetch_product_category(product_id)

        # Delete product and its images from the database
        status = adb.delete_product(product_id)
        if status != "success":
            return redirect(url_for("admin.category", error=status))

        # Delete product images from the filesystem
        product_image_folder = os.path.join("C:\\Users\\HP\\Desktop\\Codes\\coll\\internship\\boot\\static\\brand\\", str(category_id))
        product_images = os.listdir(product_image_folder)
        for image in product_images:
            if image.startswith(str(product_id)):
                image_path = os.path.join(product_image_folder, image)
                if os.path.exists(image_path):
                    os.remove(image_path)
        return redirect(url_for("admin.products"))  # Redirect to a suitable page after deletion


@admin_bp.route("/search", methods=["POST"])
def search_product():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        product_id = request.form.get("product_id")
        error=None
        results_for_name = None
        result_for_id =None
        if product_name:
            results_for_name = adb.search_product_by_name(product_name)
        
        if product_id:
            result_for_id = adb.search_product_by_id(product_id)
            
        if not results_for_name and not result_for_id:
            error="product not found."
        print(result_for_id,results_for_name)
        return render_template("admin/product-grid.html", results_for_name=results_for_name, result_for_id=result_for_id, error=error)
    else:
        return render_template("admin/404.html")


@admin_bp.route("/updateOrderStatus/<order_id>",methods=["POST"])
def update_status(order_id):
    if request.method == "POST":
        new_status = request.form.get("status")
        status= adb.update_order_status(order_id,new_status)
        if status == "success":
            return redirect(url_for("admin.Orders",order_id=order_id))

@admin_bp.route("/cancelOrderStatus/<order_id>",methods=["POST"])
def cancel_status(order_id):
    if request.method == "POST":
        session_user_id = session.get('Walpar-Nutritions_admin_session')
        if session_user_id:
            status= adb.cancel_order_status(order_id)
            if status == "success":
                return redirect(url_for("admin.Orders",order_id=order_id))