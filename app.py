# Import modules and packages
import base64
import numpy as np
import io
from PIL import Image
from keras import backend as K
from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import Flask, render_template, request, jsonify

# Define a Flask app
app= Flask(__name__)

label_dict={0:'Covid-19 Negative', 1:'Covid-19 Positive'}

# Function to load our VGG16 model into memory
def get_model():
    global model
    model = load_model('model/model.h5')
    print('[INFO] MODEL LOADED SUCCESSFULLY')
    
# Funtion to preprocess the supplied image to get it into the format it needs to be in before passing it to our model    
def preprocessing(image, target_size):
	# Check if the image is already in RGB format
	# If it is not it, then converts it to RGB format
    if image.mode != "RGB":
        image = image.convert("RGB")
    # Resize the image to the specified target size 
    image = image.resize(target_size)
    # Convert the image to a numpy array 
    image = img_to_array(image)
    # Expand the dimension of the image
    image = np.expand_dims(image, axis=0)
    # Return the preprocessed version of the image 
    return image

# Load the model
print('[INFO] Loading Keras model ...')
get_model()

# FLASK ROUTES
@app.route('/', methods=['GET'])
def index():
	# Main Page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
	# Get the file from post request
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    # Preprocess the image
    processed_image = preprocessing(image, target_size=(196,196))
    
    # Make prediction
    prediction = model.predict(processed_image)
    output=np.argmax(prediction)
    label=label_dict[output]
     
    # Response to send back to the client with predictions for the original image                 
    response = {
        'prediction' : {
            'result': label
        }
    }
    # Convert Python dictionary into JSON, and return this JSON to the front-end
    return jsonify(response)

if __name__ == '__main__':
	app.run(debug = True)