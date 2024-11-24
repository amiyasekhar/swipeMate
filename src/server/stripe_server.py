import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin # import CORS 
import stripe
import subprocess  # Add this import
import json
from dotenv import load_dotenv  # Import load_dotenv
from monitor_requests import start_browser_with_debugging, monitor_chrome_requests

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://swipemate.ai"], methods=["GET", "POST", "OPTIONS"], supports_credentials=True)

load_dotenv()
stripe.api_key = os.getenv('STRIPE_API_KEY')

if stripe.api_key:
    print("Loaded Stripe API Key")  # Debugging line

webhook_endpoint_secret = os.getenv('WEBHOOK_SECRET')
if webhook_endpoint_secret:
    print("Loaded Stripe Webhook Endpoint Secret")  # Debugging line

webhook_endpoint_secret_backup = os.getenv('WEBHOOK_SECRET_BACKUP')
if webhook_endpoint_secret_backup:
    print("Loaded Stripe Webhook Endpoint Secret Backup")  # Debugging line

# Determine the base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR:
    print("Loaded BASE_DIR")  # Debugging line


@app.route('/create-checkout-session', methods=['POST'])
@cross_origin(origins=["https://swipemate.ai", "http://localhost:3000", "http://127.0.0.1:3000"])
def create_checkout_session():
    data = json.loads(request.data)
    auth_token = data.get('authToken')

    try:
        # Create a new checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'SwipeMate AI',
                        },
                        'unit_amount': 5000,  # Amount in cents
                    },
                    'quantity': 1,
                },
            ],
            automatic_tax={'enabled': True},
            mode='payment',
            allow_promotion_codes=True,
            client_reference_id=auth_token,  # Set the auth token here
            success_url=f'https://swipemate.ai/checkout-success?authToken={auth_token}',
            #success_url=f'http://localhost:3000/checkout-success?authToken={auth_token}',
            cancel_url='https://swipemate.ai/checkout-success',
        )
        print(f"Created Stripe Checkout Session: {session.id}")
        print(f"Stripe Checkout url: {session.url}")
        print("server session data:", session)
        return jsonify({'id': session.id, 'url': session.url})
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return jsonify(error=str(e)), 500
    
@app.route('/tinder-login', methods=['GET'])
def tinder_login():
    try:
        start_browser_with_debugging('chrome')  # Start Chrome with debugging
        return jsonify({"message": "Chrome started in debugging mode"}), 200
    except Exception as e:
        print(f"Error in /tinder-login: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/retrieve-auth-token', methods=['GET'])
def retrieve_auth_token():
    try:
        # Call the monitor_chrome_requests function to start monitoring
        x_auth_token = monitor_chrome_requests()
        
        # Check if the token was successfully retrieved
        if x_auth_token:
            return jsonify({"token": x_auth_token}), 200
        else:
            return jsonify({"error": "X-Auth-Token not found. Please ensure you are logged in to Tinder and try again."}), 404
    except Exception as e:
        print(f"Error in /retrieve-auth-token: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    print("webook triggered")
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try: # Verify with normal webhook secret first
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_endpoint_secret  # Normal secret
        )
        print("Event verified using main webhook secret")
    except stripe.error.SignatureVerificationError as e: # Normal secret didn't work
        # Invalid signature
        print(f"Error {e}. Invalid signature with main secret, trying backup secret")
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_endpoint_secret_backup # Backup secret
            )
            print("Event verified using backup webhook secret")
        except stripe.error.SignatureVerificationError as e:
            print(f"Invalid signature with both secrets: {e}")
            return jsonify(success=False), 400

        except ValueError as e:
            # Invalid payload with backup secret
            print(f"Invalid payload with backup secret: {e}")
            return jsonify(success=False), 400
    except ValueError as e:
        # Invalid payload with main secret
        print(f"Invalid payload with normal secret: {e}")
        return jsonify(success=False), 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print('Payment was successful! Now we can run the Tinder scripts')
        auth_token = session.get('client_reference_id')  # Fetch the auth token
        
        if auth_token:
            print(f"We have auth token: {auth_token}")
            # Construct the relative path to the Tinder script
            tinder_script_path = os.path.join(BASE_DIR, '../tinder/tinder_script.py')
            print(f"Tinder script path: {tinder_script_path}")

            # Normalize the path (optional, for cross-platform compatibility)
            tinder_script_path = os.path.normpath(tinder_script_path)
            print(f"Normalised tinder script path: {tinder_script_path}")

            # Run Tinder script with the constructed relative path and auth token
            print("tinder script should run here")
            subprocess.run(["python3", tinder_script_path, auth_token])
            
            '''
            print('Payment was successful! Now we can run the Tinder scripts')
            subprocess.run(["C:\\Program Files\\Python310\\python.exe", tinder_script_path, auth_token])
            '''
        else:
            print("No Auth Token")
        
        
    else:
        print(f'Unhandled event type {event["type"]}')

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3002)))
    #app.run(port=3002, host='0.0.0.0')
