import tkinter as tk
import math
import random
import os

# Initial configuration
step = 15
segment_radius = 10
direction_vector = [1, 0]
foods = []
snake_segments = []

# Create window
root = tk.Tk()
root.title("Snake")

# Load icon (must be .png)
logo_path = os.path.abspath("logo.png")
try:
    icon = tk.PhotoImage(file=logo_path)
    root.iconphoto(True, icon)
except Exception as e:
    print(f"Could not load icon: {e}")

# Fullscreen
root.state('zoomed')
root.configure(bg='green')

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

canvas = tk.Canvas(root, bg='green', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

BOUND_X = screen_width / 2 - 10
BOUND_Y = screen_height / 2 - 10

# Create snake
def create_circle(x, y, r, **kwargs):
    return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

head_x, head_y = screen_width // 2, screen_height // 2
head = create_circle(head_x, head_y, segment_radius, fill="red")
snake_segments.append(head)

for i in range(1, 6):
    x = head_x - i * 2 * segment_radius
    y = head_y
    segment = create_circle(x, y, segment_radius, fill="red")
    snake_segments.append(segment)

def get_coords(segment_id):
    coords = canvas.coords(segment_id)
    x = (coords[0] + coords[2]) / 2
    y = (coords[1] + coords[3]) / 2
    return x, y

def move_snake():
    global direction_vector

    x, y = get_coords(snake_segments[0])

    if foods:
        fx, fy = get_coords(foods[0])
        dx = fx - x
        dy = fy - y
        dist = math.hypot(dx, dy)

        if dist < step:
            canvas.delete(foods[0])
            foods.pop(0)
            add_segment()
        else:
            angle = math.atan2(dy, dx)
            direction_vector = [math.cos(angle), math.sin(angle)]

    new_x = x + step * direction_vector[0]
    new_y = y + step * direction_vector[1]

    if abs(new_x - screen_width / 2) > BOUND_X or abs(new_y - screen_height / 2) > BOUND_Y:
        angle = random.uniform(0, 2 * math.pi)
        direction_vector = [math.cos(angle), math.sin(angle)]
        new_x = x + step * direction_vector[0]
        new_y = y + step * direction_vector[1]

    # Move head
    canvas.coords(snake_segments[0], new_x - segment_radius, new_y - segment_radius,
                  new_x + segment_radius, new_y + segment_radius)

    # Move body
    for i in range(len(snake_segments) - 1, 0, -1):
        prev_x, prev_y = get_coords(snake_segments[i - 1])
        canvas.coords(snake_segments[i],
                      prev_x - segment_radius, prev_y - segment_radius,
                      prev_x + segment_radius, prev_y + segment_radius)

    root.after(100, move_snake)

def add_segment():
    last_x, last_y = get_coords(snake_segments[-1])
    segment = create_circle(last_x, last_y, segment_radius, fill="red")
    snake_segments.append(segment)

def on_click(event):
    food = create_circle(event.x, event.y, segment_radius, fill="brown")
    foods.append(food)

canvas.bind("<Button-1>", on_click)

move_snake()
root.mainloop()
