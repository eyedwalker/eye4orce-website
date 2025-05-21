from flask import Flask, render_template, request, flash, redirect, url_for
from twilio.rest import Client
from dotenv import load_dotenv
import os
from flask_wtf import FlaskForm
from flask_talisman import Talisman
from flask_cors import CORS
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
import re

app = Flask(__name__,
    template_folder='templates',
    static_folder='static'
)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# Load environment variables
load_dotenv()

# Initialize Twilio client
twilio_client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)

# Configure Flask app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize security
Talisman(app)
CORS(app)

# Add security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = """
        default-src 'self';
        script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;
        style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;
        img-src 'self' data:;
        font-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;
        connect-src 'self' https://api.twilio.com;
        frame-src 'self';
    """
    return response

class OptInForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+?[1-9]\d{1,14}$', message='Please enter a valid phone number')
    ], render_kw={"placeholder": "Enter your phone number"})
    submit = SubmitField('Opt In for Updates')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = OptInForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        try:
            # Send A2P compliant welcome message
            message = """
            Welcome to Eye4orce! You'll receive important appointment reminders and updates via SMS.
            
            You'll receive messages about:
            - Appointment confirmations
            - Reminders for upcoming appointments
            - Important updates about your appointments
            
            Message and data rates may apply. Reply STOP to unsubscribe. Reply HELP for help.
            """
            
            # Send welcome message
            twilio_client.messages.create(
                body=message,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                to=phone_number
            )
            
            # Send confirmation message
            confirmation = """
            You have successfully subscribed to Eye4orce appointment reminders!
            
            You'll receive messages about:
            - Appointment confirmations
            - Reminders for upcoming appointments
            - Cancellation instructions
            - Important updates about your appointments
            
            Message and data rates may apply. Reply STOP to unsubscribe. Reply HELP for help.
            """
            
            # Send confirmation message
            twilio_client.messages.create(
                body=confirmation,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                to=phone_number
            )
            
            flash('Thank you for subscribing! You will receive updates via SMS.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('There was an error subscribing. Please try again.', 'error')
    return render_template('index.html', form=form)

@app.route('/webhook', methods=['POST'])
def webhook():
    from_number = request.values.get('From')
    body = request.values.get('Body').lower()
    
    # Handle STOP command
    if body == 'stop':
        response = "You have been unsubscribed from our SMS updates. You will no longer receive messages from us."
    
    # Handle HELP command
    elif body == 'help':
        response = """
        SMS Subscription Options:
        
        - Reply STOP to unsubscribe from all messages
        - Reply HELP to view this help message
        
        You may receive up to 4 messages per month. Message and data rates may apply.
        """
    
    # Handle other messages
    else:
        response = "Thank you for your message! We'll get back to you soon."
    
    # Send response
    twilio_client.messages.create(
        body=response,
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to=from_number
    )
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
