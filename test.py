# All icons in this program are made by: https://www.flaticon.com/authors/graphics-plazza

import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

root = tk.Tk()
root.title("Watermark App")

canvas = tk.Canvas(root, width=500, height=500, bg="#313131")
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)  # Place canvas on the left side and fill the entire space

button_frame = tk.Frame(root, bg="#59545e")
button_frame.pack(side=tk.RIGHT, fill=tk.Y)  # Place button_frame on the right side and fill vertically

image_label = None
original_image = None
watermarked_image = None
watermark_color = (255, 255, 255)  # Initial watermark color (white)
watermark_opacity = 1.0  # Initial watermark opacity (fully opaque)
watermark_position = (0, 0)  # Initial watermark position


# Function to open an image and resize it to 500x500
def open_image():
    global original_image
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = Image.open(file_path)
        original_image = original_image.resize((500, 500), Image.LANCZOS)  # Resize image to 500x500 with antialiasing
        display_image(original_image)


# Function to display an image on the canvas
def display_image(image):
    global image_label, watermarked_image
    tk_image = ImageTk.PhotoImage(image)
    image_label = tk_image
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    watermarked_image = None  # Reset watermarked image when displaying new original image


# Function to add watermark text to the image with specified color and opacity
def add_watermark():
    global original_image, watermarked_image, watermark_color, watermark_opacity, watermark_position
    if original_image is not None:
        watermark_text = simpledialog.askstring("Input", "Enter watermark text:", initialvalue="@")
        if watermark_text:
            if not watermark_text.startswith("@"):
                watermark_text = "@" + watermark_text
            watermarked_image = original_image.copy()
            draw = ImageDraw.Draw(watermarked_image)
            font = ImageFont.truetype("arial.ttf", 20)
            width, height = watermarked_image.size
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_position = (watermark_position[0], watermark_position[1])
            fill_color = (*watermark_color, int(255 * watermark_opacity))  # Ensure opacity affects transparency
            draw.text(text_position, watermark_text, font=font, fill=fill_color)
            display_image(watermarked_image)


# Function to save the watermarked image
def save_image():
    global watermarked_image
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        watermarked_image.save(file_path)


# Function to open color picker and update watermark color
def choose_color():
    global watermark_color
    color = colorchooser.askcolor(title="Choose Watermark Color")
    if color:
        watermark_color = tuple(map(int, color[0]))  # Convert color tuple to integer RGB values
        if watermarked_image:
            add_watermark()  # Reapply watermark with new color


# Function to update watermark opacity
def update_opacity(value):
    global watermark_opacity
    watermark_opacity = float(value) / 100.0  # Convert slider value to opacity (0.0 to 1.0)
    if watermarked_image:
        add_watermark()  # Reapply watermark with new opacity


# Function to adjust watermark position
def move_watermark(direction):
    global watermark_position
    step = 10  # Move 10 pixels at a time
    x, y = watermark_position
    if direction == "UP":
        y -= step
    elif direction == "DOWN":
        y += step
    elif direction == "LEFT":
        x -= step
    elif direction == "RIGHT":
        x += step
    watermark_position = (x, y)
    if watermarked_image:
        add_watermark()  # Reapply watermark with new position


# Function to reset canvas to initial state
def reset_canvas():
    global original_image
    if original_image:
        display_image(original_image)
        watermark_position = (0, 0)  # Reset watermark position


# Load images for buttons
save_img = Image.open("img/download.png")
save_img = save_img.resize((32, 32))
saveImg = ImageTk.PhotoImage(save_img)

open_img = Image.open("img/upload.png")
open_img = open_img.resize((32, 32))
openImg = ImageTk.PhotoImage(open_img)

water_img = Image.open("img/water.png")
water_img = water_img.resize((32, 32))
waterImg = ImageTk.PhotoImage(water_img)

