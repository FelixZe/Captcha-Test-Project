from flask import Flask, request, render_template, jsonify
import base64
import numpy as np
import scipy.special
from PIL import Image, ImageOps
import io
import os
import time

# Flask setup
app = Flask(__name__, template_folder="templates")

# Create a unique folder based on timestamp
def create_unique_folder():
    folder_name = f"images/{int(time.time())}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# Neural Network class
class NeuralNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # Weight matrices
        self.wih = np.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        self.lr = learningrate
        self.activation_function = lambda x: scipy.special.expit(x)

    def load_weights(self, filename):
        data = np.load(filename + ".npz")
        self.wih = data['wih']
        self.who = data['who']

    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T
        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        return final_outputs

# Neural Network setup
input_nodes = 784
hidden_nodes = 200
output_nodes = 10
learning_rate = 0.01

n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
n.load_weights("numbersAI/neuralNetNodes")

# Routes
@app.route('/')
def index():
    return render_template("index.html")

UPLOAD_FOLDER = 'uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/verify', methods=['POST'])
def verify():
    try:
        data = request.json
        target = int(data['target'])
        image_data = data['image'].split(",")[1]

        # Decode the Base64 string to an image
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        # Ensure the background is white if the image has transparency
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            white_background = Image.new('RGB', image.size, (255, 255, 255))
            image = Image.alpha_composite(white_background.convert('RGBA'), image.convert('RGBA')).convert('RGB')

        # Resize the image to 28x28
        image = image.resize((28, 28))
        image_path = os.path.join(UPLOAD_FOLDER, 'canvas_image_2.png')
        image.save(image_path, "PNG", quality=95)

        # Process image for the neural network
        image_path = '/Users/stevelang/Documents/Captcha-Test-Project/uploaded_images/canvas_image_2.png'
        processed_image = Image.open(image_path).convert('L')

        # Convert to numpy array and preprocess
        img_array = np.array(processed_image)
        print("Image shape:", img_array.shape)  # Should now be (28, 28)

        img_data = 255.0 - img_array.reshape(784)  # Invert the image (255 is white)
        img_data = (img_data / 255.0 * 0.99) + 0.01  # Scale to range [0.01, 1.0]

        # Query the neural network
        outputs = n.query(img_data)
        label = np.argmax(outputs)  # Predicted digit
        print(label)

        # Return the prediction to the client
        message = "Correct!" if label == target else f"Incorrect! AI guessed {label}."
        return jsonify({"message": message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run server
if __name__ == '__main__':
    app.run(debug=True)
