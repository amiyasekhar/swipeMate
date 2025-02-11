import requests
import time
import random
import os
import hashlib
import tensorflow as tf
import numpy as np
from google.cloud import storage
import sys
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()

# Set the auth token and URL endpoints for Tinder API
nearby_profiles_url = 'https://api.gotinder.com/v2/recs/core?locale=en'
like_url = 'https://api.gotinder.com/like/{}?locale=en'
pass_url = 'https://api.gotinder.com/pass/{}?locale=en&s_number={}'

# Path to your service account key
print("We've entered tinder script")
SERVICE_ACCOUNT_KEY = os.getenv('SERVICE_ACCOUNT_KEY')
if SERVICE_ACCOUNT_KEY:
    print("We have service account key")

# Set the environment variable to tell Google Cloud where to find the credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_KEY

# Google Cloud settings
BUCKET_NAME = 'swipemate-bucket'
MODEL_PATH = 'retrain2pt2.keras'

# Build the GCS URI for the model and test connectivity
GCS_URI = f"gs://{BUCKET_NAME}/{MODEL_PATH}"
print("Attempting to load model directly from GCS URI:", GCS_URI)

# Create directories for saving classified images
# attractive_dir = './attractive'
# unattractive_dir = './unattractive'
# os.makedirs(attractive_dir, exist_ok=True)
# os.makedirs(unattractive_dir, exist_ok=True)

# Function to load and preprocess a single image from a URL
def load_and_preprocess_image(image_url):
    print("Inside load_and_preprocess_image")
    print("Image URL is: {0}".format(image_url))
    response = requests.get(image_url)
    if response.status_code == 200:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Script directory: {script_dir}")
        
        # Create a 'temp' directory in the same location as the script
        temp_dir = os.path.join(script_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)

        # Create a unique file name using a hash of the image URL
        hash_object = hashlib.md5(image_url.encode())
        print("Hash for encoded image URL =", hash_object.hexdigest())
        img_path = os.path.join(temp_dir, hash_object.hexdigest() + ".jpg")
        print(f"Image path: {img_path}")
        
        with open(img_path, 'wb') as img_file:
            img_file.write(response.content)
            
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=(299, 299))
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img /= 255.0
        return img, img_path
    else:
        print(f"Failed to download image: {image_url}")
        return None, None


