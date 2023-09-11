# this is the module that does creates everything for our database :)
from werkzeug.security import generate_password_hash 
from flask_sqlalchemy import SQLAlchemy #allows our database to read the classes that I make as tables and rows
from flask_login import UserMixin, LoginManager # these two modules allow for loading of a current logged in user
from datetime import datetime
import uuid # for the creation of unique serial keys for the primary keys of each table
from flask_marshmallow import Marshmallow # still not sure what Marshmellow does

#internal imports
from .helpers import get_image # we want to make sure that when a user adds a new comic book to their collection, that it is shown in the card that is added

db = SQLAlchemy() # the creation of our database
login_manager = LoginManager() # instantiate the login manager so that we can have the ability to login
ma = Marshmallow() #instantiating our Marshmellow class, whatever that is

@login_manager.user_loader #this decorator calls for loading in the user
def load_user(user_id):
    return User.query.get(user_id) #this queries our database & brings back the user with the user_id provided

class User(db.Model, UserMixin):

    user_id = db.Column(db.String, primary_key = True)
    first = db.Column(db.String(30))
    last = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(30), nullable = False)
    profile_image = db.Column(db.String) # just for fun :)
    email = db.Column(db.String(150), nullable = False)
    p_number = db.Column(db.String(14), nullable = False) # if there's time, want to use phone number for 2FA will need to install some kind of module for phone number verification
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, username, password, email, p_number, first = '', last = '', profile_image = ''):
        self.user_id = self.set_id()
        self.username = username
        self.email = email
        self.first = first
        self.last = last
        self.p_number = p_number
        self.profile_image = self.set_image(profile_image)
        self.password = self.set_password(password) #we want to use this method to set our password so that it's hashed for security purposes


    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return self.user_id
    
    def set_image(self, image, title):
        if not image:
            image = get_image(title)
        return image
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"Marvel's very own {self.username}"
    


class Comic(db.Model):

    """Table for the comic books that get added to the database"""
    comic_id = db.Column(db.String, primary_key = True)
    image = db.Column(db.String, nullable = False)
    title = db.Column(db.String(200), nullable = False)
    series = db.Column(db.String(100), nullable = False)
    volume = db.Column(db.Integer, nullable = False)
    for_sale = db.Column(db.Boolean, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    page_count = db.Column(db.Integer)
    author = db.Column(db.String(150))
    isbn = db.Column(db.String(17))
    price = db.Column(db.Numeric(precision=7, scale=2), nullable = False) #if it's not for sale, then there's no need to have a price associated with it
    description = db.Column(db.String(500))
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable = False)

    def __init__(self, title, series, volume, for_sale, quantity, user_id, image = '', page_count = 0, author = '', isbn = '', price = 0, description = ''):
        self.comic_id = self.set_id()
        self.title = title
        self.series = series
        self.volume = volume
        self.for_sale = for_sale
        self.quantity = quantity
        self.user_id = user_id
        self.image = self.set_image(image, title)
        self.page_count = page_count
        self.author = author
        self.isbn = isbn
        self.price = price
        self.description = description

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self, image, title):
        if not image:
            image = get_image(title)
        return image
    
    def decrement_quantity(self, quantity):
        self.quantity -= int(quantity)
        return self.quantity
    
    def increment_quantity(self, quantity):
        self.quantity += int(quantity)
        return self.quantity
    
    def change_availablity(self):
        if self.for_sale:
            self.for_sale = False
        else:
            self.for_sale = True
        return self.for_sale
    
    def __repr__(self):
        return f'Comic: {self.series} volume {self.volume}'
    
class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    comic_order = db.relationship('ComicOrder', backref = 'customer', lazy = True)

    def __init__(self, cust_id):
        self.cust_id = cust_id # we are getting their id from the front end


class ComicOrder(db.Model):
    comic_order_id = db.Column(db.String, primary_key = True)
    comic_id = db.Column(db.String, db.ForeignKey('comic.comic_id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(precision = 7, scale = 2), nullable = False)
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable = False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable = False)

    def __init__(self, comic_id, quantity, price, order_id, cust_id):
        self.comic_order_id = self.set_id()
        self.comic_id = comic_id
        self.quantity = quantity
        self.price = self.set_price(price, quantity)
        self.order_id = order_id
        self.cust_id = cust_id

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_price(self, price, quantity):
        quantity = int(quantity)
        price = float(price)

        self.price = quantity * price
        return self.price
    
    def update_quantity(self, quantity):
        self.quantity = int(quantity)
        return self.quantity


class Order(db.Model):
    order_id = db.Column(db.String, primary_key = True)
    order_total = db.Column(db.Numeric(precision = 9, scale = 2), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable = False)
    preorder = db.relationship('ComicOrder', backref = 'order', lazy = True)

    def __init__(self, user_id):
        self.order_id = self.set_id()
        self.order_total = 0.00
        self.user_id = user_id

    def set_id(self):
        return uuid.uuid4()
    
    def increment_order_total(self, price):
        self.order_total = float(self.order_total)
        self.order_total += float(price)

        return self.order_total
    
    def decrement_order_total(self, price):
        self.order_total = float(self.order_total)
        self.order_total -= float(price)

        return self.order_total

    def __repr__(self):
        return f'Order: {self.order_id}'
    

class ComicSchema(ma.Schema):
    class Meta:
        fields = ['comic_id', 'title', 'series', 'volume', 'for_sale', 'quantity', 'user_id', 'image', 'page_count', 'author', 'isbn', 'price', 'description']

comic_schema = ComicSchema()
comic_schemas = ComicSchema(many = True)