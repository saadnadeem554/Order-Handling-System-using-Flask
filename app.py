from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sqlalchemy import func

app = Flask(__name__)
# using SQLite database because it is easy and lightweight
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Add a secret key for flash messages
app.config['SECRET_KEY'] = '1234567890abcdef'
db = SQLAlchemy(app)

# Table for storing order information like Order ID (unique), Number of items, Delivery date, Sender name, Recipient name, Recipient address, Status (default: "Ongoing")
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.Integer, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    recipient_address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Ongoing')

# Log table for loging every action
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # Unique ID
    type = db.Column(db.String(50), nullable=False)
    performer = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create database directory if it doesn't exist
if not os.path.exists('instance'):
    os.makedirs('instance')

# Check if database already exists
db_path = 'instance/database.db'
db_exists = os.path.exists(db_path)

# Create all database tables
if not db_exists:
    with app.app_context():
        db.create_all()

@app.route('/')
@app.route('/index')
@app.route('/view_orders')
def view_orders():
    orders = Order.query.all()
    return render_template('view_orders.html', orders=orders)

# View logs
@app.route('/logs')
def view_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template('logs.html', logs=logs)

# User Functions.
# Function to log actions
def log_action(action_type, performer_name):
    log_entry = Log(type=action_type, performer=performer_name)
    db.session.add(log_entry)
    db.session.commit()
    
# Route to display the add order form
@app.route('/add_order', methods=['GET'])
def show_add_order_form():
    return render_template('add_order.html')

# Add a new order
@app.route('/add_order', methods=['POST'])
def add_order():
    if request.method == 'POST':
        # get values from the form to fill the table in database
        if not request.form['items'] or not request.form['delivery_date'] or not request.form['sender_name'] or not request.form['recipient_name'] or not request.form['recipient_address']:
            flash('All fields are required!', 'error')
            return redirect(url_for('show_add_order_form'))
        
        items = request.form['items']
        delivery_date = request.form['delivery_date']
        sender_name = request.form['sender_name']
        recipient_name = request.form['recipient_name']
        recipient_address = request.form['recipient_address']
        
        # Check if order should be marked as completed immediately
        status = 'Completed' if 'mark_completed' in request.form else 'Ongoing'
        
        # check for exact duplicates
        existing_order = Order.query.filter_by(
            items=items,
            delivery_date=datetime.strptime(delivery_date, '%Y-%m-%d').date(),
            sender_name=sender_name,
            recipient_name=recipient_name,
            recipient_address=recipient_address
        ).first()
        if existing_order:
            flash('This order already exists!', 'error')
            return redirect(url_for('show_add_order_form'))

        new_order = Order(
            items=items,
            delivery_date=datetime.strptime(delivery_date, '%Y-%m-%d').date(),
            sender_name=sender_name,
            recipient_name=recipient_name,
            recipient_address=recipient_address,
            status=status
        )
        
        db.session.add(new_order)
        db.session.commit()

        # Get performer name for logging
        performer_name = request.form.get('performer_name', sender_name)
        
        # Log the action with appropriate message
        action_type = 'Add Order (Completed)' if status == 'Completed' else 'Add Order'
        log_action(action_type, performer_name)

        flash('Order added successfully!', 'success')
        return redirect(url_for('view_orders'))
    
# Display form to edit an order    
@app.route('/edit_order/<int:order_id>', methods=['GET'])
def show_edit_form(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('edit_order.html', order=order)
    
# Delete an order
@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()

    # Log the action
    performer_name = request.form.get('performer_name', 'Unknown')
    log_action('Delete Order', performer_name)

    flash('Order deleted successfully!', 'success')
    return redirect(url_for('view_orders'))

# Edit an order
@app.route('/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    if request.method == 'POST':
        # get values from the form to fill the table in database
        if not request.form['items'] or not request.form['delivery_date'] or not request.form['sender_name'] or not request.form['recipient_name'] or not request.form['recipient_address']:       # validation check!
            flash('All fields are required!', 'error')
            return redirect(url_for('view_orders'))
        
        order.items = request.form['items']
        order.delivery_date = datetime.strptime(request.form['delivery_date'], '%Y-%m-%d').date()
        order.sender_name = request.form['sender_name']
        order.recipient_name = request.form['recipient_name']
        order.recipient_address = request.form['recipient_address']
        
        db.session.commit()

        # Log the action
        performer_name = request.form.get('performer_name', 'Unknown')
        log_action('Update Order', performer_name)

        flash('Order updated successfully!', 'success')
        return redirect(url_for('view_orders'))
  
# Mark an order as completed  
@app.route('/Mark Order as Completed/<int:order_id>', methods=['POST'])
def mark_order_completed(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'Completed'
    db.session.commit()

    # Log the action
    performer_name = request.form.get('performer_name', 'Unknown')
    log_action('Mark Order as Completed', performer_name)

    flash('Order marked as completed!', 'success')
    return redirect(url_for('view_orders'))

if __name__ == '__main__':
    app.run(debug=True)