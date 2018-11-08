from flask import Flask, request, redirect, render_template, session, flash, url_for
from app import app, db
from models import Product, Purchase, Inventory_check
import cgi
from sqlalchemy import desc, text, update
from sqlalchemy.sql import exists, text
from sqlalchemy.orm import lazyload
from jinja2 import Template
from sqlalchemy.orm.query import Query
import os
from datetime import datetime, date


@app.template_filter('datetimeformat')
def datetimeformat(value, format='%B %d, %Y'):
    return value.strftime(format)


@app.route("/chart")
def chart():


    labels = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    #f or pie chart
    colors = [ "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD", "#ABCABC", "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA"  ]
    
    values = []

    format='%B'

    jan = 0
    feb = 0
    mar = 0
    apr = 0
    may = 0
    jun = 0
    jul = 0
    aug = 0
    sep = 0
    octo = 0
    nov = 0
    dec = 0

    total = 0
    
    purchases = Purchase.query.filter_by().all()
    
    for purchase in purchases:
        val = purchase.price * purchase.quantity
        month = purchase.purchase_date.strftime(format)
        total += val

        if month == 'January':
            jan += val
        elif month == 'February':  
            feb += val
        elif month == "March":
            mar += val
        elif month == 'April':
            apr += val
        elif  month == 'May':  
            may += val
        elif month == "June":
            jun += val
        elif month == 'July':
            jul += val
        elif month == 'August':  
            aug += val
            total += val
        elif month == "September":
            sep += val
        elif month == 'October':
            octo += val
        elif month == 'November':  
            nov += val
        else:
            dec += val
            total += val

    values.append(jan)        
    values.append(feb)
    values.append(mar)
    values.append(apr)        
    values.append(may)
    values.append(jun)
    values.append(jul)        
    values.append(aug)
    values.append(sep)
    values.append(octo)        
    values.append(nov)
    values.append(dec)

    return render_template('chart.html', values=values, labels=labels, total=total, set=zip(values, labels, colors))
 

@app.route('/', methods=['GET'])
def index():
 
    return render_template('index.html',
        title="Index", 
     )


@app.route('/catalog', methods=['GET'])
def catalog():

    products = Product.query.filter_by().all()

    return render_template('catalog.html',
        title="Catalog", 
        products=products,
     )


@app.route('/buy', methods=['POST'])
def add_to_cart():

    quantity = (request.form['quantity'])
    price = (request.form['price'])
    print('@@@@@@@@@@@@@@@@@@@')
    print('@@@@@@@@@@@@@@@@@@@', price)
    product_id = (int)(request.form['product_id'])
  
    if quantity == 0:
        error = 'quantity is required before proceding with purchase'
        return redirect("/catalog?=" + error) 

    if price is None:
        error = 'price is required before proceding with purchase'
        return redirect("/catalog?=" + error) 

    quantity = (int)(quantity)
    pri = (float)(price)

    new_purchase = Purchase(quantity, price, product_id,)
    db.session.add(new_purchase)
    db.session.commit()

    temp_qty = new_purchase.quantity
    temp_id = new_purchase.id
    bottle = 0
    while bottle < temp_qty:
        new_inventory = Inventory_check(100.00, 1400, temp_id, None )
        db.session.add(new_inventory)
        bottle += 1
   
    db.session.commit()


    products = Product.query.filter_by().all()
    return render_template('catalog.html',
        title="Catalog", 
        products=products, 
     )


@app.route('/product', methods=['POST'])
def product():

    brand = request.form['brand']
    name = request.form['name']
    bottle_weight = 1400.00
    vintage = request.form['vintage']
    label_name  = request.form['label_name']
    country = request.form['country']
    volume = request.form['volume']
    category = request.form['category']
    description = request.form['description']
    
    if vintage == "n/a":
        vintage = 0

    name_query = Product.query.filter(Product.name == name)
    if ( name_query.count() > 0 ):
        error = 'Prouct already exist'
        return redirect("/create?=" + error) 
  
    new_product = Product(brand, name, bottle_weight, vintage, label_name, country, volume, category, description)
    db.session.add(new_product)
    db.session.commit()
   
    return render_template('product.html', 
        title="product", 
        product=new_product,
    )


@app.route('/purchase', methods=['GET'])
def purchase():
  
    return render_template('purchase.html', 
        title="Purchase", 
    )

