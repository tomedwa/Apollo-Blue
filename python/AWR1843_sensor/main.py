import threading
import time
import read_sensor


# Define a function that will run in the first thread
def thread_function1():
    read_sensor.sensor_main_loop()


# Define a function that will run in the second thread
def thread_function2():
    while True:
        print("balls")
        # UART SHIT HERE
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        # Create the first thread as a daemon
        thread1 = threading.Thread(target=thread_function1, daemon=True)
        # Create the second thread as a daemon
        thread2 = threading.Thread(target=thread_function2, daemon=True)

        # Start both threads
        thread1.start()
        thread2.start()

        # Keep the main thread running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting...")

    print("Main file execution finished")
