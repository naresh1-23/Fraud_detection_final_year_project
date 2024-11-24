import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


class LogisticRegression:
    def __init__(self, weights=None, bias=None, learning_rate=0.01, num_iterations=1000):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = weights
        self.bias = bias
        self.losses = []  # To store loss values for plotting

    def sigmoid(self, z):
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def loss_function(self, y_true, y_pred):
        """Binary cross-entropy loss function."""
        return -np.mean(y_true * np.log(y_pred + 1e-10) + (1 - y_true) * np.log(1 - y_pred + 1e-10))

    def fit(self, X, y):
        print(self.learning_rate)
        num_samples, num_features = X.shape
        self.weights = np.zeros(num_features)
        self.bias = 0

        for _ in range(self.num_iterations):
            linear_model = np.dot(X, self.weights) + self.bias
            y_predicted = self.sigmoid(linear_model)

            # Calculate and store loss for plotting
            loss = self.loss_function(y, y_predicted)
            self.losses.append(loss)

            dw = (1 / num_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / num_samples) * np.sum(y_predicted - y)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        y_predicted = self.sigmoid(linear_model)
        y_predicted_class = [1 if i > 0.5 else 0 for i in y_predicted]
        return np.array(y_predicted_class)

    def calculate_accuracy(self, y_true, y_pred):
        correct_predictions = np.sum(y_true == y_pred)
        accuracy = correct_predictions / len(y_true)
        return accuracy

    def plot_loss(self, filename='loss_plot.png'):
        """Plot the loss over iterations and save it as an image."""
        plt.figure(figsize=(10, 6))
        plt.plot(range(self.num_iterations), self.losses, label='Loss', color='blue')
        plt.title('Loss Over Iterations')
        plt.xlabel('Iterations')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid()
        plt.savefig(filename)
        plt.close()  # Close the figure to free up memory

    def plot_confusion_matrix(self, y_true, y_pred, filename='confusion_matrix.png'):
        """Plot confusion matrix and save it as an image."""
        cm = confusion_matrix(y_true, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap=plt.cm.Blues)
        plt.title('Confusion Matrix')
        plt.savefig(filename)
        plt.close()
