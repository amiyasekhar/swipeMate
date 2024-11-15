import requests
import time
import random
import os
import hashlib
import tensorflow as tf
import numpy as np
from google.cloud import storage

# Set the auth token and URL
auth_token = 'dff1c8d9-6b71-4c6b-9c64-7bcec9d259aa'
url = 'https://api.gotinder.com/v2/recs/core?locale=en'
like_url = 'https://api.gotinder.com/like/{}?locale=en'
pass_url = 'https://api.gotinder.com/pass/{}?locale=en&s_number={}'
BUCKET_NAME = 'swipemate-bucket'
MODEL_PATH = 'retrain2pt2.keras'

# Set the headers for the request
headers = {
    'X-Auth-Token': auth_token,
    'Content-Type': 'application/json'
}

# Function to download the model from GCS
def download_model_from_gcs(bucket_name, model_path, local_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(model_path)
    try:
        blob.download_to_filename(local_path)
        print(f"Model downloaded to {local_path}")
    except Exception as e:
        print(f"Failed to download model: {e}")
        exit(1)

# Define the local path where the model will be saved
local_model_dir = './downloaded-model'
os.makedirs(local_model_dir, exist_ok=True)  # Create the directory if it doesn't exist
local_model_path = os.path.join(local_model_dir, 'retrain2pt2.keras')

# Download the model if not already present locally
if not os.path.exists(local_model_path):
    download_model_from_gcs(BUCKET_NAME, MODEL_PATH, local_model_path)

# Load the trained model
model = tf.keras.models.load_model(local_model_path)

# Create directories if they don't exist
attractive_dir = './attractive'
unattractive_dir = './unattractive'
os.makedirs(attractive_dir, exist_ok=True)
os.makedirs(unattractive_dir, exist_ok=True)

# Function to load and preprocess a single image from a URL
def load_and_preprocess_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        # Create a unique file name using a hash function
        hash_object = hashlib.md5(image_url.encode())
        img_path = os.path.join("/tmp", hash_object.hexdigest() + ".jpg")
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

# Function to get profiles with rate limiting
def get_profiles_with_rate_limiting(url, headers, rate_limit_seconds=random.uniform(3, 5)):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:  # Too many requests
        print("Rate limit exceeded. Waiting...")
        time.sleep(rate_limit_seconds)
        return get_profiles_with_rate_limiting(url, headers, rate_limit_seconds)
    else:
        print(f"Failed to fetch profiles: {response.status_code}")
        return None

# Function to like a profile
def like_profile(user_id):
    response = requests.get(like_url.format(user_id), headers=headers)
    if response.status_code == 200:
        print(f"Successfully liked user {user_id}")
    else:
        print(f"Failed to like user {user_id}: {response.status_code}")

# Function to pass on a profile
def pass_profile(user_id, s_number):
    response = requests.get(pass_url.format(user_id, s_number), headers=headers)
    if response.status_code == 200:
        print(f"Successfully passed on user {user_id}")
    else:
        print(f"Failed to pass on user {user_id}: {response.status_code}")

total_users = 0
profile_limit = 500  # Set the limit to 100 profiles
right_swipes = 0
stop_after_limit = True  # Set this to True to stop after reaching the profile limit
image_counter = 0  # Count images

# Open the file to write the outputs
with open('profiles.txt', 'a') as file:
    while right_swipes < 500:
        if stop_after_limit and total_users >= profile_limit:
            break

        # Define a random number of swipes for this batch (between 10 and 15)
        swipes_in_batch = random.randint(10, 15)
        swipes_done = 0  # Counter for this batch

        # Make the request to the Tinder API
        data = get_profiles_with_rate_limiting(url, headers)
        
        # Check if data is not None and has results
        if data and 'results' in data['data']:
            results = data['data']['results']
            
            if not results:
                break
            
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
                
                attractive_profile = False
                for photo_url in photo_urls:
                    print(f"Processing image: {photo_url}")
                    img, img_path = load_and_preprocess_image(photo_url)
                    if img is not None:
                        prediction = model.predict(img)
                        confidence = prediction[0][0]
                        label = 'attractive' if confidence > 0.5 else 'unattractive'
                        print(f"Photo is {label} with confidence {confidence}")
                        if confidence > 0.5:
                            attractive_profile = True
                            save_path = os.path.join(attractive_dir, f"1_TI_{image_counter}.jpg")
                        else:
                            save_path = os.path.join(unattractive_dir, f"0_TI_{image_counter}.jpg")
                        print(f"Saving image to: {save_path}")
                        os.rename(img_path, save_path)
                        image_counter += 1
                
                profile_label = 'attractive' if attractive_profile else 'unattractive'
                
                if attractive_profile:
                    time.sleep(random.uniform(3, 5))
                    print(f"{user_id} is attractive")
                    if right_swipes < 500:
                        print("Liking profile (right swipe)")
                        # like_profile(user_id)
                else:
                    time.sleep(random.uniform(3, 5))
                    print(f"{user_id} is unattractive")
                    print("left swipe for now")
                    # pass_profile(user_id, s_number)

                # Check if we have reached the swipe limit for this batch
                if swipes_done >= swipes_in_batch:
                    # Pause for a random duration between 3 and 5 minutes
                    print("Pausing between batches...")
                    time.sleep(random.uniform(180, 300))
                    # Reset swipe counter and set a new random swipe limit for the next batch
                    swipes_done = 0
                    swipes_in_batch = random.randint(10, 15)

            time.sleep(random.uniform(3, 5))  # Short pause between each API request
        else:
            break

# Print the total number of users
print(f"Total number of users: {total_users}")