palette_img = Image.open("img/palette.png")
palette_img = palette_img.resize((32, 32))
paletteImg = ImageTk.PhotoImage(palette_img)

up_img = Image.open("img/up-arrow.png")
up_img = up_img.resize((32, 32))
upImg = ImageTk.PhotoImage(up_img)

down_img = Image.open("img/down-arrow.png")
down_img = down_img.resize((32, 32))
downImg = ImageTk.PhotoImage(down_img)

left_img = Image.open("img/left-arrow.png")
left_img = left_img.resize((32, 32))
leftImg = ImageTk.PhotoImage(left_img)

right_img = Image.open("img/right-arrow.png")
right_img = right_img.resize((32, 32))
rightImg = ImageTk.PhotoImage(right_img)

# Create labels above each button using grid layout
label_color = tk.Label(button_frame, borderwidth=0, highlightthickness=0, bg="#59545e", text="Watermark color:")
label_color.grid(row=0, column=0, padx=1, pady=1, sticky=tk.E)

label_watermark = tk.Label(button_frame, borderwidth=0, highlightthickness=0, bg="#59545e", text="Watermark:")
label_watermark.grid(row=1, column=0, padx=1, pady=1, sticky=tk.E)

label_open = tk.Label(button_frame, borderwidth=0, highlightthickness=0, bg="#59545e", text="Open:")
label_open.grid(row=2, column=0, padx=1, pady=1, sticky=tk.E)

label_save = tk.Label(button_frame, borderwidth=0, highlightthickness=0, bg="#59545e", text="Download:")
label_save.grid(row=3, column=0, padx=1, pady=1, sticky=tk.E)

# Create buttons with images and commands
color_button = tk.Button(button_frame, borderwidth=0, highlightthickness=0, bg="#59545e",
                         activebackground="#313131", image=paletteImg, command=choose_color)
color_button.grid(row=0, column=1, padx=1, pady=1, sticky=tk.W)

watermark_button = tk.Button(button_frame, borderwidth=0, highlightthickness=0, bg="#59545e",
                             activebackground="#313131", image=waterImg, command=add_watermark)
watermark_button.grid(row=1, column=1, padx=1, pady=1, sticky=tk.W)

open_button = tk.Button(button_frame, borderwidth=0, highlightthickness=0, bg="#59545e",
                        activebackground="#313131", image=openImg, command=open_image)
open_button.grid(row=2, column=1, padx=1, pady=1, sticky=tk.W)

save_button = tk.Button(button_frame, borderwidth=0, highlightthickness=0, bg="#59545e",
                        activebackground="#313131", image=saveImg, command=save_image)
save_button.grid(row=3, column=1, padx=1, pady=1, sticky=tk.W)

# Buttons for adjusting watermark position
up_button = tk.Button(button_frame, image=upImg, bg="#59545e",
                      activebackground="#313131", fg="white", command=lambda: move_watermark("UP"))
up_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)

down_button = tk.Button(button_frame, image=downImg, bg="#59545e",
                        activebackground="#313131", fg="white", command=lambda: move_watermark("DOWN"))
down_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)

left_button = tk.Button(button_frame, image=leftImg, bg="#59545e",
                        activebackground="#313131", fg="white", command=lambda: move_watermark("LEFT"))
left_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)

right_button = tk.Button(button_frame, image=rightImg, bg="#59545e",
                         activebackground="#313131",fg="white", command=lambda: move_watermark("RIGHT"))
right_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)

reset_button = tk.Button(button_frame, text="Reset", bg="#59545e", fg="white", command=reset_canvas)
reset_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

# Slider for adjusting watermark opacity
opacity_slider = tk.Scale(button_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Opacity:", command=update_opacity,
                          bg="#59545e", fg="white", highlightthickness=0)
opacity_slider.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)

# Configure row weights to center buttons vertically
for i in range(4):  # Assuming there are 4 rows
    button_frame.grid_rowconfigure(i, weight=1)

root.mainloop()
