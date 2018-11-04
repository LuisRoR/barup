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

    i = 0
    test = ''
    labels = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    values = [0,0,0,0,0,0,0,0,0,0,0,0]
    listLen = len(labels)
    format='%B'
    purchases = Purchase.query.filter_by().all()
    
    total = 0
    for purchase in purchases:
        total += purchase.price * purchase.quantity
        test = purchase.purchase_date.strftime(format)

        if (test == labels[i]):
            values.insert(i, (purchase.price * purchase.quantity)) 

    return render_template('chart.html', values=values, labels=labels, total=total)
 

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

    quantity = (int)(request.form['quantity'])
    price = (float)(request.form['price'])
    product_id = (int)(request.form['product_id'])
  

    new_purchase = Purchase(quantity, price, product_id,)
    db.session.add(new_purchase)
    db.session.commit()

    temp_qty = new_purchase.quantity
    temp_id = new_purchase.id
    bottle = 0
    while bottle < temp_qty:
        new_inventory = Inventory_check(100.00, 1400, temp_id, '2020-01-01', )
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
    vintage = 2000
    label_name  = request.form['label_name']
    country = request.form['country']
    volume = request.form['volume']
    category = "spirit"
    description = request.form['description']
    
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
        title="Display purchase", purchases=purchases , start=start_date, end=end_date, total=total,
    )

@app.route('/inventory', methods=['POST', 'GET'])
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


    return render_template('inventory.html',
        title="Inventory", results=results, start_date=start_date, end_date=end_date, inventory_products=inventory_products,
    )


@app.route('/update', methods=['POST', 'GET'])
def update():

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
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   BREAK  @@@@@")
             
            if new_level == 0:
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

                print('@@@ BEFORE row_id.date.consumed :', row_id.date_consumed )
                tooday = date.today()
                print ('2day: ', type(tooday))
                print(type(row_id.date_consumed ))
                row_id.date_consumed = tooday
                print ('@@@ TODAY :', date.today() )
                print('@@@ AFTER row_id.date.consumed :', row_id.date_consumed )

            row_id.approx_level = new_level

            db.session.commit()

    inventory_products = db.session.query(Product, Purchase, Inventory_check).filter(Product.id == Purchase.product_id).filter(Purchase.id == Inventory_check.purchase_id).filter(Inventory_check.date_consumed > start_date, Inventory_check.date_consumed > end_date).all()
   
    results = list(map(lambda row: {"brand": row[0].brand, "name": row[0].name, "label_name": row[0].label_name, "approx_level": row[2].approx_level, "id": row[2].id}, inventory_products))


    return render_template('inventory.html',
        title="Inventory", results=results, start_date=start_date, end_date=end_date, inventory_products=inventory_products,
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


@app.route('/graph')
def graph():

    import random
    data = [random.randrange(0, 5) for _ in range(5)]

    return render_template('graph.html', data=data)


if __name__ == '__main__':
    app.run()
    #app.run(port=os.environ['PORT'])
    #    app.run(port=os.environ['PORT'])
