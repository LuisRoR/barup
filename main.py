from flask import Flask, request, redirect, render_template, session, flash, url_for
from app import app, db
from models import Product, Purchase, Inventory_check
import cgi
from sqlalchemy import desc
from sqlalchemy.orm import lazyload
from jinja2 import Template


"""
NEW CODE
"""
@app.route('/', methods=['GET'])
def index():
    """
    #users = User.query.all()
    page = request.args.get('page', 1, type=int)
    paged_users = User.query.order_by(User.username.desc()).paginate(
        page, 3, False)
   
    next_url = url_for('index', page=paged_users.next_num) \
        if paged_users.has_next else None
    prev_url = url_for('index', page=paged_users.prev_num) \
        if paged_users.has_prev else None    
    
    users = paged_users.items
    """
    return render_template('index.html',
        title="Index", 
     )

@app.route('/catalog', methods=['GET'])
def catalog():
    #products = session.query(Product).all()
    #roducts = session.execute(Product.select())
    products = Product.query.filter_by().all()
    return render_template('catalog.html',
        title="Catalog", products=products,
     )

@app.route('/buy', methods=['POST'])
def add_to_cart():
    #products = session.query(Product).all()
    #roducts = session.execute(Product.select())
    #products = Product.query.filter_by().all()
    #product_id = (int)(request.form['product_id'])

    #print(product_id )
    #print(price)
    #SSprint(quantity)

    quantity = (int)(request.form['quantity'])
    price = (float)(request.form['price'])
    product_id = (int)(request.form['product_id'])
  
    #new_purchase = Purchase(quantity, price, product_id, pur_date=None)

        # if the user typed nothing at all, redirect and tell them the error
    #if (not price) or (price.strip() == ""):
     #   error = "Please specify the movie you want to add."
     #   return redirect("/?error=" + error)

    new_purchase = Purchase(quantity, price, product_id,)

    db.session.add(new_purchase)
    db.session.commit()

    products = Product.query.filter_by().all()
    return render_template('catalog.html',
        title="Catalog", products=products, 
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
    new_product = Product(brand, name, bottle_weight, vintage, label_name, country, volume, category, description)

    db.session.add(new_product)
    db.session.commit()


   
    return render_template('product.html', 
        title="product", 
        product=new_product,
    )


@app.route('/inventory', methods=['GET'])
def inventory():
    #products = session.query(Product).all()
    #roducts = session.execute(Product.select())
    products = Product.query.filter_by().all()
    return render_template('inventory.html',
        title="Inventory", products=products,
     )


@app.route('/create', methods=['GET'])
def create():

    """
    #users = User.query.all()
    page = request.args.get('page', 1, type=int)
    paged_users = User.query.order_by(User.username.desc()).paginate(
        page, 3, False)

    next_url = url_for('index', page=paged_users.next_num) \
        if paged_users.has_next else None
    prev_url = url_for('index', page=paged_users.prev_num) \
        if paged_users.has_prev else None    
    
    users = paged_users.items
    """
    return render_template('create.html',
        title="create", 
     )

@app.route('/dummy', methods=[ 'GET'])
def dummy():

    return render_template('dummy.html',
        title="dummy", 
     )

@app.route('/reports', methods=['GET'])
def reports():

    """
    #users = User.query.all()
    page = request.args.get('page', 1, type=int)
    paged_users = User.query.order_by(User.username.desc()).paginate(
        page, 3, False)

    next_url = url_for('index', page=paged_users.next_num) \
        if paged_users.has_next else None
    prev_url = url_for('index', page=paged_users.prev_num) \
        if paged_users.has_prev else None    
    
    users = paged_users.items
    """
    return render_template('reports.html',
        title="reports", 
     )

@app.route('/test', methods=['GET'])
def test():

    return render_template('test.html',
        title="test", 
     )

@app.route('/product2', methods=['GET'])
def product2():

    return render_template('product2.html',
        title="product2", 
     )


"""
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'list_blogs']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
"""


"""
def validate_entry(title, body):
    result = ""
    blog_title = title
    blog_body = body
    blog_title_error = ''
    blog_body_error = ''

    if blog_title == '':
        blog_title_error = "Plese fill in the title"
    if blog_body == '':
        blog_body_error = "Please fill in the body"

    if blog_title_error or blog_body_error: 
        return render_template('blog_new_post.html', 
            blog = blog_title, body = blog_body,
            blog_title_error = blog_title_error,
            blog_body_error = blog_body_error
            )
    return result
"""
"""
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password(user.password, password):
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            if not user:
                flash('User does not exist, try again!', 'error')     
                return redirect ('/login')  
            else:  
                flash('Incorrect password, try again!', 'error')
            return redirect ('/login') 
        
    return render_template('login.html')
"""

"""
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username= request.form['username']
        password = request.form['password']
        verify_password = request.form['verify']

        if username == '' or password == '' or verify_password == '':
            flash('One or more fields are invalid, try again', 'error') 
            return redirect ('/signup')
        if password != verify_password:
            flash('Passwords do not match, try again', 'error') 
            return redirect ('/signup')
    
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('Username already exists, try again!', 'error')

    return render_template('signup.html')      
"""

"""
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')
"""

"""
@app.route('/', methods=[ 'GET'])
def index():
    #users = User.query.all()
    page = request.args.get('page', 1, type=int)
    paged_users = User.query.order_by(User.username.desc()).paginate(
        page, 3, False)

    next_url = url_for('index', page=paged_users.next_num) \
        if paged_users.has_next else None
    prev_url = url_for('index', page=paged_users.prev_num) \
        if paged_users.has_prev else None    
    
    users = paged_users.items
    return render_template('index.html',
        title="Index", 
        users=users, 
        next_url=next_url,
        prev_url=prev_url)
"""
"""
    return render_template('index.html',
        title="Index", id=product_id, qty=quantity, price=price,
     )
"""

"""
@app.route('/blog', methods=['POST', 'GET'])
def list_blogs(): 
    if request.method == 'POST': 
        blog_title = request.form['title']
        blog_body = request.form['body']
       
        error_page = validate_entry(blog_title, blog_body)
        if error_page:
            return error_page

        #succes
        owner = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(blog_title, blog_body, owner, pub_date=None)
        db.session.add(new_blog)
        db.session.commit()

        new_blog_id = new_blog.id
        return redirect(f'/display_blog?id={new_blog_id}') 



    if (request.method == 'GET'):
        #blogs = Blog.query.all()
        #blogs = Blog.query.order_by(Blog.pub_date.desc()).all()
        users = User.query.all()

    page = request.args.get('page', 1, type=int)
    paged_blogs = Blog.query.order_by(Blog.pub_date.desc()).paginate(
        page, 3, False)

    next_url = url_for('list_blogs', page=paged_blogs.next_num) \
        if paged_blogs.has_next else None
    prev_url = url_for('list_blogs', page=paged_blogs.prev_num) \
        if paged_blogs.has_prev else None 

    blogs = paged_blogs.items
    return render_template('blog_listings.html',
        title="Blog Post", 
        blogs=blogs,
        users=users,
        next_url=next_url,
        prev_url=prev_url) 
"""

"""
@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        return render_template('blog_new_post.html')
    return redirect('/')
"""

"""
@app.route('/display_blog', methods=['GET', 'POST'])
def display_blog():

    blog_id = int(request.args['id'])
    blog = Blog.query.get(blog_id)
   
    user = User.query.filter_by(id=blog.owner_id).first()

    db.session.add(user)
    db.session.commit()

    db.session.add(blog)
    db.session.commit()

    return render_template('display_blog.html', blog=blog, user=user)  
"""

"""
@app.route('/singleUser', methods=['GET'])
def single_user():
    user_id = int(request.args['id'])
    
    user = User.query.filter_by(id=user_id).first()
    owner = user_id
    blogs = Blog.query.all()
    blogs = Blog.query.filter_by(owner_id=owner).all()

    return render_template('singleUser.html', 
        blogs=blogs, 
        user=user) 
"""



if __name__ == '__main__':
    app.run()
