import numpy as np
import os

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from keras.models import save_model

from sklearn.model_selection import train_test_split

actions = np.array(["left", "right", "up", "down", "r_left", "r_right"])
data = np.load("combined_data.npz")
features = data["features"]
labels = data["labels"]
labels_one_hot = to_categorical(labels).astype(int)

x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)

log_dir = os.path.join("Logs")
tb_callback = TensorBoard(log_dir=log_dir)

shape = features.shape
print(shape)

model = Sequential()
model.add(Dense(64, activation="relu", input_shape=(90,)))
model.add(Dense(32, activation="relu"))
model.add(Dense(6, activation="softmax"))


# Compile the model
model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

# Train the model
history = model.fit(
    x_train,
    y_train,
    epochs=15,
    batch_size=8,
    validation_split=0.1,
    callbacks=[tb_callback],
)

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(x_test, y_test)

print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

model.save("gesture_recognition_model.keras")