def main(auth_token):
    # Set the headers for the request
    headers = {
        'X-Auth-Token': auth_token,
        'Content-Type': 'application/json'
    }

    # Attempt to load the model directly from the GCS URI
    print("Loading model directly from GCS...")
    try:
        model = tf.keras.models.load_model(GCS_URI)
        print("Model loaded successfully from GCS!")
    except Exception as e:
        print(f"Failed to load model from GCS: {e}")
        return

    # Function to get Tinder profiles with rate limiting
    def get_profiles_with_rate_limiting(nearby_profiles_url, headers, rate_limit_seconds=random.uniform(3, 5)):
        print("Inside get_profiles_with_rate_limiting")
        response = requests.get(nearby_profiles_url, headers=headers)
        if response.status_code == 200:
            print("We've got Tinder profiles")
            return response.json()
        elif response.status_code == 429:  # Too many requests
            print("Rate limit exceeded. Waiting...")
            time.sleep(rate_limit_seconds)
            return get_profiles_with_rate_limiting(nearby_profiles_url, headers, rate_limit_seconds)
        else:
            print(f"Failed to fetch profiles: {response.status_code}")
            return None

    # Function to like a profile
    def like_profile(user_id):
        print("Inside like_profile")
        try:
            response = requests.get(like_url.format(user_id), headers=headers)
            if response.status_code == 200:
                print(f"Successfully liked user {user_id}")
            else:
                print(f"Failed to like user {user_id}: {response.status_code}")
        except Exception as e:
            print(f"Unable to like user {user_id}: {e}")
            return

    # Function to pass on a profile
    def pass_profile(user_id, s_number):
        print("Inside pass_profile")
        try:
            response = requests.get(pass_url.format(user_id, s_number), headers=headers)
            if response.status_code == 200:
                print(f"Successfully passed on user {user_id}")
            else:
                print(f"Failed to pass on user {user_id}: {response.status_code}")
        except Exception as e:
            print(f"Unable to pass on user {user_id}: {e}")
            return

    total_users = 0
    profile_limit = 500  # Limit to 500 profiles
    right_swipes = 0
    stop_after_limit = True  # Stop after reaching the profile limit
    image_counter = 0  # Count images

    # Open the file to write the outputs
    with open('profiles.txt', 'w') as file:
        while right_swipes < 500:
            if stop_after_limit and total_users >= profile_limit:
                break

            # Define a random number of swipes for this batch (between 10 and 15)
            swipes_in_batch = random.randint(10, 15)
            swipes_done = 0  # Counter for this batch

            # Make the request to the Tinder API
            data = get_profiles_with_rate_limiting(nearby_profiles_url, headers)
            
            # Check if data is not None and has results
            if data and 'results' in data['data']:
                print("We've got nearby profiles")
                results = data['data']['results']
                
                # Check if results are empty
                if not results:
                    print("We have empty profiles")
                    break
                
                # Iterate over each user in the response
                for result in results:
                    if stop_after_limit and total_users >= profile_limit:
                        break

                    total_users += 1
                    swipes_done += 1
                    user = result['user']
                    s_number = result['s_number']
                    user_id = user['_id']
                    user_name = user['name']
                    photo_urls = [photo['url'] for photo in user['photos']]
                    
                    # Write user details to the file
                    file.write(f"Profile {total_users}\n")
                    file.write(f"Name: {user_name}\n")
                    file.write(f"User ID: {user_id}\n")
                    file.write(f"S Number: {s_number}\n")
                    attractive_profile = False
                    
                    for photo_url in photo_urls:
                        file.write(f"Photo URL: {photo_url}\n")
                        img, img_path = load_and_preprocess_image(photo_url)
                        if img is not None:
                            try:
                                prediction = model.predict(img)
                                confidence = prediction[0][0]
                                label = 'attractive' if confidence > 0.7 else 'unattractive'
                                file.write(f"Photo is {label} with confidence {confidence}\n")
                                if confidence > 0.7:
                                    attractive_profile = True
                                    # save_path = os.path.join(attractive_dir, f"1_TI_{image_counter}.jpg")
                                else:
                                    # save_path = os.path.join(unattractive_dir, f"0_TI_{image_counter}.jpg")
                                print(f"Saving image to: {save_path}")
                                os.rename(img_path, save_path)
                                image_counter += 1
                            except Exception as e:
                                print(f"Failed to predict image: {e}")
                    
                    profile_label = 'attractive' if attractive_profile else 'unattractive'
                    file.write(f"Profile is {profile_label}\n")
                    file.write("\n")
                    
                    # Like or pass on the profile based on the attractiveness
                    if attractive_profile:
                        time.sleep(random.uniform(3, 5))
                        print(f"{user_id} is attractive")
                        if right_swipes < 500:
                            print(f"Liking user {user_id}")
                            like_profile(user_id)
                    else:
                        time.sleep(random.uniform(3, 5))
                        print(f"{user_id} is unattractive")
                        print(f"Passing on user {user_id}")
                        pass_profile(user_id, s_number)

                    # Pause between batches if needed
                    if swipes_done >= swipes_in_batch:
                        print("Pausing between batches...")
                        time.sleep(random.uniform(180, 300))
                        swipes_done = 0
                        swipes_in_batch = random.randint(10, 15)
                        
                time.sleep(random.uniform(3, 5))
            else:
                break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tinder_script.py <auth_token>")
        sys.exit(1)

    auth_token = sys.argv[1]
    main(auth_token)