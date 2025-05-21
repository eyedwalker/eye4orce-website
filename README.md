# Eye4orce - Premium Eyewear Website

A modern, responsive website for Eye4orce eyewear featuring Twilio messaging integration.

## Features

- Modern, responsive design using Bootstrap 5
- Premium eyewear collections showcase
- Featured products section
- Twilio-powered SMS opt-in/opt-out system
- Beautiful card-based layout
- Mobile-friendly design
- A2P SMS compliant messaging system

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your Twilio credentials:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
SECRET_KEY=your_flask_secret_key
```

3. Run the application locally:
```bash
python app.py
```

4. Visit `http://localhost:5000` in your browser

## Deployment Instructions

1. Create a requirements.txt file with all dependencies
2. Create a Procfile with: `web: gunicorn app:app`
3. Set up environment variables in your deployment platform
4. Deploy using your preferred platform (Heroku, Vercel, etc.)
5. Configure Twilio webhook URLs in your environment variables

## Project Structure

- `/static` - Contains CSS, JavaScript, and image files
- `/templates` - Contains HTML templates
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file)

## Twilio Integration

The website includes an A2P SMS opt-in/opt-out system that allows customers to subscribe for updates via SMS. When a customer submits their phone number, they will be added to your Twilio messaging list. Customers can:

- Reply STOP to unsubscribe at any time
- Reply HELP to get help with managing their subscription
- Receive up to 4 messages per month

The system is fully A2P compliant and includes proper opt-in/opt-out messaging.

## Customization

To customize the website:
1. Update the images in `/static/images`
2. Modify the color scheme in `static/css/style.css`
3. Update the content in `templates/index.html`
4. Add your social media links in the footer

## License

MIT License
