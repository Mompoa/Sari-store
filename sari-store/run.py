import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import Product

# Load environment variables
load_dotenv()

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Product': Product}

if __name__ == '__main__':
    # Create sample products if database is empty
    with app.app_context():
        if Product.query.count() == 0:
            sample_products = [
                Product(
                    name='Wireless Headphones',
                    description='High-quality wireless headphones with noise cancellation. Perfect for music lovers and professionals.',
                    price=1299.99,
                    stock=15,
                    image='headphones.jpg'
                ),
                Product(
                    name='Smart Watch',
                    description='Advanced smartwatch with fitness tracking, heart rate monitor, and 7-day battery life.',
                    price=2499.99,
                    stock=8,
                    image='smartwatch.jpg'
                ),
                Product(
                    name='USB-C Cable',
                    description='Durable USB-C charging cable compatible with all USB-C devices. 2-meter length.',
                    price=299.99,
                    stock=50,
                    image='cable.jpg'
                ),
                Product(
                    name='Phone Case',
                    description='Protective phone case with shockproof design and premium materials. Available in multiple colors.',
                    price=499.99,
                    stock=30,
                    image='case.jpg'
                ),
                Product(
                    name='Screen Protector',
                    description='Tempered glass screen protector with 9H hardness rating. Easy installation with alignment guide.',
                    price=199.99,
                    stock=40,
                    image='protector.jpg'
                ),
                Product(
                    name='Portable Charger',
                    description='20000mAh portable power bank with fast charging support. Charge multiple devices simultaneously.',
                    price=899.99,
                    stock=20,
                    image='charger.jpg'
                ),
                Product(
                    name='Bluetooth Speaker',
                    description='Waterproof Bluetooth speaker with 360-degree sound. Perfect for outdoor activities.',
                    price=1599.99,
                    stock=12,
                    image='speaker.jpg'
                ),
                Product(
                    name='Webcam HD',
                    description='1080p HD webcam with built-in microphone. Ideal for video conferencing and streaming.',
                    price=1199.99,
                    stock=18,
                    image='webcam.jpg'
                ),
            ]
            
            for product in sample_products:
                db.session.add(product)
            
            db.session.commit()
            print("Sample products added to database!")
    
    # Run in debug mode only if FLASK_ENV is not production
    debug_mode = os.getenv('FLASK_ENV', 'development') != 'production'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
