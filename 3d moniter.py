import serial
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Global variables
serial_port = None
serial_angle = ""
serial_distance = ""
serial_data = ""
object_distance = 0
radar_angle = 0
radar_distance = 0
index = 0

# Initialize the serial port
def init_serial():
    global serial_port
    try:
        serial_port = serial.Serial('COM12', 115200, timeout=1)
        serial_port.flush()
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        exit()

# Read and process serial data
def read_serial_data():
    global serial_data, serial_angle, serial_distance, radar_angle, radar_distance, index

    if serial_port.in_waiting > 0:
        serial_data = serial_port.readline().decode('utf-8').strip()
        if '#' in serial_data:
            serial_data = serial_data.replace('#', '')
            index = serial_data.index('*')

            serial_angle = serial_data[:index]
            serial_distance = serial_data[index+1:]

            radar_angle = int(serial_angle)
            radar_distance = int(serial_distance)

# Initialize the plot
fig, ax = plt.subplots()
ax.set_xlim(-640, 640)
ax.set_ylim(-640, 0)
ax.set_aspect('equal')
ax.axis('off')

# Draw radar arcs and lines
def draw_radar():
    arcs = [1200, 934, 666, 400]
    for arc in arcs:
        circle = patches.Arc((0, 0), arc, arc, angle=0, theta1=180, theta2=360, color='green', linewidth=2)
        ax.add_patch(circle)
    lines = [
        ((-640, 0), (640, 0)),
        ((0, 0), (-554, -320)),
        ((0, 0), (-320, -554)),
        ((0, 0), (0, -640)),
        ((0, 0), (320, -554)),
        ((0, 0), (554, -320))
    ]
    for line in lines:
        ax.plot(*zip(*line), color='green', linewidth=2)

# Update the plot with new data
def update(frame):
    global radar_angle, radar_distance, object_distance

    read_serial_data()
    ax.cla()
    draw_radar()

    # Draw ultrasonic line
    end_x = 640 * math.cos(math.radians(radar_angle))
    end_y = -640 * math.sin(math.radians(radar_angle))
    ax.plot([0, end_x], [0, end_y], color='green', linewidth=2)

    # Draw object detection line
    if radar_distance < 40:
        object_distance = radar_distance * 15
        obj_end_x = object_distance * math.cos(math.radians(radar_angle))
        obj_end_y = -object_distance * math.sin(math.radians(radar_angle))
        ax.plot([obj_end_x, end_x], [obj_end_y, end_y], color='red', linewidth=2)

# Initialize serial port
init_serial()

# Setup the animation
ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)

# Show the plot
plt.show()

# Ensure the serial port is closed properly on exit
import atexit
atexit.register(serial_port.close)
