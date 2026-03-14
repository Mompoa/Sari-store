from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from app import db
from app.models import Product, Order, OrderItem
from app.email_service import send_order_confirmation_email
import os
from werkzeug.utils import secure_filename
from functools import wraps

# Create blueprints
main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Raben677')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== MAIN ROUTES (Customer Side) ====================

@main_bp.route('/')
def index():
    """Homepage - Display all products"""
    search_query = request.args.get('search', '')
    
    if search_query:
        products = Product.query.filter(
            Product.name.ilike(f'%{search_query}%') | 
            Product.description.ilike(f'%{search_query}%')
        ).all()
    else:
        products = Product.query.all()
    
    return render_template('index.html', products=products, search_query=search_query)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@main_bp.route('/checkout/<int:product_id>', methods=['GET', 'POST'])
def checkout(product_id):
    """Checkout page"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        # Get form data
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        customer_phone = request.form.get('customer_phone')
        customer_address = request.form.get('customer_address')
        quantity = int(request.form.get('quantity', 1))
        order_notes = request.form.get('order_notes', '')
        
        # Validate quantity
        if quantity <= 0 or quantity > product.stock:
            flash('Invalid quantity', 'error')
            return redirect(url_for('main.checkout', product_id=product_id))
        
        # Calculate total price
        total_price = product.price * quantity
        
        # Create order
        order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_address=customer_address,
            order_notes=order_notes,
            total_price=total_price
        )
        
        # Create order item
        order_item = OrderItem(
            product_id=product_id,
            quantity=quantity,
            price=product.price
        )
        order.items.append(order_item)
        
        # Update stock
        product.stock -= quantity
        
        # Save to database
        db.session.add(order)
        db.session.commit()
        
        # Send email notification
        send_order_confirmation_email(order)
        
        return redirect(url_for('main.order_success', order_id=order.id))
    
    return render_template('checkout.html', product=product)

@main_bp.route('/order-success/<int:order_id>')
def order_success(order_id):
    """Order success page"""
    order = Order.query.get_or_404(order_id)
    return render_template('order_success.html', order=order)

# ==================== ADMIN ROUTES ====================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid password', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard"""
    products_count = Product.query.count()
    orders_count = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    
    return render_template('admin/dashboard.html', 
                         products_count=products_count,
                         orders_count=orders_count,
                         total_revenue=total_revenue)

# ==================== PRODUCT MANAGEMENT ====================

@admin_bp.route('/products')
@admin_required
def products():
    """View all products"""
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    """Add new product"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to make it unique
                import time
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join('app/static/uploads', filename))
                image_filename = filename
        
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image_filename
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/add_product.html')

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    """Edit product"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image if exists
                if product.image:
                    old_path = os.path.join('app/static/uploads', product.image)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                filename = secure_filename(file.filename)
                import time
                filename = f"{int(time.time())}_{filename}"
                file.save(os.path.join('app/static/uploads', filename))
                product.image = filename
        
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/edit_product.html', product=product)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    
    # Delete image if exists
    if product.image:
        image_path = os.path.join('app/static/uploads', product.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.products'))

# ==================== ORDER MANAGEMENT ====================

@admin_bp.route('/orders')
@admin_required
def orders():
    """View all orders"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/orders/delete/<int:order_id>', methods=['POST'])
@admin_required
def delete_order(order_id):
    """Delete order"""
    order = Order.query.get_or_404(order_id)
    
    # Restore product stock
    for item in order.items:
        item.product.stock += item.quantity
    
    db.session.delete(order)
    db.session.commit()
    
    flash('Order deleted successfully!', 'success')
    return redirect(url_for('admin.orders'))
