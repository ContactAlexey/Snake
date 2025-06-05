import tkinter as tk
import math
import random
import os
import sys

# Initial configuration of game parameters
step = 15  # Movement step size in pixels
segment_radius = 10  # Radius of each snake segment and food circle
direction_vector = [1, 0]  # Initial movement direction (right)
foods = []  # List to hold food items on canvas
snake_segments = []  # List to hold snake body segments
max_size = 6  # Maximum allowed snake length before shrinking
shrink_time = 60000  # Time interval (ms) before snake shrinks (1 minute)
shrink_timer = None  # Timer reference for shrinking snake

# Create main application window
root = tk.Tk()
root.title("Snake")  # Set window title

# Load icon if available (useful when frozen into an executable)
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_path, "logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Setup fullscreen mode and window resizing options
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)
    root.geometry("1024x768")  # Window size after exiting fullscreen

root.attributes('-fullscreen', True)
root.resizable(False, False)  # Disable window resizing

# Create drawing canvas with green background to display the game
canvas = tk.Canvas(root, bg='green', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Helper function to create a circle shape on the canvas
def create_circle(x, y, r, **kwargs):
    return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

# Initialize or reset the snake on the canvas
def reset_snake():
    global snake_segments
    canvas.delete("all")  # Clear the canvas
    snake_segments = []
    # Start snake head at center of the window
    head_x = root.winfo_width() // 2
    head_y = root.winfo_height() // 2
    head = create_circle(head_x, head_y, segment_radius, fill="black")
    snake_segments.append(head)

    # Add remaining snake segments to the left of the head
    for i in range(1, max_size):
        x = head_x - i * 2 * segment_radius
        y = head_y
        segment = create_circle(x, y, segment_radius, fill="red")
        snake_segments.append(segment)

# Get the center coordinates of a given segment by its canvas ID
def get_coords(segment_id):
    coords = canvas.coords(segment_id)
    x = (coords[0] + coords[2]) / 2
    y = (coords[1] + coords[3]) / 2
    return x, y

# Main game loop: moves the snake, processes food eating and direction changes
def move_snake():
    global direction_vector, shrink_timer
    x, y = get_coords(snake_segments[0])  # Get current head position

    if foods:
        # Find closest food to snake head
        closest_food = None
        min_distance = float('inf')
        for food in foods:
            fx, fy = get_coords(food)
            dist = math.hypot(fx - x, fy - y)
            if dist < min_distance:
                min_distance = dist
                closest_food = food

        if closest_food:
            fx, fy = get_coords(closest_food)
            dx = fx - x
            dy = fy - y

            # If close enough to food, eat it and grow snake
            if min_distance < step:
                canvas.delete(closest_food)
                foods.remove(closest_food)
                add_segment()
                reset_shrink_timer()
            else:
                # Update movement direction towards the food
                angle = math.atan2(dy, dx)
                direction_vector = [math.cos(angle), math.sin(angle)]

    # Calculate new head position based on direction
    new_x = x + step * direction_vector[0]
    new_y = y + step * direction_vector[1]

    # Bounce off walls by reversing direction if hitting edges
    if new_x - segment_radius < 0 or new_x + segment_radius > root.winfo_width():
        direction_vector[0] *= -1
    if new_y - segment_radius < 0 or new_y + segment_radius > root.winfo_height():
        direction_vector[1] *= -1

    # Recalculate new position after possible direction change
    new_x = x + step * direction_vector[0]
    new_y = y + step * direction_vector[1]

    # Move head to new position
    canvas.coords(snake_segments[0], new_x - segment_radius, new_y - segment_radius,
                  new_x + segment_radius, new_y + segment_radius)

    # Move each following segment to the previous segment's old position
    for i in range(len(snake_segments) - 1, 0, -1):
        prev_x, prev_y = get_coords(snake_segments[i - 1])
        canvas.coords(snake_segments[i],
                      prev_x - segment_radius, prev_y - segment_radius,
                      prev_x + segment_radius, prev_y + segment_radius)
        canvas.itemconfig(snake_segments[i], fill="red")

    # Color the head differently
    canvas.itemconfig(snake_segments[0], fill="black")
    # Repeat move_snake every 100ms to animate
    root.after(100, move_snake)

# Add a new segment at the end of the snake
def add_segment():
    last_x, last_y = get_coords(snake_segments[-1])
    segment = create_circle(last_x, last_y, segment_radius, fill="red")
    snake_segments.append(segment)

# Event handler: create food where the user clicks
def on_click(event):
    food = create_circle(event.x, event.y, segment_radius, fill="brown")
    foods.append(food)

# Reset or start the timer that triggers snake shrinking
def reset_shrink_timer():
    global shrink_timer
    if shrink_timer is not None:
        root.after_cancel(shrink_timer)  # Cancel existing timer
    shrink_timer = root.after(shrink_time, shrink_snake)

# Shrink the snake if it's longer than max_size by removing segments one by one
def shrink_snake():
    global snake_segments

    extra_segments = len(snake_segments) - max_size

    if extra_segments > 0:
        # Take extra segments in reverse order (last added first)
        to_remove = snake_segments[-extra_segments:][::-1]

        # Blink segments to be removed before deleting them
        def blink_and_remove(index=0):
            if index < len(to_remove):
                segment = to_remove[index]

                def blink(times=6):
                    if times > 0:
                        current_color = canvas.itemcget(segment, "fill")
                        new_color = "green" if current_color != "green" else "red"
                        canvas.itemconfig(segment, fill=new_color)
                        root.after(100, lambda: blink(times - 1))
                    else:
                        if segment in snake_segments:
                            canvas.delete(segment)
                            snake_segments.remove(segment)
                        blink_and_remove(index + 1)

                blink()
            else:
                reset_shrink_timer()  # Restart shrinking timer after done

        blink_and_remove()
    else:
        reset_shrink_timer()  # Restart shrinking timer if no segments to remove

# Bind mouse click to add food
canvas.bind("<Button-1>", on_click)

# Initialize game state and start main loop
reset_snake()
move_snake()
reset_shrink_timer()
root.mainloop()