@app.route('/display_purchase', methods=['POST'])
def display_purchase():

    start_date = request.form['start-date']
    end_date = request.form['end-date']
    
    purchases= Purchase.query.join(Product, Purchase.product_id == Product.id).add_columns(Product.id, Product.brand, Product.name, Purchase.id, Purchase.product_id, Purchase.quantity, Purchase.price, Purchase.purchase_date,).filter(Purchase.purchase_date >= start_date, Purchase.purchase_date <= end_date).filter(Purchase.product_id == Product.id).all()
    
    total = 0
    for purchase in purchases:
        total += purchase.price * purchase.quantity


    return render_template('display_purchase.html', 
        title="Display purchase", purchases=purchases , start_date=start_date, end_date=end_date, total=total,
    )

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():

    if request.method == 'GET':
       return render_template('inventory.html')
   
    start_date = request.form['start-date']
    if start_date is None:
        print('OOOOOOO  IS NONE   OOOOOOOOOOO', start_date)
    end_date = request.form['end-date']
    if end_date is None:
        print('&&&&&&&&&&&&&&&', end_date,'&&&&&&&&&&&&&&', end_date)
    

    inventory_products = db.session.query(Product, Purchase, Inventory_check).filter(Product.id == Purchase.product_id).filter(Purchase.id == Inventory_check.purchase_id).filter(Inventory_check.date_consumed > start_date, Inventory_check.date_consumed > end_date).all()
   
    results = list(map(lambda row: {"brand": row[0].brand, "name": row[0].name, "label_name": row[0].label_name, "approx_level": row[2].approx_level, "id": row[2].id}, inventory_products))


    return render_template('display_inventory.html',
        title="Display inventory", results=results, start_date=start_date, end_date=end_date, inventory_products=inventory_products,
    )

@app.route('/display_inventory', methods=['POST'])
def display_inventory():

    start_date = request.form['start-date']
    end_date = request.form['end-date']

    inventory_products = (
        db.session.query(Product, Purchase, Inventory_check)
        .filter(Product.id == Purchase.product_id)
        .filter(Purchase.id == Inventory_check.purchase_id)
        .filter(Purchase.purchase_date <= end_date)
        .filter((Inventory_check.date_consumed == None) | (Inventory_check.date_consumed <= end_date))
        .order_by(Product.id)
        .all()
    )
   
    results = list(map(lambda row: {"brand": row[0].brand, "name": row[0].name, "label_name": row[0].label_name, "approx_level": row[2].approx_level, "id": row[2].id}, inventory_products))


    return render_template('display_inventory.html',
        title="Display inventory", results=results, start_date=start_date, end_date=end_date, inventory_products=inventory_products,
    )   


@app.route('/update', methods=['POST', 'GET'])
def update_inventory():

    start_date = request.form['start-date']
    end_date = request.form['end-date']

    item_levels = request.form.getlist('new-level')
    item_ids = request.form.getlist('inventory-id')

    for idx, new_level in zip(item_ids, item_levels):
        row_id = Inventory_check.query.filter_by(id = idx).first()
        print ("@@@@@@  row_id.approx_level :" , row_id.approx_level)
        print ("@@@@@@  new_level :" , new_level)
        print(type(row_id.approx_level))
        print(type(new_level))
        new_level= (float)(new_level)
        print(type(new_level))
        if row_id.approx_level != new_level:
             
            if new_level == 0:
                tooday = date.today()
                row_id.date_consumed = tooday

            row_id.approx_level = new_level

            db.session.commit()

    #inventory_products = db.session.query(Product, Purchase, Inventory_check).filter(Product.id == Purchase.product_id).filter(Purchase.id == Inventory_check.purchase_id)..all()
    inventory_products = (
        db.session.query(Product, Purchase, Inventory_check)
        .filter(Product.id == Purchase.product_id)
        .filter(Purchase.id == Inventory_check.purchase_id)
        .filter(Purchase.purchase_date <= end_date)
        .filter((Inventory_check.date_consumed == None) | (Inventory_check.date_consumed <= end_date))
        .order_by(Product.id)
        .all()
    )
   
    results = list(map(lambda row: {"brand": row[0].brand, "name": row[0].name, "label_name": row[0].label_name, "approx_level": row[2].approx_level, "id": row[2].id}, inventory_products))


    return render_template('display_inventory.html',
        title="Display inventory", results=results, start_date=start_date, end_date=end_date, inventory_products=inventory_products,
    )


@app.route('/create', methods=['GET'])
def create():

    return render_template('create.html',
        title="create", 
     )

@app.route('/reports', methods=['GET'])
def reports():

    return render_template('reports.html',
        title="reports", 
     )

@app.route('/reports-sales', methods=['GET'])
def reports_sales():

    

    return render_template('reports_sales.html',
        title="Sales report", 
     )

     

@app.route('/graph')
def graph():

    import random
    data = [random.randrange(0, 5) for _ in range(5)]

    return render_template('graph.html', data=data)


if __name__ == '__main__':
    app.run()
    #app.run(port=os.environ['PORT'])
    #    app.run(port=os.environ['PORT'])
