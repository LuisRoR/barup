from app import db
from datetime import datetime, date

"""
class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3

class MyClass(Base):
    __tablename__ = 'some_table'
    id = Column(Integer, primary_key=True)
    value = Column(Enum(MyEnum))
"""

class Product (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    name = db.Column(db.String(50))
    bottle_weight = db.Column(db.Float)
    vintage = db.Column(db.Integer)
    label_name = db.Column(db.String(50))
    country = db.Column(db.String(50))
    volume = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.String(2000))
    purchase = db.relationship('Purchase', backref='product', )

    def __init__(self, brand, name, bottle_weight, vintage, label_name, country, volume,category, description):
        self.brand = brand
        self.name = name
        self.bottle_weight = bottle_weight
        self.vintage = vintage
        self.label_name  = label_name
        self.country = country
        self.volume = volume
        self.category = category
        self.description = description

class Purchase (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    purchase_date = db.Column(db.DateTime)
    inventory = db.relationship('Inventory_check', backref='purchase', )
    def __init__(self, quantity, price, product, purchase_date=None):
        self.quantity = quantity
        self.price = price
        self.product_id = product
        if purchase_date is None:
            purchase_date = datetime.utcnow().strftime("%Y%m%d")
            #purchase_date = date.today()
        self.purchase_date = purchase_date

class Inventory_check (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    approx_level = db.Column(db.Float)
    weight = db.Column(db.Float)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    date_consumed = db.Column(db.DateTime)
    date_measured = db.Column(db.DateTime)
    def __init__(self, approx_level, weight, purchase, date_consumed , date_measured=None):
        self.approx_level = approx_level
        self.weight = weight
        self.purchase_id = purchase
        self.date_consumed  = date_consumed 
        if date_measured  is None:
            date_measured  = datetime.utcnow()
        self.date_measured  = date_measured                 

