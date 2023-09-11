from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required

from haagen_dazs.models import Customer, Comic, ComicOrder, Order, db, comic_schema, comic_schemas

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/token', methods = ['GET', 'POST'])
def token():

    data = request.json

    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client Id.  Try Again'
        }
    
@api.route('/order/<cust_id>')
@jwt_required()
def get_order(cust_id):

    comic_order = ComicOrder.query.filter(ComicOrder.cust_id == cust_id).all()

    data = []

    for order in comic_order:

        comic = Comic.query.filter(Comic.comic_id == order.comic_id).first()

        comic_data = comic_schema.dump(comic)
        comic_data['quantity'] = order.quantity
        comic_data['order_id'] = order.order_id
        comic_data['id'] = order.comic_order_id

        data.append(comic_data)
    
    return jsonify(data)


@api.route('/order/create/<cust_id>', methods = ['POST'])
@jwt_required()
def create_order(cust_id):

    data = request.json

    customer_order = data['order']

    customer = Customer.query.filter(Customer.cust_id == cust_id).first()
    if not customer:
        customer = Customer(cust_id)
        db.session.add(customer)

    order = Order()
    db.session.add(order)

    for comic in customer_order:

        comic_order = ComicOrder(comic['comic_id'], comic['quantity'], comic['price'], order.order_id, customer.cust_id)
        db.session.add(comic_order)

        order.increment_order_total(comic_order.price)

        current_comic = Comic.query.filter(Comic.comic_id == comic['comic_id']).first()
        current_comic.decrement_quantity(comic['quantity'])

    db.session.commit()

    return {
        'status': 200,
        'message': 'New Order was created!'
    }



@api.route('/order/update/<order_id>', methods=['PUT', 'POST'])
@jwt_required()
def update_order(order_id):
    try:

        data = request.json
        new_quantity = int(data['quantity'])
        comic_id = data['comic_id']

        comic_order = ComicOrder.query.filter(ComicOrder.order_id == order_id, ComicOrder.comic_id == comic_id).first()
        order = Order.query.get(order_id)
        comic = Comic.query.get(comic_id)

        comic_order.set_price(comic.price, new_quantity)

        diff = abs(comic_order.quantity - new_quantity)

        if comic_order.quantity < new_quantity:
            comic.decrement_quantity(diff) #decrease our available inventory
            order.increment_order_total(comic_order.price) #our order total is going to be more
        
        elif comic_order.quantity > new_quantity:
            comic.increment_quantity(diff) #increase our available inventory
            order.decrement_order_total(comic_order.price) #our order total is going to be less

        comic_order.update_quantity(new_quantity)

        db.session.commit()

        return {
            'status': 200,
            'message': 'Order was successfully updated!'
        }
    
    except:

        return {
            'status': 400,
            'message': 'Unable to process your request.  Please try again'
        }
    
@api.route('/order/delete/<order_id>', methods=['DELETE'])
@jwt_required()
def delete_item_order(order_id):

    data = request.json
    comic_id = data['comic_id']

    comic_order = ComicOrder.query.filter(ComicOrder.order_id == order_id, ComicOrder.comic_id == comic_id).first()

    order = Order.query.get(order_id)
    comic = Comic.query.get(comic_id)

    order.decrement_order_total(comic_order.price)
    comic.increment_quantity(comic_order.quantity)

    db.session.delete(comic_order)
    db.session.commit()

    return {
        'status': 200,
        'message': 'Order was successfully deleted!'
    }