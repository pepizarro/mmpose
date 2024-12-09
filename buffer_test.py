import sys
import time
import random
import numpy as np
from tools.ring_buffer import RingBuffer

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def producer():

    ring_buffer = RingBuffer(name="inference_buffer", capacity=10, message_size=256, create=True)


    try:
        while True:
            # Simulate inference result as a string
            result = f"Inference result {random.randint(0, 100)}".encode('utf-8')
            result = result.ljust(256, b'\0')  # Pad to fixed size
            success = ring_buffer.write(result)
            if success:
                print(f"Produced: {result.decode('utf-8').strip()}")
            time.sleep(0.5)  # Simulate inference delay
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        ring_buffer.close()


def consumer():

    # Create a figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set up the plot limits (you can adjust based on your data)
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])

    # Line object that will hold the points
    scatter = ax.scatter([], [], [], c='r', marker='o')
    data = np.random.rand(17, 3) * 20 - 10
    scatter._offsets3d = (data[:, 0], data[:, 1], data[:, 2])
    plt.draw()

    def read(ring_buffer):
        try:
            while True:
                # Read a message from the ring buffer
                message = ring_buffer.read()
                if message:
                    message = message.rstrip(b'\0')

                    try:
                        result = np.frombuffer(message, dtype=np.float32).reshape((1, 17, 3))
                        scatter._offsets3d = (result[:, 0], result[:, 1], result[:, 2])
                        plt.draw()
                        print("read succesful")
                    except Exception as e:
                        print("error parsing: ", e)

        except KeyboardInterrupt:
            print("Stopping consumer...")
        finally:
            ring_buffer.close()


    while True:
        try:
            # Attempt to connect to the existing Ring Buffer
            ring_buffer = RingBuffer(name="inference_buffer", capacity=10, message_size=512, create=False)
            print("Successfully connected to the Ring Buffer.")
            read(ring_buffer)
            break  # Exit the loop if successful
        except Exception as e:
            print("Ring Buffer not found, retrying in 1 second...")
            time.sleep(1)  # Wait before retrying




def main():
    if len(sys.argv) < 2:
        print("Usage: python demo.py <produce|consume>")
        return

    mode = sys.argv[1]
    if mode == "produce":
        producer()
    elif mode == "consume":
        consumer()
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python demo.py <produce|consume>")

if __name__ == "__main__":
    main()


