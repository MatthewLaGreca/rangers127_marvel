from flask import Blueprint, render_template, request, flash, redirect

from haagen_dazs.models import Comic, Order, Customer, db
from haagen_dazs.forms import ComicForm

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def collection():

    collection = Comic.query.filter(Comic.user_id == user_id).all()

    #To do: figure out how to only get the customers of the current user; something like this customers = Customer.query.filter(Customer.comic_order)
    customers = Customer.query.all()
    orders = Order.query.filter(Order.user_id == user_id).all()

    collection_stats = {
        'comics': len(collection),
        'sales': sum([order.order_total for order in orders]),
        'customers': len(customers)
    }
    
    return render_template('collection.html', collection=collection, stats=collection_stats)

@site.route('/collection/add', methods=['GET', 'POST'])
def add():
    
    addform = ComicForm()

    if request.method == 'POST' and addform.validate_on_submit():
        try:
            title = addform.title.data
            author = addform.author.data
            isbn = addform.isbn.data
            page_count = addform.page_count.data
            for_sale = addform.for_sale.data
            price = addform.price.data
            quantity = addform.quantity.data
            volume = addform.volume.data
            series = addform.series.data
            image = addform.image.data
            description = addform.description.data

            collection = Comic(title, series, volume, for_sale, quantity, image, page_count, author, isbn, price, description)

            db.session.add(collection)
            db.session.commit()

            flash(f'You have successfully added {title}!', category='success')
            return redirect('/')
        
        except:
            flash('We were unable to process your request.  Please try again', category='warning')
            return redirect('/collection/add')
        
    return render_template('add.html', form=addform)

@site.route('/<user_id>/collection/update/<id>', methods=['GET','POST'])
def update(id):

    updateform = ComicForm()
    comic = Comic.query.get(id)

    if request.method == 'POST' and updateform.validate_on_submit():

        try:
            comic.title = updateform.title.data
            comic.author = updateform.author.data
            comic.isbn = updateform.isbn.data
            comic.page_count = updateform.page_count.data
            comic.for_sale = updateform.for_sale.data
            comic.price = updateform.price.data
            comic.quantity = updateform.quantity.data
            comic.volume = updateform.volume.data
            comic.series = updateform.series.data
            comic.image = updateform.image.data
            comic.description = updateform.description.data

            db.session.commit()

            flash(f'You have successfully updated {comic.title}!', category='success')
            return redirect('/')
        
        except:
            flash('We were unable to process your request.  Please try again', category='warning')
            return redirect(f'/collection/add')
    return render_template('update.html', form=updateform, comic=comic)

@site.route('/collection/delete/<id>')
def delete(id):

    comic = Comic.query.get(id)
    db.session.delete(comic)
    db.session.commit()

    return redirect('/')