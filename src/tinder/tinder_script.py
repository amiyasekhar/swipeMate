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

# Set the auth token and URL
nearby_profiles_url = 'https://api.gotinder.com/v2/recs/core?locale=en'
like_url = 'https://api.gotinder.com/like/{}?locale=en'
pass_url = 'https://api.gotinder.com/pass/{}?locale=en&s_number={}'

# Path to your service account key
print("We've entered tinder script")
SERVICE_ACCOUNT_KEY = os.getenv('SERVICE_ACCOUNT_KEY')
if (SERVICE_ACCOUNT_KEY):
    print("We have service account key")

# Set the environment variable to tell Google Cloud where to find the credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_KEY

# Google Cloud settings
BUCKET_NAME = 'swipemate-bucket'
MODEL_PATH = 'retrain2pt2.keras'

# Define the local path where the model will be saved
local_model_dir = './downloaded-model'
os.makedirs(local_model_dir, exist_ok=True)  # Create the directory if it doesn't exist
local_model_path = os.path.join(local_model_dir, 'retrain2pt2.keras')
if (local_model_path):
    print(f"Local model path has been set to {local_model_path}")

# Create directories if they don't exist
attractive_dir = './attractive'
unattractive_dir = './unattractive'
os.makedirs(attractive_dir, exist_ok=True)
os.makedirs(unattractive_dir, exist_ok=True)

# Function to download the model from GCS
def download_model_from_gcs(bucket_name, model_path, local_path):
    print("Inside download_model_from_gcs")
    client = storage.Client()  # This will use the GOOGLE_APPLICATION_CREDENTIALS env var
    if client:
        print("We have console client")
    bucket = client.bucket(bucket_name)
    if bucket:
        print("We have bucket")
    blob = bucket.blob(model_path)
    if blob:
        print("We have bucket blob")
    try:
        blob.download_to_filename(local_path)
        print(f"Model downloaded to {local_path}")
    except Exception as e:
        print(f"Failed to download model: {e}")
        exit(1)

# Function to load and preprocess a single image from a URL
def load_and_preprocess_image(image_url):
    print("We are inside load_and_preprocess_image")
    print("image url is {0}".format(image_url))
    response = requests.get(image_url)
    if response.status_code == 200:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir:
            print(f"Script directory: {script_dir}")
        
        # Create a 'temp' directory in the same location as the script
        temp_dir = os.path.join(script_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)

        # Create a unique file name using a hash function
        hash_object = hashlib.md5(image_url.encode())
        print("hash object for encoded image url =", hash_object.hexdigest())
        img_path = os.path.join(temp_dir, hash_object.hexdigest() + ".jpg")
        print(f"Img path: {img_path}")
        
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

    # Download the model if not already present locally
    if not os.path.exists(local_model_path):
        print("Attempting download of model, it's not present locally")
        download_model_from_gcs(BUCKET_NAME, MODEL_PATH, local_model_path)

    # Check if the model was downloaded successfully
    if not os.path.exists(local_model_path):
        print(f"Model file not found at {local_model_path} after download. Exiting.")
        return

    # Load the trained model
    print("Loading model...")
    try:
        model = tf.keras.models.load_model(local_model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Function to get profiles with rate limiting
    def get_profiles_with_rate_limiting(nearby_profiles_url, headers, rate_limit_seconds=random.uniform(3, 5)):
        print("We are inside get_profiles_with_rate_limiting")
        response = requests.get(nearby_profiles_url, headers=headers)
        if response.status_code == 200:
            print("We've got tinder profiles")
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
        print("We are inside like_profile")
        try:
            response = requests.get(like_url.format(user_id), headers=headers)
            if response.status_code == 200:
                print(f"Successfully liked user {user_id}")
            else:
                print(f"Failed to like user {user_id}: {response.status_code}")
        except:
            print(f"Unable to like or dislike user {user_id}")
            return

    # Function to pass on a profile
    def pass_profile(user_id, s_number):
        print("We are inside like_profile")
        try:
            response = requests.get(pass_url.format(user_id, s_number), headers=headers)
            if response.status_code == 200:
                print(f"Successfully passed on user {user_id}")
            else:
                print(f"Failed to pass on user {user_id}: {response.status_code}")
        except:
            print(f"Unable to like or dislike user {user_id}")
            return


    total_users = 0
    profile_limit = 500  # Set the limit to 500 profiles
    right_swipes = 0
    stop_after_limit = True  # Set this to True to stop after reaching the profile limit
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
                # Get the list of results
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
                    swipes_done += 1  # Increment the swipe counter
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
                                    save_path = os.path.join(attractive_dir, f"1_TI_{image_counter}.jpg")
                                else:
                                    save_path = os.path.join(unattractive_dir, f"0_TI_{image_counter}.jpg")
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
                            print(f"We are liking {user_id}")
                            # like_profile(user_id)

                    else:
                        time.sleep(random.uniform(3, 5))
                        print(f"{user_id} is unattractive")
                        print(f"we are disliking {user_id}")
                        # pass_profile(user_id, s_number)

                    # Check if we have reached the swipe limit for this batch
                    if swipes_done >= swipes_in_batch:
                        # Pause for a random duration between 3 and 5 minutes
                        print("Pausing between batches...")
                        time.sleep(random.uniform(180, 300))
                        # Reset swipe counter and set a new random swipe limit for the next batch
                        swipes_done = 0
                        swipes_in_batch = random.randint(10, 15)
                        
                # Pause for a random duration between 3 to 5 seconds
                time.sleep(random.uniform(3, 5))
            else:
                break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tinder_script.py <auth_token>")
        sys.exit(1)

    auth_token = sys.argv[1]
    main(auth_token)
