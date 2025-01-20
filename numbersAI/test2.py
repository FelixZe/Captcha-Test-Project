import imageio
import matplotlib.pyplot as plt
import numpy as np
import scipy.special
import scipy.ndimage
from PIL import Image

# Neural network class definition
class NeuralNetwork:

    # Initialize the neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # Link weight matrices, wih and who
        self.wih = np.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        # Learning rate
        self.lr = learningrate

        # Activation function (sigmoid)
        self.activation_function = lambda x: scipy.special.expit(x)

    # Load weights from a .npz file
    def load_weights(self, filename):
        data = np.load(filename + ".npz")
        self.wih = data['wih']
        self.who = data['who']

    # Query the network (make a prediction)
    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T

        # Calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        # Calculate signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

# Number of input, hidden, and output nodes
input_nodes = 784
hidden_nodes = 200
output_nodes = 10

# Learning rate
learning_rate = 0.01

# Create an instance of the neural network
n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

# Load previously saved weights
n.load_weights("numbersAI/neuralNetNodes")

# Test the neural network with your own image

# Load an image and preprocess it
image_path = '/Users/stevelang/Documents/Captcha-Test-Project/uploaded_images/canvas_image_2.png'
processed_image = Image.open(image_path).convert('L')

# Convert to numpy array and preprocess
img_array = np.array(processed_image)
print("Image shape:", img_array.shape)  # Should now be (28, 28)

img_data = 255.0 - img_array.reshape(784)  # Invert the image (255 is white)
img_data = (img_data / 255.0 * 0.99) + 0.01  # Scale to range [0.01, 1.0]

# Display the image
plt.imshow(img_data.reshape(28, 28), cmap='Greys', interpolation='None')
#plt.show()

# Query the network with the image data
outputs = n.query(img_data)
print(outputs)

# The index of the highest value corresponds to the predicted label
label = np.argmax(outputs)
print("Network says:", label)
