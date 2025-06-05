import tkinter as tk
import math
import os
import sys

# Game configuration
step = 15
segment_radius = 10
direction_vector = [1, 0]
foods = []
snake_segments = []
max_size = 6
shrink_time = 60000
shrink_timer = None

# Create window
root = tk.Tk()
root.title("Snake")

# Load icon (if any)
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_path, "logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Fullscreen setup
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)
    root.geometry("1024x768")

root.attributes('-fullscreen', True)
root.resizable(False, False)

canvas = tk.Canvas(root, bg='green', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

def create_circle(x, y, r, **kwargs):
    return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

def reset_snake():
    global snake_segments
    canvas.delete("all")
    snake_segments = []
    head_x = root.winfo_width() // 2
    head_y = root.winfo_height() // 2
    head = create_circle(head_x, head_y, segment_radius, fill="black")
    snake_segments.append(head)

    for i in range(1, max_size):
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
    global direction_vector, shrink_timer
    x, y = get_coords(snake_segments[0])

    if foods:
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

            if min_distance < step:
                canvas.delete(closest_food)
                foods.remove(closest_food)
                add_segment()
                reset_shrink_timer()
            else:
                angle = math.atan2(dy, dx)
                direction_vector = [math.cos(angle), math.sin(angle)]

    new_x = x + step * direction_vector[0]
    new_y = y + step * direction_vector[1]

    if new_x - segment_radius < 0 or new_x + segment_radius > root.winfo_width():
        direction_vector[0] *= -1
    if new_y - segment_radius < 0 or new_y + segment_radius > root.winfo_height():
        direction_vector[1] *= -1

    new_x = x + step * direction_vector[0]
    new_y = y + step * direction_vector[1]

    canvas.coords(snake_segments[0], new_x - segment_radius, new_y - segment_radius,
                  new_x + segment_radius, new_y + segment_radius)

    for i in range(len(snake_segments) - 1, 0, -1):
        prev_x, prev_y = get_coords(snake_segments[i - 1])
        canvas.coords(snake_segments[i],
                      prev_x - segment_radius, prev_y - segment_radius,
                      prev_x + segment_radius, prev_y + segment_radius)
        canvas.itemconfig(snake_segments[i], fill="red")

    canvas.itemconfig(snake_segments[0], fill="black")
    root.after(100, move_snake)

def add_segment():
    last_x, last_y = get_coords(snake_segments[-1])
    segment = create_circle(last_x, last_y, segment_radius, fill="red")
    snake_segments.append(segment)

def on_click(event):
    food = create_circle(event.x, event.y, segment_radius, fill="brown")
    foods.append(food)

def reset_shrink_timer():
    global shrink_timer
    if shrink_timer is not None:
        root.after_cancel(shrink_timer)
    shrink_timer = root.after(shrink_time, shrink_snake)

def shrink_snake():
    global snake_segments
    extra_segments = len(snake_segments) - max_size

    if extra_segments > 0:
        to_remove = snake_segments[-extra_segments:][::-1]

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
                reset_shrink_timer()
        blink_and_remove()
    else:
        reset_shrink_timer()

canvas.bind("<Button-1>", on_click)

# Start game after ensuring canvas size is updated
def start_game():
    root.update_idletasks()
    reset_snake()
    move_snake()
    reset_shrink_timer()

root.after(100, start_game)
root.mainloop()
