# sari/store.com - Digital Store Website

A complete Shopee-style e-commerce platform built with Flask, SQLite, and responsive HTML/CSS/JavaScript.

## 📋 Features

### Customer Features
- **Product Browsing**: View all products in a grid layout with images, prices, and descriptions
- **Product Search**: Search products by name or description
- **Product Details**: View detailed product information including full description and stock availability
- **Shopping Cart & Checkout**: Add products to cart and proceed to checkout
- **Order Placement**: Complete order form with customer details and order notes
- **Email Notifications**: Automatic email confirmation sent to admin for each order
- **Responsive Design**: Mobile-friendly interface optimized for all devices

### Admin Features
- **Secure Login**: Password-protected admin panel (Password: `Raben677`)
- **Product Management**:
  - Add new products with images, prices, and descriptions
  - Edit existing products
  - Delete products
  - Manage product stock
  - Upload product images (supports PNG, JPG, JPEG, GIF, WebP)
- **Order Management**:
  - View all customer orders
  - See detailed order information including customer details and items
  - Delete orders
  - Track order history

### Technical Features
- **SQLite Database**: Lightweight, file-based database
- **Email Integration**: SMTP-based email notifications for orders
- **File Upload**: Secure image upload with validation
- **Session Management**: Secure admin authentication
- **Responsive CSS**: Mobile-first design approach
- **Form Validation**: Client and server-side validation

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask 2.3.3
- **Database**: SQLite
- **ORM**: SQLAlchemy via Flask-SQLAlchemy
- **Email**: SMTP (Gmail)
- **Server**: Flask Development Server (can be upgraded to production WSGI)

## 📁 Project Structure

```
sari-store/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models.py                # Database models
│   ├── routes.py                # Application routes
│   ├── email_service.py         # Email functionality
│   ├── templates/
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Homepage
│   │   ├── product_detail.html  # Product detail page
│   │   ├── checkout.html        # Checkout page
│   │   ├── order_success.html   # Order confirmation page
│   │   └── admin/
│   │       ├── base.html        # Admin base template
│   │       ├── login.html       # Admin login
│   │       ├── dashboard.html   # Admin dashboard
│   │       ├── products.html    # Product list
│   │       ├── add_product.html # Add product form
│   │       ├── edit_product.html# Edit product form
│   │       └── orders.html      # Order management
│   └── static/
│       ├── css/
│       │   ├── style.css        # Main stylesheet
│       │   └── admin.css        # Admin stylesheet
│       ├── js/
│       │   ├── main.js          # Main JavaScript
│       │   └── admin.js         # Admin JavaScript
│       └── uploads/             # Product images directory
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or Download the Project

```bash
cd /home/ubuntu/sari-store
```

### Step 2: Install Dependencies

```bash
pip3 install -r requirements.txt
```

Or with sudo if needed:

```bash
sudo pip3 install -r requirements.txt --break-system-packages
```

### Step 3: Configure Email Settings (Optional)

The application is pre-configured with SMTP settings for Gmail. If you want to use different email settings, edit `app/email_service.py`:

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "iglesiaalejandro21@gmail.com"
SENDER_PASSWORD = "sbrc ztlc vbqu dmep"
RECIPIENT_EMAIL = "iglesiaalejandro21@gmail.com"
```

### Step 4: Run the Application

```bash
python3 run.py
```

The application will start on `http://localhost:5000`

### Step 5: Access the Application

- **Store**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Admin Password**: `Raben677`

## 📝 Usage Guide

### For Customers

1. **Browse Products**: Visit the homepage to see all available products
2. **Search Products**: Use the search bar to find specific products
3. **View Details**: Click "View Details" on any product card to see full information
4. **Checkout**: Click "Buy Now" to proceed to checkout
5. **Place Order**: Fill in your details and submit the order
6. **Confirmation**: You'll see an order confirmation page with details

### For Admins

1. **Login**: Navigate to `/admin` and enter the password `Raben677`
2. **Dashboard**: View statistics about products, orders, and revenue
3. **Manage Products**:
   - Click "Products" to view all products
   - Click "Add New Product" to create a new product
   - Click "Edit" to modify a product
   - Click "Delete" to remove a product
