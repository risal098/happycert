import tkinter as tk
from tkinter import filedialog, colorchooser, simpledialog
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("800x600")

        # Variables
        self.image_path = None
        self.image = None
        self.tk_image = None
        self.text = "Full Name Risal"
        self.text_size = 20
        self.text_position = (100, 100)
        self.text_color = "#000000"
        self.text_font = "Arial"
        self.font_file = ""

        # Topbar with 6 buttons
        self.topbar = tk.Frame(root, bg="lightgray", height=40)
        self.topbar.pack(fill=tk.X)

        self.import_button = tk.Button(
            self.topbar, text="Import Image", command=self.import_image)
        self.import_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(
            self.topbar, text="Save", command=self.save)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.text_size_button = tk.Button(
            self.topbar, text="Increase Text Size", command=self.increase_text_size)
        self.text_size_button.pack(side=tk.LEFT, padx=10)

        self.decrease_size_button = tk.Button(
            self.topbar, text="Decrease Text Size", command=self.decrease_text_size)
        self.decrease_size_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(
            self.topbar, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.font_button = tk.Button(
            self.topbar, text="Change Font", command=self.change_font)
        self.font_button.pack(side=tk.LEFT, padx=10)

        self.color_button = tk.Button(
            self.topbar, text="Change Text Color", command=self.change_color)
        self.color_button.pack(side=tk.LEFT, padx=10)

        # Canvas for image and text
        self.canvas = tk.Canvas(root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Mouse click to place text
        self.canvas.bind("<Button-1>", self.on_click)
        # Mouse drag to move text
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def import_image(self):
        """Open file dialog to import an image and show it."""
        file_path = filedialog.askopenfilename(title="Open Image", filetypes=[
                                               ("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_path = file_path
            self.image = Image.open(self.image_path)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.canvas.create_text(self.text_position, text=self.text, font=(
                self.text_font, self.text_size), fill=self.text_color, tags="text")
            print(f"Image Path: {self.image_path}")
            print(
                f"Text Position: {self.text_position}, Text Size: {self.text_size}, Text Font: {self.text_font}, Text Color: {self.text_color}")

    def on_click(self, event):
        """Handle mouse click to set text position."""
        self.text_position = (event.x, event.y)
        self.update_text_position()

    def on_drag(self, event):
        """Handle mouse drag to move text."""
        self.text_position = (event.x, event.y)
        self.update_text_position()

    def update_text_position(self):
        """Update the position and print to CLI."""
        self.canvas.delete("text")  # Delete old text
        self.canvas.create_text(self.text_position, text=self.text, font=(
            self.text_font, self.text_size), fill=self.text_color, tags="text")
        print(
            f"Text Position: {self.text_position}, Text Size: {self.text_size}, Text Font: {self.text_font}, Text Color: {self.text_color}")

    def increase_text_size(self):
        """Increase text size and update text."""
        self.text_size += 2
        self.update_text_size()

    def decrease_text_size(self):
        """Decrease text size and update text."""
        if self.text_size > 2:
            self.text_size -= 2
        self.update_text_size()

    def save(self):
        image = Image.open(self.image_path)
        draw = ImageDraw.Draw(image)
        if self.font_file=="":
        	font=ImageFont.truetype("arial.ttf", size=self.text_size*1.3)
        else:
        	font = ImageFont.truetype(self.font_file, size=self.text_size*1.3)
        text = "Full Name Risal"
        position = self.text_position
        hex_color = self.text_color
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        draw.text(position, text, font=font, fill=rgb_color)
       # image.save('output_image.png')  # Save to a new file
        image.show()  # Optionally, show the image

    def update_text_size(self):
        """Update the size of the text and print to CLI."""
        self.canvas.delete("text")  # Delete old text
        self.canvas.create_text(self.text_position, text=self.text, font=(
            self.text_font, self.text_size), fill=self.text_color, tags="text")
        print(
            f"Text Position: {self.text_position}, Text Size: {self.text_size}, Text Font: {self.text_font}, Text Color: {self.text_color}")

    def change_font(self):
        """Allow the user to select a custom font (.ttf) from their folder."""
        font_file = filedialog.askopenfilename(title="Select Font", filetypes=[
                                               ("TrueType Font", "*.ttf *.otf")])
        if font_file and os.path.exists(font_file):
            # Load the font into Tkinter
            try:
                self.text_font = tkfont.Font(
                    family=font_file)  # Load the font file
                self.font_file = str(font_file)
                print(f"Selected Font: {self.font_file},{self.text_font},")
                self.update_text_size()
            except Exception as e:
                print(f"Error loading font: {e}")

    def change_color(self):
        """Change the text color using a color chooser."""
        color = colorchooser.askcolor()[1]  # Returns a hex color
        if color:
            self.text_color = color
            self.update_text_size()

    def reset(self):
        """Reset the canvas and settings."""
        self.canvas.delete("all")
        self.text_size = 20
        self.text_position = (100, 100)
        self.text_color = "#000000"
        self.text_font = "Arial"
        self.font_file = ""
        print(
            f"Text Position: {self.text_position}, Text Size: {self.text_size}, Text Font: {self.text_font}, Text Color: {self.text_color}")


# Main program to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
