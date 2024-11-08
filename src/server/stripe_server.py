import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin # import CORS 
import stripe
import subprocess  # Add this import
import json
from dotenv import load_dotenv  # Import load_dotenv

app = Flask(__name__)
CORS(app, origins=["https://swipemate.ai"], methods=["GET", "POST", "OPTIONS"])

load_dotenv()
print()
# print("Correct env path: ", "/Users/amiyasekhar/Downloads/swipeMate/.env")
# print("API KEY: ", os.getenv('STRIPE_API_KEY'))
# print("WHSEC: ", os.getenv('WEBHOOK_SECRET'))

# Set your secret key. Remember to replace this with your actual secret key.
# stripe.api_key = "sk_test_51MIxt5KhH8zNT0eB8iLQwqDCpcFhhjQJhUHhc7YF99YfdgsfZ58FayYJwPTvtTokk195NMPVEpZ3rk56CsfrbzBi00SBkjyRrE"
# webhook_endpoint_secret = "whsec_LG3tvZ1TnYUc9MpF2f9HFPR0n0Z94uOu"
stripe.api_key = os.getenv('STRIPE_API_KEY')
# print(f"Loaded Stripe API Key: {stripe.api_key}")  # Debugging line
webhook_endpoint_secret = os.getenv('WEBHOOK_SECRET')
# print(f"Loaded Webhook Secret: {webhook_endpoint_secret}")  # Debugging line

# Determine the base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/create-checkout-session', methods=['POST'])
@cross_origin(origins='https://swipemate.ai')
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
                        'unit_amount': 100,  # Amount in cents
                    },
                    'quantity': 1,
                },
            ],
            automatic_tax={'enabled': True},
            mode='payment',
            client_reference_id=auth_token,  # Set the auth token here
            success_url=f'https://swipemate.ai/checkout-success?authToken={auth_token}',
            #success_url=f'http://localhost:3000/checkout-success?authToken={auth_token}',
            cancel_url='https://your-website.com/cancel',
        )
        print(f"Created Stripe Checkout Session: {session.id}")
        return jsonify({'id': session.id})
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return jsonify(error=str(e)), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    print("webook triggered")
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_endpoint_secret  # Use the correct variable here
        )
    except ValueError as e:
        # Invalid payload
        print(f"Invalid payload: {e}")
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"Invalid signature: {e}")
        return jsonify(success=False), 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        auth_token = session.get('client_reference_id')  # Fetch the auth token
        
        if auth_token:
            # Construct the relative path to the Tinder script
            tinder_script_path = os.path.join(BASE_DIR, '../tinder/tinder_script2.py')
            print(f"Tinder script path: {tinder_script_path}")

            # Normalize the path (optional, for cross-platform compatibility)
            tinder_script_path = os.path.normpath(tinder_script_path)
            print(f"Normalised tinder script path: {tinder_script_path}")

            # Run Tinder script with the constructed relative path and auth token
            print('Payment was successful! Now we can run the Tinder scripts')
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