4. **Manage Orders**:
   - Click "Orders" to view all customer orders
   - View detailed order information
   - Delete orders if needed

## 🔐 Security Features

- **Password Protection**: Admin panel is protected with a strong password
- **Session Management**: Admin sessions are managed securely
- **File Upload Validation**: Only image files are allowed for product uploads
- **File Size Limits**: Maximum 16MB per upload
- **CSRF Protection**: Forms include security measures
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection

## 📧 Email Configuration

The application automatically sends email notifications when a customer places an order. The email includes:

- Order ID and date
- Customer information (name, email, phone, address)
- Items ordered with prices and quantities
- Total order amount
- Order notes (if provided)

### Email Settings

To change the email configuration, edit `app/email_service.py`:

```python
SMTP_SERVER = "smtp.gmail.com"      # SMTP server address
SMTP_PORT = 587                     # SMTP port
SENDER_EMAIL = "your-email@gmail.com"  # Sender email
SENDER_PASSWORD = "your-app-password"  # App-specific password
RECIPIENT_EMAIL = "admin@example.com"  # Admin email
```

## 🎨 Customization

### Change Store Name

Edit `app/templates/base.html`:
```html
<span class="logo-text">sari/store</span>
```

### Change Colors

Edit `app/static/css/style.css`:
```css
:root {
    --primary-color: #ff6b6b;      /* Main color */
    --secondary-color: #ff8787;    /* Secondary color */
    --dark-color: #2d3436;         /* Dark color */
    /* ... more colors ... */
}
```

### Change Admin Password

Edit `app/routes.py`:
```python
ADMIN_PASSWORD = "Raben677"
```

## 📊 Database Schema

### Products Table
- `id`: Product ID (Primary Key)
- `name`: Product name
- `description`: Product description
- `price`: Product price
- `stock`: Available stock quantity
- `image`: Product image filename
- `created_at`: Creation timestamp

### Orders Table
- `id`: Order ID (Primary Key)
- `customer_name`: Customer name
- `customer_email`: Customer email
- `customer_phone`: Customer phone
- `customer_address`: Delivery address
- `order_notes`: Special instructions
- `total_price`: Order total
- `created_at`: Order timestamp

### Order Items Table
- `id`: Item ID (Primary Key)
- `order_id`: Associated order ID (Foreign Key)
- `product_id`: Associated product ID (Foreign Key)
- `quantity`: Quantity ordered
- `price`: Price at time of order

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use, you can change it in `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Email Not Sending
1. Check SMTP credentials in `app/email_service.py`
2. Ensure "Less secure app access" is enabled for Gmail
3. Check firewall settings for port 587
4. Review Flask logs for error messages

### Images Not Displaying
1. Ensure `app/static/uploads/` directory exists
2. Check file permissions on the uploads folder
3. Verify image filenames in the database

### Database Issues
To reset the database:
```bash
rm app/store.db
python3 run.py  # Will recreate the database with sample products
```

## 🚀 Deployment

For production deployment:

1. **Use a Production WSGI Server**: Replace Flask's development server with Gunicorn or uWSGI
   ```bash
   pip3 install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

2. **Enable HTTPS**: Use SSL certificates for secure connections

3. **Environment Variables**: Store sensitive data in environment variables
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   ```

4. **Database**: Consider using PostgreSQL or MySQL for production

5. **Email Service**: Use a dedicated email service like SendGrid or AWS SES

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Flask documentation: https://flask.palletsprojects.com/
3. Check SQLAlchemy documentation: https://docs.sqlalchemy.org/

## 📄 License

This project is provided as-is for educational and commercial use.

## 🎯 Future Enhancements

- User registration and authentication
- Shopping cart functionality
- Payment gateway integration
- Order tracking system
- Product reviews and ratings
- Inventory management
- Advanced analytics dashboard
- Multi-language support
- Dark mode theme

---

**Version**: 1.0.0  
**Last Updated**: March 13, 2026  
**Author**: sari/store Development Team
