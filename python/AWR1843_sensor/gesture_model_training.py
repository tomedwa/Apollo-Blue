import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split

# Load data
data = np.load("combined_data.npz")
features = data["features"]
labels = data["labels"]

features = features.reshape(features.shape[0], 1, features.shape[1])

x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)

# Define model
model = Sequential()
model.add(LSTM(64, input_shape=(x_train.shape[1], x_train.shape[2])))
model.add(Dense(32, activation="relu"))
model.add(Dense(4, activation="softmax"))

# Compile the model
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

# Callbacks
log_dir = os.path.join("Logs")
tb_callback = TensorBoard(log_dir=log_dir)

# Train the model
history = model.fit(
    x_train,
    y_train,
    epochs=30,
    batch_size=8,
    validation_split=0.1,
    callbacks=[tb_callback],
)

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(x_test, y_test)

print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

# Save the model
model.save("gesture_recognition_model.h5")
