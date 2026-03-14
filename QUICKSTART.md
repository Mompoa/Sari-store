# Quick Start Guide - sari/store.com

Get your online store up and running in 5 minutes!

## ⚡ Quick Setup

### 1. Install Dependencies
```bash
cd /home/ubuntu/sari-store
pip3 install -r requirements.txt
```

### 2. Run the Application
```bash
python3 run.py
```

### 3. Open in Browser
- **Store**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin

## 🔑 Default Credentials

**Admin Password**: `Raben677`

## 📧 Email Configuration

The app is pre-configured to send emails to: `iglesiaalejandro21@gmail.com`

SMTP Settings:
- Server: smtp.gmail.com
- Port: 587
- Email: iglesiaalejandro21@gmail.com
- Password: sbrc ztlc vbqu dmep

## 🛍️ First Steps

### As a Customer:
1. Browse products on the homepage
2. Click "View Details" on any product
3. Click "Buy Now" to checkout
4. Fill in your details and place the order
5. Check your email for confirmation

### As an Admin:
1. Go to http://localhost:5000/admin
2. Enter password: `Raben677`
3. Click "Add New Product" to add products
4. Click "View Orders" to see customer orders

## 📁 Important Files

- `run.py` - Start the application
- `app/routes.py` - All application logic
- `app/models.py` - Database structure
- `app/email_service.py` - Email configuration
- `app/templates/` - HTML pages
- `app/static/css/` - Styling
- `app/static/js/` - JavaScript

## 🔧 Customization

### Change Store Name
Edit `app/templates/base.html` line 18:
```html
<span class="logo-text">Your Store Name</span>
```

### Change Admin Password
Edit `app/routes.py` line 12:
```python
ADMIN_PASSWORD = "your-new-password"
```

### Change Colors
Edit `app/static/css/style.css` lines 5-15:
```css
--primary-color: #your-color;
```

## 🆘 Common Issues

**Port 5000 already in use?**
```bash
python3 run.py  # Change port in run.py
```

**Emails not sending?**
- Check SMTP credentials in `app/email_service.py`
- Enable "Less secure app access" for Gmail

**Database reset?**
```bash
rm app/store.db
python3 run.py  # Recreates with sample products
```

## 📚 Full Documentation

See `README.md` for complete documentation.

---

**Happy Selling! 🎉**
