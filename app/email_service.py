import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Get email configuration from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'iglesiaalejandro21@gmail.com')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'sbrc ztlc vbqu dmep')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'iglesiaalejandro21@gmail.com')

def send_order_confirmation_email(order):
    """
    Send order confirmation email to the admin
    """
    try:
        # Create the email message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"New Order #{order.id} - sari/store.com"
        message["From"] = SENDER_EMAIL
        message["To"] = RECIPIENT_EMAIL
        
        # Create HTML email body
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #ff6b6b; color: white; padding: 20px; border-radius: 5px 5px 0 0; }}
                    .content {{ background-color: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
                    .section {{ margin-bottom: 20px; }}
                    .section-title {{ font-weight: bold; font-size: 16px; color: #ff6b6b; margin-bottom: 10px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                    th {{ background-color: #f0f0f0; font-weight: bold; }}
                    .total {{ font-size: 18px; font-weight: bold; color: #ff6b6b; }}
                    .footer {{ background-color: #f0f0f0; padding: 15px; text-align: center; font-size: 12px; color: #666; border-radius: 0 0 5px 5px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>New Order Received</h1>
                        <p>Order ID: #{order.id}</p>
                    </div>
                    
                    <div class="content">
                        <div class="section">
                            <div class="section-title">Customer Information</div>
                            <table>
                                <tr>
                                    <td><strong>Name:</strong></td>
                                    <td>{order.customer_name}</td>
                                </tr>
                                <tr>
                                    <td><strong>Email:</strong></td>
                                    <td>{order.customer_email}</td>
                                </tr>
                                <tr>
                                    <td><strong>Phone:</strong></td>
                                    <td>{order.customer_phone}</td>
                                </tr>
                                <tr>
                                    <td><strong>Address:</strong></td>
                                    <td>{order.customer_address}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div class="section">
                            <div class="section-title">Order Items</div>
                            <table>
                                <thead>
                                    <tr>
                                        <th>Product Name</th>
                                        <th>Price</th>
                                        <th>Quantity</th>
                                        <th>Total</th>
                                    </tr>
                                </thead>
                                <tbody>
        """
        
        for item in order.items:
            html_body += f"""
                                    <tr>
                                        <td>{item.product.name}</td>
                                        <td>₱{item.price:.2f}</td>
                                        <td>{item.quantity}</td>
                                        <td>₱{item.quantity * item.price:.2f}</td>
                                    </tr>
            """
        
        html_body += f"""
                                </tbody>
                            </table>
                        </div>
                        
                        <div class="section">
                            <div class="section-title">Order Summary</div>
                            <table>
                                <tr>
                                    <td><strong>Total Price:</strong></td>
                                    <td class="total">₱{order.total_price:.2f}</td>
                                </tr>
                                <tr>
                                    <td><strong>Order Date:</strong></td>
                                    <td>{order.created_at.strftime('%Y-%m-%d %H:%M:%S')}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div class="section">
                            <div class="section-title">Order Notes</div>
                            <p>{order.order_notes if order.order_notes else 'No notes'}</p>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated email from sari/store.com. Please do not reply to this email.</p>
                        <p>&copy; 2026 sari/store.com. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Attach the HTML content
        part = MIMEText(html_body, "html")
        message.attach(part)
        
        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
        
        print(f"Email sent successfully for order #{order.id}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
