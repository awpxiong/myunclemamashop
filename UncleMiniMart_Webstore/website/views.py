from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Product
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    prod_all = Product.query.all()
    return render_template("home.html", user=current_user, products=prod_all)

@views.route('/allproduct')
def allproducts():
    prod_all = Product.query.all()
    return render_template("allproduct.html", user=current_user, products=prod_all)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    prod_all = Product.query.all()
    if request.method == 'POST':
        productID = request.form.get('prodID')
        productname = request.form.get('prodname')
        productprice = request.form.get('prodprice')
        prod_all = Product.query.all()
        prod = Product.query.filter_by(prod_name=productname).first()
        pid = Product.query.filter_by(prod_id=productID).first()

        if prod or pid:
            flash('Failed! Product is existed in database', category ='error')
        elif len(productname) < 2:
            flash('productname has to be more than 2 characters.', category='error')
        elif len(productID) < 1:
            flash('Product ID cant be empty or 0 value.', category='error')
        elif productprice.isalpha():
            flash('Price should only contain Numeric Value!.', category='error')
        elif productID.isalpha():
            flash('Product ID should only containt Numeric Value!.', category='error')
        else:
            new_prod = Product(prod_id=productID, prod_name=productname, prod_price=productprice)
            db.session.add(new_prod)
            db.session.commit() 
            flash('Product has been added successfully!', category='success')
            return redirect(url_for('views.admin'))
    else:
        productID = request.form.get('up_prodID')
        productname = request.form.get('up_prodname')
        productprice = request.form.get('up_prodprice')
        return render_template("admin.html", user=current_user, products=prod_all, mod_prodid=productID, mod_prodname = productname, mod_prodprice=productprice)

@views.route('/admin/update', methods=['GET', 'POST'])
@login_required
def produpdate():
    prod_all = Product.query.all()
    if request.method == 'POST':
        productID = request.values.get('prodID')
        productname = request.values.get('prodname')
        productprice = request.values.get('prodprice')
       
        search_prodID = Product.query.filter_by(prod_id=productID).first()
        if search_prodID:
            search_prodID.prod_name = productname
            search_prodID.prod_price = productprice
            db.session.commit()
            flash('Product has been updated successfully!', category='success')
            return redirect(url_for('views.admin'))
        elif len(productID) < 1:
            flash('Product ID cant be empty or 0 value.', category='error')
        elif productID.isalpha():
            flash('ID should only contain Numeric Value!.', category='error')
        else:
            flash('Product ID does not Exist!', category ='error')
        return render_template("admin.html", user=current_user, products=prod_all, mod_prodid=productID, mod_prodname = productname, mod_prodprice=productprice)
    return render_template("admin.html", user=current_user, products=prod_all)

@views.route('/admin/delete', methods=['GET', 'POST'])
@login_required
def proddelete():
    prod_all = Product.query.all()
    if request.method == 'POST':
        productID = request.values.get('del_prodID')
        productname = request.values.get('del_prodname')
        search_prodID = Product.query.filter_by(prod_id=productID).first()
        search_prodName = Product.query.filter_by(prod_name=productname).first()
        if search_prodID:
            db.session.delete(search_prodID)
            db.session.commit()
            flash('Product has been deleted successfully!', category='success')
            return redirect(url_for('views.admin'))
        elif search_prodName:
            db.session.delete(search_prodName)
            db.session.commit()
            flash('Product has been deleted successfully!', category='success')
            return redirect(url_for('views.admin'))
        elif len(productID) < 1:
            flash('Product ID cant be empty or 0 value.', category='error')
        elif productID.isalpha():
            flash('ID should only contain Numeric Value!.', category='error')
        else:
            flash('Product ID Or Product Name does not Exist!', category ='error')
        return render_template("admin.html", user=current_user, products=prod_all, mod_prodid=productID, mod_prodname = productname, mod_prodprice=productprice)
    return render_template("admin.html", user=current_user, products=prod_all)